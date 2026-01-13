# AIMETA P=更新日志API_系统更新记录|R=更新日志查询|NR=不含日志修改|E=route:GET_/api/updates/*|X=http|A=日志查询|D=fastapi,sqlalchemy|S=db|RD=./README.ai
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.session import get_session
from ...schemas.admin import UpdateLogRead
from ...services.update_log_service import UpdateLogService

router = APIRouter(prefix="/api/updates", tags=["Updates"])


def get_update_log_service(session: AsyncSession = Depends(get_session)) -> UpdateLogService:
    return UpdateLogService(session)


@router.get("/latest", response_model=List[UpdateLogRead])
async def read_latest_updates(
    service: UpdateLogService = Depends(get_update_log_service),
) -> List[UpdateLogRead]:
    logs = await service.list_logs(limit=5)
    return [UpdateLogRead.model_validate(log) for log in logs]
