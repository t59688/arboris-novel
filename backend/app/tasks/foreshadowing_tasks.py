# AIMETA P=伏笔分析任务_异步伏笔检测|R=异步伏笔分析_提醒生成|NR=不含同步分析|E=celery_task:analyze_foreshadowing|X=job|A=Celery任务|D=celery,redis|S=db,cache|RD=./README.ai
"""伏笔管理异步任务"""
import logging
import re
from typing import List, Dict, Any
from app.config.celery_config import app
from app.services.foreshadowing_service import ForeshadowingService

logger = logging.getLogger(__name__)

# 伏笔检测规则
QUESTION_PATTERNS = [
    r"[？?]",  # 问号
    r"到底是谁",
    r"为什么",
    r"怎么样",
    r"是什么",
]

MYSTERY_KEYWORDS = [
    "神秘", "秘密", "隐藏", "真相", "身份", "来历",
    "目的", "意图", "阴谋", "计划", "真实",
]

CLUE_KEYWORDS = [
    "奇怪", "异常", "不寻常", "古怪", "诡异",
    "可疑", "怀疑", "疑惑", "困惑", "谜团",
]

SETUP_KEYWORDS = [
    "准备", "计划", "打算", "决定", "开始",
    "即将", "将要", "要去", "前往", "出发",
]


def detect_questions(text: str) -> List[str]:
    """检测问题型伏笔"""
    questions = []
    for pattern in QUESTION_PATTERNS:
        matches = re.finditer(pattern, text)
        for match in matches:
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text[start:end].strip()
            if context and context not in questions:
                questions.append(context)
    return questions[:5]  # 最多返回 5 个


def detect_mysteries(text: str) -> List[str]:
    """检测神秘型伏笔"""
    mysteries = []
    for keyword in MYSTERY_KEYWORDS:
        if keyword in text:
            # 找到关键词周围的上下文
            idx = text.find(keyword)
            start = max(0, idx - 40)
            end = min(len(text), idx + 40)
            context = text[start:end].strip()
            if context and context not in mysteries:
                mysteries.append(context)
    return mysteries[:5]


def detect_clues(text: str) -> List[str]:
    """检测线索型伏笔"""
    clues = []
    for keyword in CLUE_KEYWORDS:
        if keyword in text:
            idx = text.find(keyword)
            start = max(0, idx - 40)
            end = min(len(text), idx + 40)
            context = text[start:end].strip()
            if context and context not in clues:
                clues.append(context)
    return clues[:5]


def detect_setups(text: str) -> List[str]:
    """检测铺垫型伏笔"""
    setups = []
    for keyword in SETUP_KEYWORDS:
        if keyword in text:
            idx = text.find(keyword)
            start = max(0, idx - 40)
            end = min(len(text), idx + 40)
            context = text[start:end].strip()
            if context and context not in setups:
                setups.append(context)
    return setups[:5]


@app.task(bind=True, name='app.tasks.foreshadowing_tasks.detect_foreshadowings')
def detect_foreshadowings(
    self,
    novel_id: str,
    chapter_id: int,
    chapter_number: int,
    content: str,
):
    """
    异步检测章节中的伏笔
    
    Args:
        novel_id: 小说项目 ID
        chapter_id: 章节 ID
        chapter_number: 章节号
        content: 章节内容
    """
    try:
        logger.info(f"开始检测伏笔: novel={novel_id}, chapter={chapter_number}")
        
        # 更新任务状态
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 0,
                'total': 100,
                'status': '正在分析章节内容...'
            }
        )
        
        # 检测不同类型的伏笔
        detected_foreshadowings = []
        
        # 检测问题型伏笔
        questions = detect_questions(content)
        for q in questions:
            detected_foreshadowings.append({
                'type': 'question',
                'content': q,
                'confidence': 0.8,
            })
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 25, 'total': 100, 'status': '检测问题型伏笔...'}
        )
        
        # 检测神秘型伏笔
        mysteries = detect_mysteries(content)
        for m in mysteries:
            detected_foreshadowings.append({
                'type': 'mystery',
                'content': m,
                'confidence': 0.7,
            })
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 50, 'total': 100, 'status': '检测神秘型伏笔...'}
        )
        
        # 检测线索型伏笔
        clues = detect_clues(content)
        for c in clues:
            detected_foreshadowings.append({
                'type': 'clue',
                'content': c,
                'confidence': 0.6,
            })
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 75, 'total': 100, 'status': '检测线索型伏笔...'}
        )
        
        # 检测铺垫型伏笔
        setups = detect_setups(content)
        for s in setups:
            detected_foreshadowings.append({
                'type': 'setup',
                'content': s,
                'confidence': 0.65,
            })
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 100, 'total': 100, 'status': '分析完成'}
        )
        
        logger.info(f"检测到 {len(detected_foreshadowings)} 个伏笔: novel={novel_id}, chapter={chapter_number}")
        
        return {
            'status': 'success',
            'novel_id': novel_id,
            'chapter_number': chapter_number,
            'detected_count': len(detected_foreshadowings),
            'foreshadowings': detected_foreshadowings,
        }
    
    except Exception as exc:
        logger.exception(f"伏笔检测失败: {exc}")
        self.update_state(
            state='FAILURE',
            meta={'error': str(exc)}
        )
        raise


@app.task(bind=True, name='app.tasks.foreshadowing_tasks.check_reminders')
def check_reminders(
    self,
    novel_id: str,
    current_chapter_number: int,
    total_chapters: int,
):
    """
    检查并创建伏笔提醒
    
    Args:
        novel_id: 小说项目 ID
        current_chapter_number: 当前章节号
        total_chapters: 总章节数
    """
    try:
        logger.info(f"检查伏笔提醒: novel={novel_id}, chapter={current_chapter_number}/{total_chapters}")
        
        # 创建会话
        import asyncio
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from app.core.config import settings
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                _check_reminders_impl(novel_id, current_chapter_number, total_chapters)
            )
            logger.info(f"提醒检查完成: novel={novel_id}, reminders={result['reminders_created']}")
            return result
        finally:
            loop.close()
    
    except Exception as exc:
        logger.exception(f"提醒检查失败: {exc}")
        raise


async def _check_reminders_impl(
    novel_id: str,
    current_chapter_number: int,
    total_chapters: int,
):
    """提醒检查实现"""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from app.core.config import settings
    
    # 延迟创建数据库引擎
    engine = create_async_engine(settings.database_url, echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        try:
            service = ForeshadowingService(session)
            reminders = await service.check_and_create_reminders(
                project_id=novel_id,
                current_chapter_number=current_chapter_number,
                total_chapters=total_chapters,
            )
            await session.commit()
            
            return {
                'status': 'success',
                'novel_id': novel_id,
                'reminders_created': len(reminders),
            }
        
        except Exception as exc:
            logger.exception(f"提醒检查实现失败: {exc}")
            raise
        finally:
            await engine.dispose()
