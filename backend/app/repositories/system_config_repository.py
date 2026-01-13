# AIMETA P=系统配置仓库_配置数据访问|R=配置CRUD|NR=不含业务逻辑|E=SystemConfigRepository|X=internal|A=仓库类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Iterable, Optional

from sqlalchemy import select

from .base import BaseRepository
from ..models import SystemConfig


class SystemConfigRepository(BaseRepository[SystemConfig]):
    model = SystemConfig

    async def get_by_key(self, key: str) -> Optional[SystemConfig]:
        result = await self.session.execute(select(SystemConfig).where(SystemConfig.key == key))
        return result.scalars().first()

    async def list_all(self) -> Iterable[SystemConfig]:
        result = await self.session.execute(select(SystemConfig).order_by(SystemConfig.key))
        return result.scalars().all()
