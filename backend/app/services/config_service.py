# AIMETA P=配置服务_系统配置业务逻辑|R=配置读写|NR=不含数据访问|E=ConfigService|X=internal|A=服务类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Iterable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.system_config_repository import SystemConfigRepository
from ..models import SystemConfig
from ..schemas.config import SystemConfigCreate, SystemConfigRead, SystemConfigUpdate


class ConfigService:
    """系统配置服务：提供 CRUD 接口，并负责转换 Pydantic 模型。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SystemConfigRepository(session)

    async def list_configs(self) -> list[SystemConfigRead]:
        configs = await self.repo.list_all()
        return [SystemConfigRead.model_validate(cfg) for cfg in configs]

    async def get_config(self, key: str) -> Optional[SystemConfigRead]:
        config = await self.repo.get_by_key(key)
        return SystemConfigRead.model_validate(config) if config else None

    async def upsert_config(self, payload: SystemConfigCreate) -> SystemConfigRead:
        instance = await self.repo.get_by_key(payload.key)
        if instance:
            await self.repo.update_fields(instance, value=payload.value, description=payload.description)
        else:
            instance = SystemConfig(**payload.model_dump())
            await self.repo.add(instance)
        await self.session.commit()
        return SystemConfigRead.model_validate(instance)

    async def patch_config(self, key: str, payload: SystemConfigUpdate) -> Optional[SystemConfigRead]:
        instance = await self.repo.get_by_key(key)
        if not instance:
            return None
        await self.repo.update_fields(instance, **payload.model_dump(exclude_unset=True))
        await self.session.commit()
        return SystemConfigRead.model_validate(instance)

    async def remove_config(self, key: str) -> bool:
        instance = await self.repo.get_by_key(key)
        if not instance:
            return False
        await self.repo.delete(instance)
        await self.session.commit()
        return True
