# AIMETA P=伏笔服务_伏笔管理业务逻辑|R=伏笔CRUD_回收追踪|NR=不含自动分析|E=ForeshadowingService|X=internal|A=服务类|D=sqlalchemy|S=db|RD=./README.ai
"""伏笔管理服务"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.foreshadowing import (
    Foreshadowing,
    ForeshadowingResolution,
    ForeshadowingReminder,
    ForeshadowingAnalysis,
)
from ..models.novel import Chapter, NovelProject

logger = logging.getLogger(__name__)


class ForeshadowingService:
    """伏笔管理服务"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_foreshadowing(
        self,
        project_id: str,
        chapter_id: int,
        chapter_number: int,
        content: str,
        foreshadowing_type: str,
        keywords: Optional[List[str]] = None,
        author_note: Optional[str] = None,
        is_manual: bool = True,
        ai_confidence: Optional[float] = None,
    ) -> Foreshadowing:
        """创建伏笔"""
        foreshadowing = Foreshadowing(
            project_id=project_id,
            chapter_id=chapter_id,
            chapter_number=chapter_number,
            content=content,
            type=foreshadowing_type,
            keywords=keywords or [],
            author_note=author_note,
            is_manual=is_manual,
            ai_confidence=ai_confidence,
        )
        self.session.add(foreshadowing)
        await self.session.flush()
        logger.info(f"创建伏笔: project={project_id}, chapter={chapter_number}, type={foreshadowing_type}")
        return foreshadowing
    
    async def get_foreshadowings(
        self,
        project_id: str,
        status: Optional[str] = None,
        foreshadowing_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[List[Foreshadowing], int]:
        """获取伏笔列表"""
        query = select(Foreshadowing).where(Foreshadowing.project_id == project_id)
        
        if status:
            query = query.where(Foreshadowing.status == status)
        if foreshadowing_type:
            query = query.where(Foreshadowing.type == foreshadowing_type)
        
        # 获取总数
        count_query = select(func.count()).select_from(Foreshadowing).where(Foreshadowing.project_id == project_id)
        if status:
            count_query = count_query.where(Foreshadowing.status == status)
        if foreshadowing_type:
            count_query = count_query.where(Foreshadowing.type == foreshadowing_type)
        
        total = await self.session.scalar(count_query)
        
        # 分页
        query = query.order_by(Foreshadowing.chapter_number).limit(limit).offset(offset)
        result = await self.session.execute(query)
        foreshadowings = result.scalars().all()
        
        return foreshadowings, total
    
    async def resolve_foreshadowing(
        self,
        foreshadowing_id: int,
        resolved_chapter_id: int,
        resolved_chapter_number: int,
        resolution_text: str,
        resolution_type: str = "direct",
        quality_score: Optional[int] = None,
    ) -> ForeshadowingResolution:
        """标记伏笔回收"""
        # 更新伏笔状态
        foreshadowing = await self.session.get(Foreshadowing, foreshadowing_id)
        if not foreshadowing:
            raise ValueError(f"伏笔不存在: {foreshadowing_id}")
        
        foreshadowing.status = "resolved"
        foreshadowing.resolved_chapter_id = resolved_chapter_id
        foreshadowing.resolved_chapter_number = resolved_chapter_number
        
        # 创建回收记录
        resolution = ForeshadowingResolution(
            foreshadowing_id=foreshadowing_id,
            resolved_at_chapter_id=resolved_chapter_id,
            resolved_at_chapter_number=resolved_chapter_number,
            resolution_text=resolution_text,
            resolution_type=resolution_type,
            quality_score=quality_score,
        )
        self.session.add(resolution)
        await self.session.flush()
        
        logger.info(f"标记伏笔回收: foreshadowing={foreshadowing_id}, chapter={resolved_chapter_number}")
        return resolution
    
    async def abandon_foreshadowing(
        self,
        foreshadowing_id: int,
        reason: Optional[str] = None,
    ) -> Foreshadowing:
        """放弃伏笔"""
        foreshadowing = await self.session.get(Foreshadowing, foreshadowing_id)
        if not foreshadowing:
            raise ValueError(f"伏笔不存在: {foreshadowing_id}")
        
        foreshadowing.status = "abandoned"
        if reason:
            foreshadowing.author_note = f"{foreshadowing.author_note or ''}\n[放弃原因]: {reason}".strip()
        
        await self.session.flush()
        logger.info(f"放弃伏笔: foreshadowing={foreshadowing_id}")
        return foreshadowing
    
    async def get_unresolved_foreshadowings(
        self,
        project_id: str,
        current_chapter_number: int,
    ) -> List[Foreshadowing]:
        """获取未回收的伏笔"""
        query = select(Foreshadowing).where(
            and_(
                Foreshadowing.project_id == project_id,
                Foreshadowing.status == "open",
            )
        ).order_by(Foreshadowing.chapter_number)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create_reminder(
        self,
        project_id: str,
        foreshadowing_id: int,
        reminder_type: str,
        message: str,
        suggested_chapter_range: Optional[Dict[str, int]] = None,
    ) -> ForeshadowingReminder:
        """创建提醒"""
        reminder = ForeshadowingReminder(
            project_id=project_id,
            foreshadowing_id=foreshadowing_id,
            reminder_type=reminder_type,
            message=message,
            suggested_chapter_range=suggested_chapter_range,
        )
        self.session.add(reminder)
        await self.session.flush()
        logger.info(f"创建提醒: foreshadowing={foreshadowing_id}, type={reminder_type}")
        return reminder
    
    async def get_active_reminders(
        self,
        project_id: str,
        limit: int = 50,
    ) -> List[ForeshadowingReminder]:
        """获取活跃提醒"""
        query = select(ForeshadowingReminder).where(
            and_(
                ForeshadowingReminder.project_id == project_id,
                ForeshadowingReminder.status == "active",
            )
        ).order_by(ForeshadowingReminder.created_at.desc()).limit(limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def dismiss_reminder(
        self,
        reminder_id: int,
        reason: Optional[str] = None,
    ) -> ForeshadowingReminder:
        """忽略提醒"""
        reminder = await self.session.get(ForeshadowingReminder, reminder_id)
        if not reminder:
            raise ValueError(f"提醒不存在: {reminder_id}")
        
        reminder.status = "dismissed"
        reminder.dismissed_at = datetime.utcnow()
        reminder.dismissed_reason = reason
        
        await self.session.flush()
        logger.info(f"忽略提醒: reminder={reminder_id}")
        return reminder
    
    async def analyze_foreshadowings(
        self,
        project_id: str,
    ) -> ForeshadowingAnalysis:
        """分析伏笔统计"""
        # 获取所有伏笔
        query = select(Foreshadowing).where(Foreshadowing.project_id == project_id)
        result = await self.session.execute(query)
        foreshadowings = result.scalars().all()
        
        # 统计
        total = len(foreshadowings)
        resolved_count = sum(1 for f in foreshadowings if f.status == "resolved")
        unresolved_count = sum(1 for f in foreshadowings if f.status == "open")
        abandoned_count = sum(1 for f in foreshadowings if f.status == "abandoned")
        
        # 计算平均回收距离
        resolution_distances = []
        for f in foreshadowings:
            if f.status == "resolved" and f.resolved_chapter_number:
                distance = f.resolved_chapter_number - f.chapter_number
                resolution_distances.append(distance)
        
        avg_resolution_distance = (
            sum(resolution_distances) / len(resolution_distances)
            if resolution_distances
            else 0
        )
        
        # 计算未回收比例
        unresolved_ratio = unresolved_count / total if total > 0 else 0
        
        # 模式分析
        type_distribution = {}
        for f in foreshadowings:
            type_distribution[f.type] = type_distribution.get(f.type, 0) + 1
        
        # 质量评分
        quality_scores = []
        for f in foreshadowings:
            if f.resolutions:
                for resolution in f.resolutions:
                    if resolution.quality_score:
                        quality_scores.append(resolution.quality_score)
        
        overall_quality_score = (
            sum(quality_scores) / len(quality_scores)
            if quality_scores
            else None
        )
        
        # 生成建议
        recommendations = []
        if unresolved_ratio > 0.3:
            recommendations.append(f"有 {unresolved_count} 个伏笔未回收，建议在后续章节中处理")
        if avg_resolution_distance > 15:
            recommendations.append("伏笔回收距离较长，可能影响读者记忆，建议缩短回收周期")
        if overall_quality_score and overall_quality_score < 6:
            recommendations.append("伏笔回收质量评分较低，建议改进回收方式")
        
        # 更新或创建分析记录
        analysis = await self.session.get(ForeshadowingAnalysis, project_id)
        if not analysis:
            analysis = ForeshadowingAnalysis(project_id=project_id)
            self.session.add(analysis)
        
        analysis.total_foreshadowings = total
        analysis.resolved_count = resolved_count
        analysis.unresolved_count = unresolved_count
        analysis.abandoned_count = abandoned_count
        analysis.avg_resolution_distance = avg_resolution_distance
        analysis.unresolved_ratio = unresolved_ratio
        analysis.pattern_analysis = type_distribution
        analysis.overall_quality_score = overall_quality_score
        analysis.recommendations = recommendations
        analysis.analyzed_at = datetime.utcnow()
        
        await self.session.flush()
        logger.info(f"分析伏笔: project={project_id}, total={total}, resolved={resolved_count}")
        return analysis
    
    async def check_and_create_reminders(
        self,
        project_id: str,
        current_chapter_number: int,
        total_chapters: int,
    ) -> List[ForeshadowingReminder]:
        """检查并创建提醒"""
        reminders = []
        
        # 获取未回收的伏笔
        unresolved = await self.get_unresolved_foreshadowings(project_id, current_chapter_number)
        
        for foreshadowing in unresolved:
            # 检查是否已有活跃提醒
            existing_query = select(ForeshadowingReminder).where(
                and_(
                    ForeshadowingReminder.foreshadowing_id == foreshadowing.id,
                    ForeshadowingReminder.status == "active",
                )
            )
            existing = await self.session.scalar(existing_query)
            if existing:
                continue
            
            # 长期未提及提醒
            distance = current_chapter_number - foreshadowing.chapter_number
            if distance > 10:
                reminder = await self.create_reminder(
                    project_id=project_id,
                    foreshadowing_id=foreshadowing.id,
                    reminder_type="long_time_no_mention",
                    message=f"第 {foreshadowing.chapter_number} 章埋下的伏笔已有 {distance} 章未提及，是否打算在后续章节中解答？",
                    suggested_chapter_range={
                        "start": current_chapter_number + 1,
                        "end": min(current_chapter_number + 5, total_chapters),
                    },
                )
                reminders.append(reminder)
            
            # 接近结局提醒
            if current_chapter_number > total_chapters * 0.8:
                reminder = await self.create_reminder(
                    project_id=project_id,
                    foreshadowing_id=foreshadowing.id,
                    reminder_type="unresolved",
                    message=f"小说即将结束，第 {foreshadowing.chapter_number} 章的伏笔仍未回收",
                )
                reminders.append(reminder)
        
        return reminders
