# AIMETA P=用户模型_用户账户定义|R=用户表|NR=不含用户逻辑|E=User|X=internal|A=ORM模型|D=sqlalchemy|S=none|RD=./README.ai
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class User(Base):
    """用户主表，记录账号及权限信息。"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(128), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # 关系映射
    novel_projects: Mapped[list["NovelProject"]] = relationship("NovelProject", back_populates="owner")
    llm_config: Mapped[Optional["LLMConfig"]] = relationship("LLMConfig", back_populates="user", uselist=False)
