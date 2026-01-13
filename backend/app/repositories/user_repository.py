# AIMETA P=用户仓库_用户数据访问|R=用户CRUD_认证查询|NR=不含业务逻辑|E=UserRepository|X=internal|A=仓库类|D=sqlalchemy|S=db|RD=./README.ai
from datetime import date
from typing import Iterable, Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..models import User, UserDailyRequest


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_external_id(self, external_id: str) -> Optional[User]:
        stmt = select(User).where(User.external_id == external_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_all(self) -> Iterable[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def increment_daily_request(self, user_id: int) -> None:
        today = date.today()
        stmt = select(UserDailyRequest).where(
            UserDailyRequest.user_id == user_id,
            UserDailyRequest.request_date == today,
        )
        result = await self.session.execute(stmt)
        record = result.scalars().first()

        if record is None:
            record = UserDailyRequest(user_id=user_id, request_date=today, request_count=1)
            self.session.add(record)
        else:
            record.request_count += 1
        await self.session.flush()

    async def get_daily_request(self, user_id: int) -> int:
        today = date.today()
        stmt = select(UserDailyRequest.request_count).where(
            UserDailyRequest.user_id == user_id,
            UserDailyRequest.request_date == today,
        )
        result = await self.session.execute(stmt)
        value = result.scalars().first()
        return value or 0

    async def count_users(self) -> int:
        stmt = select(func.count(User.id))
        result = await self.session.execute(stmt)
        return result.scalar_one()
