# AIMETA P=情感分析任务_异步情感曲线计算|R=异步情感分析_缓存更新|NR=不含同步分析|E=celery_task:analyze_emotion|X=job|A=Celery任务|D=celery,redis|S=db,cache|RD=./README.ai
import logging
from typing import List, Optional
from app.config.celery_config import app
from app.services.emotion_service import EmotionService
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)

@app.task(bind=True, name='app.tasks.emotion_tasks.analyze_emotion_async')
def analyze_emotion_async(
    self,
    novel_id: str,
    chapter_ids: Optional[List[str]] = None
):
    """
    异步分析小说的情感曲线
    
    Args:
        novel_id: 小说项目 ID
        chapter_ids: 需要分析的章节 ID 列表，如果为空则分析所有章节
    """
    try:
        logger.info(f"开始异步分析情感曲线: novel_id={novel_id}, chapters={len(chapter_ids) if chapter_ids else 'all'}")
        
        # 更新任务状态
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 0,
                'total': len(chapter_ids) if chapter_ids else 0,
                'status': '初始化分析...'
            }
        )
        
        # 创建会话
        import asyncio
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from app.core.config import settings
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                _analyze_emotion_impl(novel_id, chapter_ids, self)
            )
            logger.info(f"情感曲线分析完成: novel_id={novel_id}")
            return result
        finally:
            loop.close()
    
    except Exception as exc:
        logger.exception(f"情感分析失败: {exc}")
        self.update_state(
            state='FAILURE',
            meta={'error': str(exc)}
        )
        raise

async def _analyze_emotion_impl(
    novel_id: str,
    chapter_ids: Optional[List[str]],
    task
):
    """异步分析实现"""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from app.core.config import settings
    
    # 延迟创建数据库引擎
    engine = create_async_engine(settings.database_url, echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        try:
            emotion_service = EmotionService(session)
            cache_service = CacheService()
            
            # 更新任务状态
            task.update_state(
                state='PROGRESS',
                meta={
                    'current': 0,
                    'total': 100,
                    'status': '正在分析情感...'
                }
            )
            
            # 分析情感
            emotion_data = await emotion_service.analyze_novel_emotion(novel_id, chapter_ids)
            
            # 更新任务状态
            task.update_state(
                state='PROGRESS',
                meta={
                    'current': 80,
                    'total': 100,
                    'status': '正在更新缓存...'
                }
            )
            
            # 更新缓存
            cache_service.set_emotion_curve(novel_id, emotion_data)
            
            # 更新元数据
            meta = {
                'last_analyzed': emotion_data['analyzed_at'],
                'total_chapters': len(emotion_data['emotion_points']),
                'chapter_hashes': emotion_data.get('chapter_hashes', {}),
            }
            cache_service.set_emotion_meta(novel_id, meta)
            
            # 更新任务状态为完成
            task.update_state(
                state='PROGRESS',
                meta={
                    'current': 100,
                    'total': 100,
                    'status': '分析完成'
                }
            )
            
            return {
                'status': 'success',
                'novel_id': novel_id,
                'chapters_analyzed': len(emotion_data['emotion_points']),
                'data': emotion_data
            }
        
        except Exception as exc:
            logger.exception(f"异步分析实现失败: {exc}")
            raise
        finally:
            await engine.dispose()
