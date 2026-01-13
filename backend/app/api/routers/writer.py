# AIMETA P=写作API_章节生成和大纲创建|R=章节生成_大纲生成_评审|NR=不含数据存储|E=route:POST_/api/writer/*|X=http|A=生成_评审|D=fastapi,openai|S=net,db|RD=./README.ai
import json
import logging
import os
from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.config import settings
from ...core.dependencies import get_current_user
from ...db.session import get_session
from ...models.novel import Chapter, ChapterOutline
from ...schemas.novel import (
    DeleteChapterRequest,
    EditChapterRequest,
    EvaluateChapterRequest,
    GenerateChapterRequest,
    GenerateOutlineRequest,
    NovelProject as NovelProjectSchema,
    SelectVersionRequest,
    UpdateChapterOutlineRequest,
)
from ...schemas.user import UserInDB
from ...services.chapter_context_service import ChapterContextService
from ...services.chapter_ingest_service import ChapterIngestionService
from ...services.llm_service import LLMService
from ...services.novel_service import NovelService
from ...services.prompt_service import PromptService
from ...services.vector_store_service import VectorStoreService
from ...utils.json_utils import remove_think_tags, unwrap_markdown_json
from ...repositories.system_config_repository import SystemConfigRepository

router = APIRouter(prefix="/api/writer", tags=["Writer"])
logger = logging.getLogger(__name__)


async def _load_project_schema(service: NovelService, project_id: str, user_id: int) -> NovelProjectSchema:
    return await service.get_project_schema(project_id, user_id)


def _extract_tail_excerpt(text: Optional[str], limit: int = 500) -> str:
    """截取章节结尾文本，默认保留 500 字。"""
    if not text:
        return ""
    stripped = text.strip()
    if len(stripped) <= limit:
        return stripped
    return stripped[-limit:]


@router.post("/novels/{project_id}/chapters/generate", response_model=NovelProjectSchema)
async def generate_chapter(
    project_id: str,
    request: GenerateChapterRequest,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> NovelProjectSchema:
    novel_service = NovelService(session)
    prompt_service = PromptService(session)
    llm_service = LLMService(session)

    project = await novel_service.ensure_project_owner(project_id, current_user.id)
    logger.info("用户 %s 开始为项目 %s 生成第 %s 章", current_user.id, project_id, request.chapter_number)
    outline = await novel_service.get_outline(project_id, request.chapter_number)
    if not outline:
        logger.warning("项目 %s 未找到第 %s 章纲要，生成流程终止", project_id, request.chapter_number)
        raise HTTPException(status_code=404, detail="蓝图中未找到对应章节纲要")

    chapter = await novel_service.get_or_create_chapter(project_id, request.chapter_number)
    chapter.real_summary = None
    chapter.selected_version_id = None
    chapter.status = "generating"
    await session.commit()

    outlines_map = {item.chapter_number: item for item in project.outlines}
    # 收集所有可用的历史章节摘要，便于在 Prompt 中提供前情背景
    completed_chapters = []
    latest_prev_number = -1
    previous_summary_text = ""
    previous_tail_excerpt = ""
    for existing in project.chapters:
        if existing.chapter_number >= request.chapter_number:
            continue
        if existing.selected_version is None or not existing.selected_version.content:
            continue
        if not existing.real_summary:
            summary = await llm_service.get_summary(
                existing.selected_version.content,
                temperature=0.15,
                user_id=current_user.id,
                timeout=180.0,
            )
            existing.real_summary = remove_think_tags(summary)
            await session.commit()
        completed_chapters.append(
            {
                "chapter_number": existing.chapter_number,
                "title": outlines_map.get(existing.chapter_number).title if outlines_map.get(existing.chapter_number) else f"第{existing.chapter_number}章",
                "summary": existing.real_summary,
            }
        )
        if existing.chapter_number > latest_prev_number:
            latest_prev_number = existing.chapter_number
            previous_summary_text = existing.real_summary or ""
            previous_tail_excerpt = _extract_tail_excerpt(existing.selected_version.content)

    project_schema = await novel_service._serialize_project(project)
    blueprint_dict = project_schema.blueprint.model_dump()

    if "relationships" in blueprint_dict and blueprint_dict["relationships"]:
        for relation in blueprint_dict["relationships"]:
            if "character_from" in relation:
                relation["from"] = relation.pop("character_from")
            if "character_to" in relation:
                relation["to"] = relation.pop("character_to")

    # 蓝图中禁止携带章节级别的细节信息，避免重复传输大段场景或对话内容
    banned_blueprint_keys = {
        "chapter_outline",
        "chapter_summaries",
        "chapter_details",
        "chapter_dialogues",
        "chapter_events",
        "conversation_history",
        "character_timelines",
    }
    for key in banned_blueprint_keys:
        if key in blueprint_dict:
            blueprint_dict.pop(key, None)

    writer_prompt = await prompt_service.get_prompt("writing")
    if not writer_prompt:
        logger.error("未配置名为 'writing' 的写作提示词，无法生成章节内容")
        raise HTTPException(status_code=500, detail="缺少写作提示词，请联系管理员配置 'writing' 提示词")

    # 初始化向量检索服务，若未配置则自动降级为纯提示词生成
    vector_store: Optional[VectorStoreService]
    if not settings.vector_store_enabled:
        vector_store = None
    else:
        try:
            vector_store = VectorStoreService()
        except RuntimeError as exc:
            logger.warning("向量库初始化失败，RAG 检索被禁用: %s", exc)
            vector_store = None
    context_service = ChapterContextService(llm_service=llm_service, vector_store=vector_store)

    outline_title = outline.title or f"第{outline.chapter_number}章"
    outline_summary = outline.summary or "暂无摘要"
    query_parts = [outline_title, outline_summary]
    if request.writing_notes:
        query_parts.append(request.writing_notes)
    rag_query = "\n".join(part for part in query_parts if part)
    rag_context = await context_service.retrieve_for_generation(
        project_id=project_id,
        query_text=rag_query or outline.title or outline.summary or "",
        user_id=current_user.id,
    )
    chunk_count = len(rag_context.chunks) if rag_context and rag_context.chunks else 0
    summary_count = len(rag_context.summaries) if rag_context and rag_context.summaries else 0
    logger.info(
        "项目 %s 第 %s 章检索到 %s 个剧情片段和 %s 条摘要",
        project_id,
        request.chapter_number,
        chunk_count,
        summary_count,
    )
    # print("rag_context:",rag_context)
    # 将蓝图、前情、RAG 检索结果拼装成结构化段落，供模型理解
    blueprint_text = json.dumps(blueprint_dict, ensure_ascii=False, indent=2)
    completed_lines = [
        f"- 第{item['chapter_number']}章 - {item['title']}:{item['summary']}"
        for item in completed_chapters
    ]
    previous_summary_text = previous_summary_text or "暂无可用摘要"
    previous_tail_excerpt = previous_tail_excerpt or "暂无上一章结尾内容"
    completed_section = "\n".join(completed_lines) if completed_lines else "暂无前情摘要"
    rag_chunks_text = "\n\n".join(rag_context.chunk_texts()) if rag_context.chunks else "未检索到章节片段"
    rag_summaries_text = "\n".join(rag_context.summary_lines()) if rag_context.summaries else "未检索到章节摘要"
    writing_notes = request.writing_notes or "无额外写作指令"

    prompt_sections = [
        ("[世界蓝图](JSON)", blueprint_text),
        # ("[前情摘要]", completed_section),
        ("[上一章摘要]", previous_summary_text),
        ("[上一章结尾]", previous_tail_excerpt),
        ("[检索到的剧情上下文](Markdown)", rag_chunks_text),
        ("[检索到的章节摘要](Markdown)", rag_summaries_text),
        (
            "[当前章节目标]",
            f"标题：{outline_title}\n摘要：{outline_summary}\n写作要求：{writing_notes}",
        ),
    ]
    prompt_input = "\n\n".join(f"{title}\n{content}" for title, content in prompt_sections if content)
    logger.debug("章节写作提示词：%s\n%s", writer_prompt, prompt_input)
    
    async def _generate_single_version(idx: int) -> Dict:
        try:
            response = await llm_service.get_llm_response(
                system_prompt=writer_prompt,
                conversation_history=[{"role": "user", "content": prompt_input}],
                temperature=0.9,
                user_id=current_user.id,
                timeout=600.0,
            )
            cleaned = remove_think_tags(response)
            normalized = unwrap_markdown_json(cleaned)
            try:
                return json.loads(normalized)
            except json.JSONDecodeError as parse_err:
                logger.warning(
                    "项目 %s 第 %s 章第 %s 个版本 JSON 解析失败，将原始内容作为纯文本处理: %s",
                    project_id,
                    request.chapter_number,
                    idx + 1,
                    parse_err,
                )
                return {"content": normalized}
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception(
                "项目 %s 生成第 %s 章第 %s 个版本时发生异常: %s",
                project_id,
                request.chapter_number,
                idx + 1,
                exc,
            )
            raise HTTPException(
                status_code=500,
                detail=f"生成章节第 {idx + 1} 个版本时失败: {str(exc)[:200]}"
            )

    version_count = await _resolve_version_count(session)
    logger.info(
        "项目 %s 第 %s 章计划生成 %s 个版本",
        project_id,
        request.chapter_number,
        version_count,
    )
    
    raw_versions = []
    try:
        for idx in range(version_count):
            raw_versions.append(await _generate_single_version(idx))
    except Exception as exc:
        logger.exception("项目 %s 生成第 %s 章时发生异常: %s", project_id, request.chapter_number, exc)
        chapter.status = "failed"
        await session.commit()
        if isinstance(exc, HTTPException):
            raise exc
        raise HTTPException(
            status_code=500,
            detail=f"生成章节失败: {str(exc)[:200]}"
        )

    contents: List[str] = []
    metadata: List[Dict] = []
    for variant in raw_versions:
        if isinstance(variant, dict):
            if "content" in variant and isinstance(variant["content"], str):
                contents.append(variant["content"])
            elif "chapter_content" in variant:
                contents.append(str(variant["chapter_content"]))
            else:
                contents.append(json.dumps(variant, ensure_ascii=False))
            metadata.append(variant)
        else:
            contents.append(str(variant))
            metadata.append({"raw": variant})

    await novel_service.replace_chapter_versions(chapter, contents, metadata)
    logger.info(
        "项目 %s 第 %s 章生成完成，已写入 %s 个版本",
        project_id,
        request.chapter_number,
        len(contents),
    )
    return await _load_project_schema(novel_service, project_id, current_user.id)


async def _resolve_version_count(session: AsyncSession) -> int:
    repo = SystemConfigRepository(session)
    record = await repo.get_by_key("writer.version_count")
    if record and record.value:
        try:
            return int(record.value)
        except ValueError:
            pass
    return int(os.getenv("WRITER_VERSION_COUNT", "3"))


@router.post("/novels/{project_id}/chapters/select", response_model=NovelProjectSchema)
async def select_chapter_version(
    project_id: str,
    request: SelectVersionRequest,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> NovelProjectSchema:
    novel_service = NovelService(session)
    project = await novel_service.ensure_project_owner(project_id, current_user.id)
    chapter = await novel_service.get_or_create_chapter(project_id, request.chapter_number)

    # 使用 novel_service.select_chapter_version 确保排序一致
    # 该函数会按 created_at 排序并校验索引
    selected_version = await novel_service.select_chapter_version(chapter, request.version_index)
    
    # 校验内容是否为空
    if not selected_version.content or len(selected_version.content.strip()) == 0:
        # 回滚状态，不标记为 successful
        await session.rollback()
        raise HTTPException(status_code=400, detail="选中的版本内容为空，无法确认为最终版")

    # 异步触发向量化入库
    try:
        llm_service = LLMService(session)
        ingest_service = ChapterIngestionService(llm_service=llm_service)
        await ingest_service.ingest_chapter(
            project_id=project_id,
            chapter_number=request.chapter_number,
            title=chapter.title or f"第{request.chapter_number}章",
            content=selected_version.content,
            summary=None
        )
        logger.info(f"章节 {request.chapter_number} 向量化入库成功")
    except Exception as e:
        logger.error(f"章节 {request.chapter_number} 向量化入库失败: {e}")
        # 向量化失败不应阻止版本选择，仅记录错误

    return await _load_project_schema(novel_service, project_id, current_user.id)


@router.post("/novels/{project_id}/chapters/evaluate", response_model=NovelProjectSchema)
async def evaluate_chapter(
    project_id: str,
    request: EvaluateChapterRequest,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> NovelProjectSchema:
    novel_service = NovelService(session)
    prompt_service = PromptService(session)
    llm_service = LLMService(session)

    project = await novel_service.ensure_project_owner(project_id, current_user.id)
    # 确保预加载 selected_version 关系
    from sqlalchemy.orm import selectinload
    stmt = (
        select(Chapter)
        .options(selectinload(Chapter.selected_version))
        .where(
            Chapter.project_id == project_id,
            Chapter.chapter_number == request.chapter_number,
        )
    )
    result = await session.execute(stmt)
    chapter = result.scalars().first()
    
    if not chapter:
        chapter = await novel_service.get_or_create_chapter(project_id, request.chapter_number)

    # 如果没有选中版本，使用最新版本进行评审
    version_to_evaluate = chapter.selected_version
    if not version_to_evaluate:
        # 获取该章节的所有版本，选择最新的一个
        from sqlalchemy.orm import selectinload
        stmt_versions = (
            select(Chapter)
            .options(selectinload(Chapter.versions))
            .where(
                Chapter.project_id == project_id,
                Chapter.chapter_number == request.chapter_number,
            )
        )
        result_versions = await session.execute(stmt_versions)
        chapter_with_versions = result_versions.scalars().first()
        
        if not chapter_with_versions or not chapter_with_versions.versions:
            raise HTTPException(status_code=400, detail="该章节还没有生成任何版本，无法进行评审")
        
        # 使用最新的版本（列表中的最后一个）
        version_to_evaluate = chapter_with_versions.versions[-1]
    
    if not version_to_evaluate or not version_to_evaluate.content:
        raise HTTPException(status_code=400, detail="版本内容为空，无法进行评审")

    chapter.status = "evaluating"
    await session.commit()

    eval_prompt = await prompt_service.get_prompt("evaluation")
    if not eval_prompt:
        logger.warning("未配置名为 'evaluation' 的评审提示词，将跳过 AI 评审")
        # 使用 add_chapter_evaluation 创建评审记录
        await novel_service.add_chapter_evaluation(
            chapter=chapter,
            version=version_to_evaluate,
            feedback="未配置评审提示词",
            decision="skipped"
        )
        return await _load_project_schema(novel_service, project_id, current_user.id)

    try:
        evaluation_raw = await llm_service.get_llm_response(
            system_prompt=eval_prompt,
            conversation_history=[{"role": "user", "content": version_to_evaluate.content}],
            temperature=0.3,
            user_id=current_user.id,
        )
        evaluation_text = remove_think_tags(evaluation_raw)
        
        # 校验 AI 返回的内容不为空
        if not evaluation_text or len(evaluation_text.strip()) == 0:
            raise ValueError("评审结果为空")
        
        # 使用 add_chapter_evaluation 创建评审记录
        # 这会自动设置状态为 WAITING_FOR_CONFIRM
        await novel_service.add_chapter_evaluation(
            chapter=chapter,
            version=version_to_evaluate,
            feedback=evaluation_text,
            decision="reviewed"
        )
        logger.info("项目 %s 第 %s 章评审成功", project_id, request.chapter_number)
    except Exception as exc:
        logger.exception("项目 %s 第 %s 章评审失败: %s", project_id, request.chapter_number, exc)
        # 回滚事务，恢复状态
        await session.rollback()
        
        # 重新加载 chapter 对象（因为 rollback 后对象已脱离 session）
        stmt = (
            select(Chapter)
            .where(
                Chapter.project_id == project_id,
                Chapter.chapter_number == request.chapter_number,
            )
        )
        result = await session.execute(stmt)
        chapter = result.scalars().first()
        
        if chapter:
            # 使用 add_chapter_evaluation 创建失败记录
            # 注意：这里不能再用 add_chapter_evaluation，因为它会设置状态为 waiting_for_confirm
            # 失败时应该设置为 evaluation_failed
            from app.models.novel import ChapterEvaluation
            evaluation_record = ChapterEvaluation(
                chapter_id=chapter.id,
                version_id=version_to_evaluate.id,
                decision="failed",
                feedback=f"评审失败: {str(exc)}",
                score=None
            )
            session.add(evaluation_record)
            chapter.status = "evaluation_failed"
            await session.commit()
        
        # 抛出异常，让前端知道评审失败
        raise HTTPException(status_code=500, detail=f"评审失败: {str(exc)}")
    
    return await _load_project_schema(novel_service, project_id, current_user.id)


@router.post("/novels/{project_id}/chapters/update-outline", response_model=NovelProjectSchema)
async def update_chapter_outline(
    project_id: str,
    request: UpdateChapterOutlineRequest,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> NovelProjectSchema:
    novel_service = NovelService(session)
    await novel_service.ensure_project_owner(project_id, current_user.id)

    outline = await novel_service.get_outline(project_id, request.chapter_number)
    if not outline:
        raise HTTPException(status_code=404, detail="未找到对应章节大纲")

    outline.title = request.title
    outline.summary = request.summary
    outline.narrative_phase = request.narrative_phase
    outline.foreshadowing = request.foreshadowing
    outline.emotion_hook = request.emotion_hook
    await session.commit()

    return await _load_project_schema(novel_service, project_id, current_user.id)


@router.post("/novels/{project_id}/chapters/delete", response_model=NovelProjectSchema)
async def delete_chapters(
    project_id: str,
    request: DeleteChapterRequest,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> NovelProjectSchema:
    novel_service = NovelService(session)
    await novel_service.ensure_project_owner(project_id, current_user.id)

    for ch_num in request.chapter_numbers:
        await novel_service.delete_chapter(project_id, ch_num)

    await session.commit()
    return await _load_project_schema(novel_service, project_id, current_user.id)


@router.post("/novels/{project_id}/chapters/outline", response_model=NovelProjectSchema)
async def generate_chapters_outline(
    project_id: str,
    request: GenerateOutlineRequest,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> NovelProjectSchema:
    novel_service = NovelService(session)
    prompt_service = PromptService(session)
    llm_service = LLMService(session)

    project = await novel_service.ensure_project_owner(project_id, current_user.id)
    
    # 获取蓝图信息
    project_schema = await novel_service._serialize_project(project)
    blueprint_text = json.dumps(project_schema.blueprint.model_dump(), ensure_ascii=False, indent=2)
    
    # 获取已有的章节大纲
    existing_outlines = [
        f"第{o.chapter_number}章 - {o.title}: {o.summary}"
        for o in sorted(project.outlines, key=lambda x: x.chapter_number)
    ]
    existing_outlines_text = "\n".join(existing_outlines) if existing_outlines else "暂无"

    outline_prompt = await prompt_service.get_prompt("outline_generation")
    if not outline_prompt:
        raise HTTPException(status_code=500, detail="未配置大纲生成提示词")

    prompt_input = f"""
[世界蓝图]
{blueprint_text}

[已有章节大纲]
{existing_outlines_text}

[生成任务]
请从第 {request.start_chapter} 章开始，续写接下来的 {request.num_chapters} 章的大纲。
要求返回 JSON 格式，包含一个 chapters 数组，每个元素包含 chapter_number, title, summary。
"""

    response = await llm_service.get_llm_response(
        system_prompt=outline_prompt,
        conversation_history=[{"role": "user", "content": prompt_input}],
        temperature=0.7,
        user_id=current_user.id,
    )
    
    cleaned = remove_think_tags(response)
    normalized = unwrap_markdown_json(cleaned)
    try:
        data = json.loads(normalized)
        new_outlines = data.get("chapters", [])
        for item in new_outlines:
            await novel_service.update_or_create_outline(
                project_id, 
                item["chapter_number"], 
                item["title"], 
                item["summary"]
            )
        await session.commit()
    except Exception as exc:
        logger.exception("生成大纲解析失败: %s", exc)
        raise HTTPException(status_code=500, detail=f"大纲生成失败: {str(exc)}")

    return await _load_project_schema(novel_service, project_id, current_user.id)


@router.post("/novels/{project_id}/chapters/edit", response_model=NovelProjectSchema)
async def edit_chapter_content(
    project_id: str,
    request: EditChapterRequest,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> NovelProjectSchema:
    novel_service = NovelService(session)
    llm_service = LLMService(session)
    
    await novel_service.ensure_project_owner(project_id, current_user.id)
    chapter = await novel_service.get_or_create_chapter(project_id, request.chapter_number)
    
    # 更新内容
    chapter.content = request.content
    
    # 重新生成摘要
    try:
        summary = await llm_service.get_summary(
            request.content,
            temperature=0.15,
            user_id=current_user.id,
        )
        chapter.real_summary = remove_think_tags(summary)
    except Exception as e:
        logger.warning(f"编辑章节后自动生成摘要失败: {e}")
    
    chapter.status = "successful"
    await session.commit()
    
    # 异步触发向量化入库
    try:
        llm_service = LLMService(session)
        ingest_service = ChapterIngestionService(llm_service=llm_service)
        await ingest_service.ingest_chapter(
            project_id=project_id,
            chapter_number=request.chapter_number,
            title=chapter.title or f"第{request.chapter_number}章",
            content=request.content,
            summary=None
        )
        logger.info(f"章节 {request.chapter_number} 向量化入库成功")
    except Exception as e:
        logger.error(f"章节 {request.chapter_number} 向量化入库失败: {e}")
        # 向量化失败不应阻止内容编辑，仅记录错误
    
    return await _load_project_schema(novel_service, project_id, current_user.id)
