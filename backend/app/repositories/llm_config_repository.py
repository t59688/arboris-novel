# AIMETA P=LLM配置仓库_配置数据访问|R=配置CRUD|NR=不含业务逻辑|E=LLMConfigRepository|X=internal|A=仓库类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Optional

from sqlalchemy import select

from .base import BaseRepository
from ..models import LLMConfig


class LLMConfigRepository(BaseRepository[LLMConfig]):
    model = LLMConfig

    async def get_by_user(self, user_id: int) -> Optional[LLMConfig]:
        result = await self.session.execute(select(LLMConfig).where(LLMConfig.user_id == user_id))
        return result.scalars().first()
