# AIMETA P=分析API_情感曲线和章节分析|R=情感分析_章节统计|NR=不含数据修改|E=route:GET_/api/analytics/*|X=http|A=情感分析_统计查询|D=fastapi,sqlalchemy|S=db,cache|RD=./README.ai
"""
情感曲线和伏笔追踪分析API
"""
import json
import logging
import re
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.dependencies import get_current_user
from ...db.session import get_session
from ...models.novel import Chapter, ChapterOutline, ChapterVersion, NovelProject
from ...schemas.user import UserInDB
from ...services.llm_service import LLMService
from ...services.prompt_service import PromptService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


# ==================== 数据模型 ====================

class EmotionPoint(BaseModel):
    """单个章节的情感数据点"""
    chapter_number: int
    title: str
    emotion_type: str  # 喜悦/悲伤/愤怒/恐惧/惊讶/平静
    intensity: int  # 1-10
    narrative_phase: Optional[str] = None  # 12341234循环中的阶段
    description: str  # 情感描述


class EmotionCurveResponse(BaseModel):
    """情感曲线响应"""
    project_id: str
    project_title: str
    total_chapters: int
    emotion_points: List[EmotionPoint]
    average_intensity: float
    emotion_distribution: dict  # 各情感类型的分布


class Foreshadowing(BaseModel):
    """单个伏笔"""
    id: str
    description: str
    planted_chapter: int
    planted_chapter_title: str
    expected_payoff_chapter: Optional[int] = None
    actual_payoff_chapter: Optional[int] = None
    status: str  # planted/paid_off/overdue
    importance: str  # short/medium/long


class ForeshadowingResponse(BaseModel):
    """伏笔追踪响应"""
    project_id: str
    project_title: str
    total_foreshadowings: int
    planted_count: int
    paid_off_count: int
    overdue_count: int
    foreshadowings: List[Foreshadowing]


# ==================== 情感分析 ====================

EMOTION_KEYWORDS = {
    "喜悦": ["开心", "高兴", "欣喜", "兴奋", "愉快", "欢乐", "幸福", "满足", "得意", "狂喜", "笑", "乐"],
    "悲伤": ["难过", "伤心", "悲痛", "哀伤", "忧郁", "沮丧", "失落", "绝望", "泪", "哭", "痛苦"],
    "愤怒": ["生气", "愤怒", "恼火", "暴怒", "怒火", "气愤", "恨", "咬牙", "握拳", "怒吼"],
    "恐惧": ["害怕", "恐惧", "惊恐", "担忧", "焦虑", "不安", "颤抖", "发抖", "心惊", "胆寒"],
    "惊讶": ["震惊", "惊讶", "意外", "诧异", "愕然", "目瞪口呆", "不敢相信", "难以置信"],
    "平静": ["平静", "安宁", "淡然", "从容", "镇定", "沉着", "安详", "宁静"],
}

NARRATIVE_PHASE_KEYWORDS = {
    "事件": ["突然", "意外", "发现", "出现", "打破", "离奇"],
    "势力": ["对立", "敌人", "对手", "势力", "阵营", "威胁"],
    "挑衅1": ["挑衅", "嘲讽", "侮辱", "轻视", "看不起"],
    "挑衅2": ["打击", "损失", "失去", "剥夺", "阻碍"],
    "挑衅3": ["绝境", "危机", "崩溃", "毁灭", "灭顶"],
    "回击1": ["反击", "回应", "证明", "小胜"],
    "回击2": ["扳回", "逆转", "反败为胜"],
    "回击3": ["胜利", "成功", "化解", "解决"],
    "回击4": ["揭露", "真相", "幕后", "黑手", "终极"],
}


def analyze_emotion(text: str) -> tuple[str, int]:
    """分析文本的主要情感和强度"""
    emotion_scores = {emotion: 0 for emotion in EMOTION_KEYWORDS}
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            count = text.count(keyword)
            emotion_scores[emotion] += count
    
    # 找出最高分的情感
    max_emotion = max(emotion_scores, key=emotion_scores.get)
    max_score = emotion_scores[max_emotion]
    
    if max_score == 0:
        return "平静", 3
    
    # 计算强度 (1-10)
    intensity = min(10, max(1, max_score))
    
    # 根据感叹号和问号增加强度
    exclamation_count = text.count("！") + text.count("!")
    question_count = text.count("？") + text.count("?")
    intensity = min(10, intensity + exclamation_count // 3 + question_count // 5)
    
    return max_emotion, intensity


def detect_narrative_phase(text: str, summary: str = "") -> Optional[str]:
    """检测叙事阶段"""
    combined_text = text + " " + summary
    phase_scores = {phase: 0 for phase in NARRATIVE_PHASE_KEYWORDS}
    
    for phase, keywords in NARRATIVE_PHASE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in combined_text:
                phase_scores[phase] += 1
    
    max_phase = max(phase_scores, key=phase_scores.get)
    if phase_scores[max_phase] > 0:
        return max_phase
    return None


def generate_emotion_description(emotion: str, intensity: int, title: str) -> str:
    """生成情感描述"""
    intensity_words = {
        (1, 3): "轻微的",
        (4, 6): "明显的",
        (7, 8): "强烈的",
        (9, 10): "极度的",
    }
    
    for (low, high), word in intensity_words.items():
        if low <= intensity <= high:
            return f"《{title}》呈现{word}{emotion}情绪"
    
    return f"《{title}》的情感基调为{emotion}"


# ==================== 伏笔分析 ====================

FORESHADOWING_PLANT_PATTERNS = [
    r"(?:似乎|好像|仿佛).*(?:隐藏|藏着|暗示)",
    r"(?:不知道|不清楚|不明白).*(?:为什么|原因)",
    r"(?:神秘|奇怪|诡异).*(?:人物|事件|现象)",
    r"(?:留下|埋下|种下).*(?:伏笔|悬念|谜团)",
    r"(?:日后|将来|以后).*(?:会|将)",
    r"(?:这件事|此事).*(?:蹊跷|古怪|不简单)",
]

FORESHADOWING_PAYOFF_PATTERNS = [
    r"(?:原来|原来如此|所以)",
    r"(?:真相|谜底|答案).*(?:揭开|揭晓|大白)",
    r"(?:终于|最终).*(?:明白|理解|知道)",
    r"(?:之前|当初|那时).*(?:原来|竟然)",
    r"(?:恍然大悟|豁然开朗)",
]


def extract_foreshadowings(chapters_data: list) -> List[Foreshadowing]:
    """从章节数据中提取伏笔"""
    foreshadowings = []
    planted_items = []  # 记录已埋设的伏笔
    
    for chapter in chapters_data:
        chapter_num = chapter["chapter_number"]
        title = chapter["title"]
        content = chapter.get("content", "")
        summary = chapter.get("summary", "")
        combined = content + " " + summary
        
        # 检测埋设的伏笔
        for i, pattern in enumerate(FORESHADOWING_PLANT_PATTERNS):
            matches = re.findall(pattern, combined)
            for match in matches:
                foreshadowing_id = f"fs_{chapter_num}_{i}_{len(planted_items)}"
                # 提取上下文作为描述
                context_match = re.search(f".{{0,20}}{re.escape(match)}.{{0,20}}", combined)
                description = context_match.group(0) if context_match else match
                
                planted_items.append({
                    "id": foreshadowing_id,
                    "description": description.strip(),
                    "planted_chapter": chapter_num,
                    "planted_chapter_title": title,
                    "importance": "short" if i < 2 else ("medium" if i < 4 else "long"),
                })
        
        # 检测回收的伏笔
        for pattern in FORESHADOWING_PAYOFF_PATTERNS:
            if re.search(pattern, combined):
                # 尝试匹配之前埋设的伏笔
                for planted in planted_items:
                    if planted.get("actual_payoff_chapter") is None:
                        # 简单匹配：如果当前章节提到了伏笔相关内容
                        if any(word in combined for word in planted["description"].split()[:3]):
                            planted["actual_payoff_chapter"] = chapter_num
                            break
    
    # 构建伏笔列表
    current_chapter = max(c["chapter_number"] for c in chapters_data) if chapters_data else 0
    
    for planted in planted_items:
        # 计算预期回收章节
        importance_offset = {"short": 2, "medium": 6, "long": 15}
        expected_payoff = planted["planted_chapter"] + importance_offset.get(planted["importance"], 5)
        
        # 确定状态
        if planted.get("actual_payoff_chapter"):
            status = "paid_off"
        elif current_chapter > expected_payoff:
            status = "overdue"
        else:
            status = "planted"
        
        foreshadowings.append(Foreshadowing(
            id=planted["id"],
            description=planted["description"],
            planted_chapter=planted["planted_chapter"],
            planted_chapter_title=planted["planted_chapter_title"],
            expected_payoff_chapter=expected_payoff,
            actual_payoff_chapter=planted.get("actual_payoff_chapter"),
            status=status,
            importance=planted["importance"],
        ))
    
    return foreshadowings


# ==================== API端点 ====================

@router.get("/{project_id}/emotion-curve", response_model=EmotionCurveResponse)
async def get_emotion_curve(
    project_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> EmotionCurveResponse:
    """获取小说的情感曲线数据"""
    
    # 获取项目
    result = await session.execute(
        select(NovelProject).where(
            NovelProject.id == project_id,
            NovelProject.user_id == current_user.id
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 获取所有章节和大纲
    chapters_result = await session.execute(
        select(Chapter).where(Chapter.project_id == project_id).order_by(Chapter.chapter_number)
    )
    chapters = chapters_result.scalars().all()
    
    outlines_result = await session.execute(
        select(ChapterOutline).where(ChapterOutline.project_id == project_id).order_by(ChapterOutline.chapter_number)
    )
    outlines = {o.chapter_number: o for o in outlines_result.scalars().all()}
    
    # 分析每个章节的情感
    emotion_points = []
    emotion_counts = {}
    total_intensity = 0
    
    for chapter in chapters:
        # 获取章节内容
        content = ""
        if chapter.selected_version_id:
            version_result = await session.execute(
                select(ChapterVersion).where(ChapterVersion.id == chapter.selected_version_id)
            )
            version = version_result.scalar_one_or_none()
            if version:
                content = version.content
        
        outline = outlines.get(chapter.chapter_number)
        title = outline.title if outline else f"第{chapter.chapter_number}章"
        summary = outline.summary if outline else ""
        
        # 分析情感
        emotion, intensity = analyze_emotion(content + " " + summary)
        narrative_phase = detect_narrative_phase(content, summary)
        description = generate_emotion_description(emotion, intensity, title)
        
        emotion_points.append(EmotionPoint(
            chapter_number=chapter.chapter_number,
            title=title,
            emotion_type=emotion,
            intensity=intensity,
            narrative_phase=narrative_phase,
            description=description,
        ))
        
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        total_intensity += intensity
    
    # 计算统计数据
    avg_intensity = total_intensity / len(chapters) if chapters else 0
    
    return EmotionCurveResponse(
        project_id=project_id,
        project_title=project.title,
        total_chapters=len(chapters),
        emotion_points=emotion_points,
        average_intensity=round(avg_intensity, 2),
        emotion_distribution=emotion_counts,
    )


@router.get("/{project_id}/foreshadowing", response_model=ForeshadowingResponse)
async def get_foreshadowing(
    project_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> ForeshadowingResponse:
    """获取小说的伏笔追踪数据"""
    
    # 获取项目
    result = await session.execute(
        select(NovelProject).where(
            NovelProject.id == project_id,
            NovelProject.user_id == current_user.id
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 获取所有章节和大纲
    chapters_result = await session.execute(
        select(Chapter).where(Chapter.project_id == project_id).order_by(Chapter.chapter_number)
    )
    chapters = chapters_result.scalars().all()
    
    outlines_result = await session.execute(
        select(ChapterOutline).where(ChapterOutline.project_id == project_id).order_by(ChapterOutline.chapter_number)
    )
    outlines = {o.chapter_number: o for o in outlines_result.scalars().all()}
    
    # 构建章节数据
    chapters_data = []
    for chapter in chapters:
        content = ""
        if chapter.selected_version_id:
            version_result = await session.execute(
                select(ChapterVersion).where(ChapterVersion.id == chapter.selected_version_id)
            )
            version = version_result.scalar_one_or_none()
            if version:
                content = version.content
        
        outline = outlines.get(chapter.chapter_number)
        
        chapters_data.append({
            "chapter_number": chapter.chapter_number,
            "title": outline.title if outline else f"第{chapter.chapter_number}章",
            "summary": outline.summary if outline else "",
            "content": content,
        })
    
    # 提取伏笔
    foreshadowings = extract_foreshadowings(chapters_data)
    
    # 统计
    planted_count = sum(1 for f in foreshadowings if f.status == "planted")
    paid_off_count = sum(1 for f in foreshadowings if f.status == "paid_off")
    overdue_count = sum(1 for f in foreshadowings if f.status == "overdue")
    
    return ForeshadowingResponse(
        project_id=project_id,
        project_title=project.title,
        total_foreshadowings=len(foreshadowings),
        planted_count=planted_count,
        paid_off_count=paid_off_count,
        overdue_count=overdue_count,
        foreshadowings=foreshadowings,
    )


@router.post("/{project_id}/analyze-emotion-ai")
async def analyze_emotion_with_ai(
    project_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(get_current_user),
) -> EmotionCurveResponse:
    """使用AI深度分析情感曲线（更准确但较慢）"""
    
    # 获取项目
    result = await session.execute(
        select(NovelProject).where(
            NovelProject.id == project_id,
            NovelProject.user_id == current_user.id
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 获取所有章节
    chapters_result = await session.execute(
        select(Chapter).where(Chapter.project_id == project_id).order_by(Chapter.chapter_number)
    )
    chapters = chapters_result.scalars().all()
    
    outlines_result = await session.execute(
        select(ChapterOutline).where(ChapterOutline.project_id == project_id).order_by(ChapterOutline.chapter_number)
    )
    outlines = {o.chapter_number: o for o in outlines_result.scalars().all()}
    
    # 构建章节摘要列表
    chapter_summaries = []
    for chapter in chapters:
        outline = outlines.get(chapter.chapter_number)
        if outline:
            chapter_summaries.append(f"第{chapter.chapter_number}章《{outline.title}》：{outline.summary}")
    
    if not chapter_summaries:
        raise HTTPException(status_code=400, detail="没有可分析的章节")
    
    # 使用AI分析
    llm_service = LLMService(session)
    
    prompt = f"""请分析以下小说章节的情感走向，为每个章节返回情感类型和强度。

章节列表：
{chr(10).join(chapter_summaries)}

请以JSON格式返回，格式如下：
{{
  "chapters": [
    {{
      "chapter_number": 1,
      "emotion_type": "喜悦/悲伤/愤怒/恐惧/惊讶/平静",
      "intensity": 1-10的数字,
      "narrative_phase": "事件/势力/挑衅1/挑衅2/挑衅3/回击1/回击2/回击3/回击4/过渡",
      "description": "简短的情感描述"
    }}
  ]
}}

只返回JSON，不要其他内容。"""

    try:
        response = await llm_service.get_llm_response(
            system_prompt="你是一个专业的小说情感分析师。",
            conversation_history=[{"role": "user", "content": prompt}],
            temperature=0.3,
            user_id=current_user.id
        )
        # 解析JSON
        import json
        from ...utils.json_utils import unwrap_markdown_json
        cleaned = unwrap_markdown_json(response)
        data = json.loads(cleaned)
        
        emotion_points = []
        emotion_counts = {}
        total_intensity = 0
        
        for item in data.get("chapters", []):
            outline = outlines.get(item["chapter_number"])
            title = outline.title if outline else f"第{item['chapter_number']}章"
            
            emotion_points.append(EmotionPoint(
                chapter_number=item["chapter_number"],
                title=title,
                emotion_type=item.get("emotion_type", "平静"),
                intensity=item.get("intensity", 5),
                narrative_phase=item.get("narrative_phase"),
                description=item.get("description", ""),
            ))
            
            emotion = item.get("emotion_type", "平静")
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            total_intensity += item.get("intensity", 5)
        
        avg_intensity = total_intensity / len(emotion_points) if emotion_points else 0
        
        return EmotionCurveResponse(
            project_id=project_id,
            project_title=project.title,
            total_chapters=len(emotion_points),
            emotion_points=emotion_points,
            average_intensity=round(avg_intensity, 2),
            emotion_distribution=emotion_counts,
        )
        
    except Exception as e:
        logger.error(f"AI情感分析失败: {e}")
        # 回退到关键词分析
        return await get_emotion_curve(project_id, session, current_user)
