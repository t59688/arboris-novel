# AIMETA P=管理员设置仓库_设置数据访问|R=设置CRUD|NR=不含业务逻辑|E=AdminSettingRepository|X=internal|A=仓库类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Optional

from sqlalchemy import select

from .base import BaseRepository
from ..models import AdminSetting


class AdminSettingRepository(BaseRepository[AdminSetting]):
    model = AdminSetting

    async def get_value(self, key: str) -> Optional[str]:
        result = await self.session.execute(select(AdminSetting).where(AdminSetting.key == key))
        record = result.scalars().first()
        return record.value if record else None
