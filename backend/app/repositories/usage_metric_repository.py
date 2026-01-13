# AIMETA P=使用指标仓库_指标数据访问|R=指标CRUD|NR=不含业务逻辑|E=UsageMetricRepository|X=internal|A=仓库类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Optional

from sqlalchemy import select

from .base import BaseRepository
from ..models import UsageMetric


class UsageMetricRepository(BaseRepository[UsageMetric]):
    model = UsageMetric

    async def get_or_create(self, key: str) -> UsageMetric:
        result = await self.session.execute(select(UsageMetric).where(UsageMetric.key == key))
        instance = result.scalars().first()
        if instance is None:
            instance = UsageMetric(key=key, value=0)
            self.session.add(instance)
            await self.session.flush()
        return instance
