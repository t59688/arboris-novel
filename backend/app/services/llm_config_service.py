# AIMETA P=LLM配置服务_模型配置业务逻辑|R=配置管理_模型选择|NR=不含模型调用|E=LLMConfigService|X=internal|A=服务类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import LLMConfig
from ..repositories.llm_config_repository import LLMConfigRepository
from ..schemas.llm_config import LLMConfigCreate, LLMConfigRead


class LLMConfigService:
    """用户自定义 LLM 配置服务。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = LLMConfigRepository(session)

    async def upsert_config(self, user_id: int, payload: LLMConfigCreate) -> LLMConfigRead:
        instance = await self.repo.get_by_user(user_id)
        data = payload.model_dump(exclude_unset=True)
        if "llm_provider_url" in data and data["llm_provider_url"] is not None:
            # HttpUrl 类型在 sqlite 中无法直接写入，需要提前转为字符串
            data["llm_provider_url"] = str(data["llm_provider_url"])
        if instance:
            await self.repo.update_fields(instance, **data)
        else:
            instance = LLMConfig(user_id=user_id, **data)
            await self.repo.add(instance)
        await self.session.commit()
        return LLMConfigRead.model_validate(instance)

    async def get_config(self, user_id: int) -> Optional[LLMConfigRead]:
        instance = await self.repo.get_by_user(user_id)
        return LLMConfigRead.model_validate(instance) if instance else None

    async def delete_config(self, user_id: int) -> bool:
        instance = await self.repo.get_by_user(user_id)
        if not instance:
            return False
        await self.repo.delete(instance)
        await self.session.commit()
        return True
