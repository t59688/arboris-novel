# AIMETA P=系统配置模型_全局配置存储|R=系统配置表|NR=不含配置逻辑|E=SystemConfig|X=internal|A=ORM模型|D=sqlalchemy|S=none|RD=./README.ai
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class SystemConfig(Base):
    """系统级配置项，例如默认 LLM API Key、模型名称等。"""

    __tablename__ = "system_configs"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
