# AIMETA P=伏笔模型_伏笔和回收追踪|R=伏笔表_回收表_提醒表_分析表|NR=不含业务逻辑|E=Foreshadowing_ForeshadowingResolution|X=internal|A=ORM模型|D=sqlalchemy|S=none|RD=./README.ai
"""伏笔管理数据模型"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, BigInteger, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base

# 自定义列类型：兼容跨数据库环境
BIGINT_PK_TYPE = BigInteger().with_variant(Integer, "sqlite")
LONG_TEXT_TYPE = Text().with_variant(LONGTEXT, "mysql")


class Foreshadowing(Base):
    """伏笔主表 - 存储小说中的伏笔信息"""
    
    __tablename__ = "foreshadowings"
    
    id: Mapped[int] = mapped_column(BIGINT_PK_TYPE, primary_key=True, autoincrement=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("novel_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # 伏笔内容
    content: Mapped[str] = mapped_column(LONG_TEXT_TYPE, nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False)  # question, mystery, hint, clue, setup
    keywords: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    
    # 伏笔状态
    status: Mapped[str] = mapped_column(String(32), default="open", index=True)  # open, resolved, abandoned
    resolved_chapter_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chapters.id", ondelete="SET NULL"))
    resolved_chapter_number: Mapped[Optional[int]] = mapped_column(Integer)
    
    # 元数据
    is_manual: Mapped[bool] = mapped_column(default=False)
    ai_confidence: Mapped[Optional[float]] = mapped_column(Float)
    author_note: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    chapter: Mapped["Chapter"] = relationship("Chapter", foreign_keys=[chapter_id])
    resolved_chapter: Mapped[Optional["Chapter"]] = relationship("Chapter", foreign_keys=[resolved_chapter_id])
    resolutions: Mapped[list["ForeshadowingResolution"]] = relationship(
        back_populates="foreshadowing", cascade="all, delete-orphan"
    )
    reminders: Mapped[list["ForeshadowingReminder"]] = relationship(
        back_populates="foreshadowing", cascade="all, delete-orphan"
    )


class ForeshadowingResolution(Base):
    """伏笔回收记录 - 记录伏笔如何被回收"""
    
    __tablename__ = "foreshadowing_resolutions"
    
    id: Mapped[int] = mapped_column(BIGINT_PK_TYPE, primary_key=True, autoincrement=True)
    foreshadowing_id: Mapped[int] = mapped_column(ForeignKey("foreshadowings.id", ondelete="CASCADE"), nullable=False)
    
    # 回收信息
    resolved_at_chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    resolved_at_chapter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    resolution_text: Mapped[str] = mapped_column(LONG_TEXT_TYPE, nullable=False)
    resolution_type: Mapped[Optional[str]] = mapped_column(String(32))  # direct, twist, delayed, etc.
    
    # 评估
    quality_score: Mapped[Optional[int]] = mapped_column(Integer)  # 1-10
    reader_satisfaction: Mapped[Optional[int]] = mapped_column(Integer)  # 1-10
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    foreshadowing: Mapped[Foreshadowing] = relationship(back_populates="resolutions")
    resolved_chapter: Mapped["Chapter"] = relationship("Chapter", foreign_keys=[resolved_at_chapter_id])


class ForeshadowingReminder(Base):
    """伏笔提醒 - 提醒作者处理未回收的伏笔"""
    
    __tablename__ = "foreshadowing_reminders"
    
    id: Mapped[int] = mapped_column(BIGINT_PK_TYPE, primary_key=True, autoincrement=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("novel_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    foreshadowing_id: Mapped[int] = mapped_column(ForeignKey("foreshadowings.id", ondelete="CASCADE"), nullable=False)
    
    # 提醒信息
    reminder_type: Mapped[str] = mapped_column(String(32), nullable=False)  # unresolved, long_time_no_mention, pattern_mismatch
    message: Mapped[str] = mapped_column(LONG_TEXT_TYPE, nullable=False)
    suggested_chapter_range: Mapped[Optional[dict]] = mapped_column(JSON)  # {"start": 10, "end": 20}
    
    # 状态
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)  # active, dismissed, resolved
    dismissed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    dismissed_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    foreshadowing: Mapped[Foreshadowing] = relationship(back_populates="reminders")


class ForeshadowingAnalysis(Base):
    """伏笔分析结果 - 存储伏笔分析的统计数据"""
    
    __tablename__ = "foreshadowing_analysis"
    
    id: Mapped[int] = mapped_column(BIGINT_PK_TYPE, primary_key=True, autoincrement=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("novel_projects.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # 分析结果
    total_foreshadowings: Mapped[int] = mapped_column(Integer, default=0)
    resolved_count: Mapped[int] = mapped_column(Integer, default=0)
    unresolved_count: Mapped[int] = mapped_column(Integer, default=0)
    abandoned_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # 统计数据
    avg_resolution_distance: Mapped[Optional[float]] = mapped_column(Float)
    unresolved_ratio: Mapped[Optional[float]] = mapped_column(Float)
    pattern_analysis: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # 质量评估
    overall_quality_score: Mapped[Optional[float]] = mapped_column(Float)
    recommendations: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# 为了避免循环导入，这些关系在 novel.py 中定义
# 需要在 novel.py 的 NovelProject 中添加：
# foreshadowings: Mapped[list["Foreshadowing"]] = relationship(
#     back_populates="project", cascade="all, delete-orphan", order_by="Foreshadowing.chapter_number"
# )
