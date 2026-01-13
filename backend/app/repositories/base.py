# AIMETA P=仓库基类_通用CRUD方法|R=create_get_update_delete|NR=不含具体表操作|E=BaseRepository|X=internal|A=基类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Any, Generic, Iterable, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """通用仓储基类，封装常见的增删改查操作。"""

    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, **filters: Any) -> Optional[ModelType]:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self, *, filters: Optional[dict[str, Any]] = None) -> Iterable[ModelType]:
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)

    async def update_fields(self, instance: ModelType, **values: Any) -> ModelType:
        for key, value in values.items():
            if value is None:
                continue
            setattr(instance, key, value)
        await self.session.flush()
        return instance
