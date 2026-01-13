# AIMETA P=提示词仓库_提示模板数据访问|R=提示词CRUD|NR=不含业务逻辑|E=PromptRepository|X=internal|A=仓库类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..models import Prompt


class PromptRepository(BaseRepository[Prompt]):
    model = Prompt

    async def get_by_name(self, name: str) -> Optional[Prompt]:
        result = await self.session.execute(select(Prompt).where(Prompt.name == name))
        return result.scalars().first()

    async def list_all(self) -> Iterable[Prompt]:
        result = await self.session.execute(select(Prompt).order_by(Prompt.name))
        return result.scalars().all()
