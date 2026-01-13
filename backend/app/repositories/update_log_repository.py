# AIMETA P=更新日志仓库_日志数据访问|R=日志CRUD|NR=不含业务逻辑|E=UpdateLogRepository|X=internal|A=仓库类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Iterable

from sqlalchemy import select

from .base import BaseRepository
from ..models import UpdateLog


class UpdateLogRepository(BaseRepository[UpdateLog]):
    model = UpdateLog

    async def list(self) -> Iterable[UpdateLog]:
        result = await self.session.execute(select(UpdateLog).order_by(UpdateLog.created_at.desc()))
        return result.scalars().all()

    async def list_latest(self, limit: int = 5) -> Iterable[UpdateLog]:
        stmt = select(UpdateLog).order_by(UpdateLog.created_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
