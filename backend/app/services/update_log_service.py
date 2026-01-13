# AIMETA P=更新日志服务_日志业务逻辑|R=日志CRUD|NR=不含数据访问|E=UpdateLogService|X=internal|A=服务类|D=sqlalchemy|S=db|RD=./README.ai
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UpdateLog
from ..repositories.update_log_repository import UpdateLogRepository


class UpdateLogService:
    """更新日志服务，提供增删改查能力，并保证置顶唯一。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UpdateLogRepository(session)

    async def list_logs(self, limit: Optional[int] = None) -> List[UpdateLog]:
        if limit is None:
            return list(await self.repo.list())
        return list(await self.repo.list_latest(limit))

    async def create_log(self, content: str, creator: str | None = None, *, is_pinned: bool = False) -> UpdateLog:
        if is_pinned:
            await self._clear_pinned()
        log = UpdateLog(content=content, created_by=creator, is_pinned=is_pinned)
        await self.repo.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def update_log(self, log_id: int, *, content: Optional[str] = None, is_pinned: Optional[bool] = None) -> UpdateLog:
        log = await self.repo.get(id=log_id)
        if not log:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新记录不存在")

        updates = {}
        if content is not None:
            updates["content"] = content
        if is_pinned is not None:
            if is_pinned:
                await self._clear_pinned()
            updates["is_pinned"] = is_pinned

        if updates:
            await self.repo.update_fields(log, **updates)
            await self.session.commit()
            await self.session.refresh(log)

        return log

    async def delete_log(self, log_id: int) -> None:
        log = await self.repo.get(id=log_id)
        if not log:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新记录不存在")
        await self.repo.delete(log)
        await self.session.commit()

    async def _clear_pinned(self) -> None:
        await self.session.execute(update(UpdateLog).values(is_pinned=False))
