# AIMETA P=用户日请求模型_每日请求限制|R=日请求统计表|NR=不含限制逻辑|E=UserDailyRequest|X=internal|A=ORM模型|D=sqlalchemy|S=none|RD=./README.ai
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class UserDailyRequest(Base):
    """记录每位用户每日使用次数的限流表。"""

    __tablename__ = "user_daily_requests"
    __table_args__ = (UniqueConstraint("user_id", "request_date", name="uq_user_daily"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    request_date: Mapped[date] = mapped_column(Date, nullable=False)
    request_count: Mapped[int] = mapped_column(Integer, default=0)
