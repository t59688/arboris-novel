# AIMETA P=管理员设置模型_系统配置存储|R=键值对配置表|NR=不含配置逻辑|E=AdminSetting|X=internal|A=ORM模型|D=sqlalchemy|S=none|RD=./README.ai
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class AdminSetting(Base):
    """后台配置项，采用简单的 KV 结构。"""

    __tablename__ = "admin_settings"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
