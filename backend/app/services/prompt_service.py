# AIMETA P=提示词服务_提示模板管理|R=提示词加载_缓存|NR=不含内容生成|E=PromptService|X=internal|A=服务类|D=sqlalchemy|S=db,fs|RD=./README.ai
import asyncio
from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Prompt
from ..repositories.prompt_repository import PromptRepository
from ..schemas.prompt import PromptCreate, PromptRead, PromptUpdate

_CACHE: Dict[str, PromptRead] = {}
_LOCK = asyncio.Lock()
_LOADED = False


class PromptService:
    """提示词服务，提供缓存加速与 CRUD 能力。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PromptRepository(session)

    async def preload(self) -> None:
        global _CACHE, _LOADED
        prompts = await self.repo.list_all()
        async with _LOCK:
            _CACHE = {item.name: PromptRead.model_validate(item) for item in prompts}
            _LOADED = True

    async def get_prompt(self, name: str) -> Optional[str]:
        global _LOADED
        async with _LOCK:
            if not _LOADED:
                prompts = await self.repo.list_all()
                _CACHE.update({item.name: PromptRead.model_validate(item) for item in prompts})
                _LOADED = True
            cached = _CACHE.get(name)
        if cached:
            return cached.content

        prompt = await self.repo.get_by_name(name)
        if not prompt:
            return None

        prompt_read = PromptRead.model_validate(prompt)
        async with _LOCK:
            _CACHE[name] = prompt_read
        return prompt_read.content

    async def list_prompts(self) -> list[PromptRead]:
        prompts = await self.repo.list_all()
        return [PromptRead.model_validate(item) for item in prompts]

    async def get_prompt_by_id(self, prompt_id: int) -> Optional[PromptRead]:
        instance = await self.repo.get(id=prompt_id)
        if not instance:
            return None
        return PromptRead.model_validate(instance)

    async def create_prompt(self, payload: PromptCreate) -> PromptRead:
        data = payload.model_dump()
        tags = data.get("tags")
        if tags is not None:
            data["tags"] = ",".join(tags)
        prompt = Prompt(**data)
        await self.repo.add(prompt)
        await self.session.commit()
        prompt_read = PromptRead.model_validate(prompt)
        async with _LOCK:
            _CACHE[prompt_read.name] = prompt_read
            global _LOADED
            _LOADED = True
        return prompt_read

    async def update_prompt(self, prompt_id: int, payload: PromptUpdate) -> Optional[PromptRead]:
        instance = await self.repo.get(id=prompt_id)
        if not instance:
            return None
        update_data = payload.model_dump(exclude_unset=True)
        if "tags" in update_data and update_data["tags"] is not None:
            update_data["tags"] = ",".join(update_data["tags"])
        await self.repo.update_fields(instance, **update_data)
        await self.session.commit()
        prompt_read = PromptRead.model_validate(instance)
        async with _LOCK:
            _CACHE[prompt_read.name] = prompt_read
        return prompt_read

    async def delete_prompt(self, prompt_id: int) -> bool:
        instance = await self.repo.get(id=prompt_id)
        if not instance:
            return False
        await self.repo.delete(instance)
        await self.session.commit()
        async with _LOCK:
            _CACHE.pop(instance.name, None)
        return True
