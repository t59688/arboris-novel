# AIMETA P=管理员设置服务_设置业务逻辑|R=设置读写_验证|NR=不含数据访问|E=AdminSettingService|X=internal|A=服务类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import AdminSetting
from ..repositories.admin_setting_repository import AdminSettingRepository


class AdminSettingService:
    """管理员配置项服务，提供简单的 KV 操作。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AdminSettingRepository(session)

    async def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        value = await self.repo.get_value(key)
        return value if value is not None else default

    async def set(self, key: str, value: str) -> None:
        record = await self.repo.get(key=key)
        if record:
            await self.repo.update_fields(record, value=value)
        else:
            setting = AdminSetting(key=key, value=value)
            await self.repo.add(setting)
        await self.session.commit()
