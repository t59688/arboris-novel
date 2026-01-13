# AIMETA P=情感服务_情感曲线分析|R=情感分析_曲线生成|NR=不含内容生成|E=EmotionService|X=internal|A=服务类|D=redis|S=db,cache|RD=./README.ai
import hashlib
import logging
from typing import List, Dict, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.novel import Chapter, ChapterVersion, ChapterOutline
from app.utils.emotion_analyzer import analyze_emotion, detect_narrative_phase, generate_emotion_description

logger = logging.getLogger(__name__)

class EmotionService:
    """情感分析服务"""
    
    def __init__(self, session: AsyncSession = None):
        self.session = session
    
    @staticmethod
    def get_chapter_hash(content: str) -> str:
        """计算章节内容的哈希值"""
        return hashlib.md5(content.encode()).hexdigest()
    
    async def check_if_needs_update(
        self, 
        novel_id: str, 
        cache_service
    ) -> Tuple[bool, List[str]]:
        """检查是否需要更新情感分析"""
        # 获取缓存的元数据
        meta = cache_service.get_emotion_meta(novel_id)
        if not meta:
            logger.info(f"没有缓存元数据，需要完整分析: {novel_id}")
            return True, []  # 没有缓存，需要完整分析
        
        # 获取当前所有章节
        chapters = await self.get_all_chapters(novel_id)
        
        # 对比哈希值
        changed_chapters = []
        cached_hashes = meta.get('chapter_hashes', {})
        
        for chapter in chapters:
            content = await self.get_chapter_content(chapter.id)
            if not content:
                continue
            
            current_hash = self.get_chapter_hash(content)
            cached_hash = cached_hashes.get(str(chapter.id))
            
            if current_hash != cached_hash:
                changed_chapters.append(str(chapter.id))
        
        if changed_chapters:
            logger.info(f"检测到 {len(changed_chapters)} 个章节有变化: {novel_id}")
            return True, changed_chapters
        
        logger.info(f"没有检测到变化: {novel_id}")
        return False, []
    
    async def get_all_chapters(self, novel_id: str) -> List[Chapter]:
        """获取所有章节"""
        if not self.session:
            return []
        
        try:
            result = await self.session.execute(
                select(Chapter).where(Chapter.project_id == novel_id).order_by(Chapter.chapter_number)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"获取章节失败: {e}")
            return []
    
    async def get_chapter_content(self, chapter_id: str) -> str:
        """获取章节内容"""
        if not self.session:
            return ""
        
        try:
            result = await self.session.execute(
                select(Chapter).where(Chapter.id == chapter_id)
            )
            chapter = result.scalar_one_or_none()
            if not chapter or not chapter.selected_version_id:
                return ""
            
            version_result = await self.session.execute(
                select(ChapterVersion).where(ChapterVersion.id == chapter.selected_version_id)
            )
            version = version_result.scalar_one_or_none()
            return version.content if version else ""
        except Exception as e:
            logger.error(f"获取章节内容失败: {e}")
            return ""
    
    async def analyze_novel_emotion(
        self, 
        novel_id: str, 
        chapter_ids: List[str] = None
    ) -> Dict:
        """分析小说的情感曲线"""
        # 1. 获取所有章节
        chapters = await self.get_all_chapters(novel_id)
        if not chapters:
            logger.warning(f"项目没有章节: {novel_id}")
            return {
                'project_id': novel_id,
                'emotion_points': [],
                'average_intensity': 0,
                'emotion_distribution': {},
                'analyzed_at': None,
            }
        
        # 2. 获取所有大纲
        try:
            result = await self.session.execute(
                select(ChapterOutline).where(ChapterOutline.project_id == novel_id)
            )
            outlines = {o.chapter_number: o for o in result.scalars().all()}
        except Exception as e:
            logger.warning(f"获取大纲失败: {e}")
            outlines = {}
        
        # 3. 分析情感
        emotion_points = []
        emotion_counts = {}
        total_intensity = 0
        chapter_hashes = {}
        
        for chapter in chapters:
            # 如果指定了章节列表，跳过未指定的章节
            if chapter_ids and str(chapter.id) not in chapter_ids:
                continue
            
            content = await self.get_chapter_content(chapter.id)
            if not content:
                continue
            
            # 计算哈希值
            chapter_hash = self.get_chapter_hash(content)
            chapter_hashes[str(chapter.id)] = chapter_hash
            
            # 获取大纲
            outline = outlines.get(chapter.chapter_number)
            title = outline.title if outline else f"第{chapter.chapter_number}章"
            summary = outline.summary if outline else ""
            
            # 分析情感
            emotion, intensity = analyze_emotion(content + " " + summary)
            narrative_phase = detect_narrative_phase(content, summary)
            description = generate_emotion_description(emotion, intensity, title)
            
            emotion_points.append({
                'chapter_number': chapter.chapter_number,
                'chapter_id': str(chapter.id),
                'title': title,
                'emotion_type': emotion,
                'intensity': intensity,
                'narrative_phase': narrative_phase,
                'description': description,
            })
            
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            total_intensity += intensity
        
        # 4. 计算平均强度
        avg_intensity = total_intensity / len(emotion_points) if emotion_points else 0
        
        # 5. 返回结果
        from datetime import datetime
        return {
            'project_id': novel_id,
            'emotion_points': emotion_points,
            'average_intensity': round(avg_intensity, 2),
            'emotion_distribution': emotion_counts,
            'analyzed_at': datetime.now().isoformat(),
            'chapter_hashes': chapter_hashes,
        }
