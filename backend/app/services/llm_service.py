# AIMETA P=LLM服务_大模型调用封装|R=API调用_流式生成|NR=不含业务逻辑|E=LLMService|X=internal|A=服务类|D=openai,httpx|S=net|RD=./README.ai
import logging
import os
from typing import Any, Dict, List, Optional

import httpx
from fastapi import HTTPException, status
from openai import APIConnectionError, APITimeoutError, AsyncOpenAI, InternalServerError

from ..core.config import settings
from ..repositories.llm_config_repository import LLMConfigRepository
from ..repositories.system_config_repository import SystemConfigRepository
from ..repositories.user_repository import UserRepository
from ..services.admin_setting_service import AdminSettingService
from ..services.prompt_service import PromptService
from ..services.usage_service import UsageService
from ..utils.llm_tool import ChatMessage, LLMClient

logger = logging.getLogger(__name__)

try:  # pragma: no cover - 运行环境未安装时兼容
    from ollama import AsyncClient as OllamaAsyncClient
except ImportError:  # pragma: no cover - Ollama 为可选依赖
    OllamaAsyncClient = None


class LLMService:
    """封装与大模型交互的所有逻辑，包括配额控制与配置选择。"""

    def __init__(self, session):
        self.session = session
        self.llm_repo = LLMConfigRepository(session)
        self.system_config_repo = SystemConfigRepository(session)
        self.user_repo = UserRepository(session)
        self.admin_setting_service = AdminSettingService(session)
        self.usage_service = UsageService(session)
        self._embedding_dimensions: Dict[str, int] = {}

    async def get_llm_response(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        *,
        temperature: float = 0.7,
        user_id: Optional[int] = None,
        timeout: float = 300.0,
        response_format: Optional[str] = "json_object",
    ) -> str:
        messages = [{"role": "system", "content": system_prompt}, *conversation_history]
        return await self._stream_and_collect(
            messages,
            temperature=temperature,
            user_id=user_id,
            timeout=timeout,
            response_format=response_format,
        )

    async def get_summary(
        self,
        chapter_content: str,
        *,
        temperature: float = 0.2,
        user_id: Optional[int] = None,
        timeout: float = 180.0,
        system_prompt: Optional[str] = None,
    ) -> str:
        if not system_prompt:
            prompt_service = PromptService(self.session)
            system_prompt = await prompt_service.get_prompt("extraction")
        if not system_prompt:
            logger.error("未配置名为 'extraction' 的摘要提示词，无法生成章节摘要")
            raise HTTPException(status_code=500, detail="未配置摘要提示词，请联系管理员配置 'extraction' 提示词")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chapter_content},
        ]
        return await self._stream_and_collect(messages, temperature=temperature, user_id=user_id, timeout=timeout)

    async def _stream_and_collect(
        self,
        messages: List[Dict[str, str]],
        *,
        temperature: float,
        user_id: Optional[int],
        timeout: float,
        response_format: Optional[str] = None,
    ) -> str:
        config = await self._resolve_llm_config(user_id)
        client = LLMClient(api_key=config["api_key"], base_url=config.get("base_url"))

        chat_messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in messages]

        full_response = ""
        finish_reason = None

        logger.info(
            "Streaming LLM response: model=%s user_id=%s messages=%d",
            config.get("model"),
            user_id,
            len(messages),
        )

        try:
            async for part in client.stream_chat(
                messages=chat_messages,
                model=config.get("model"),
                temperature=temperature,
                timeout=int(timeout),
                response_format=response_format,
            ):
                if part.get("content"):
                    full_response += part["content"]
                if part.get("finish_reason"):
                    finish_reason = part["finish_reason"]
        except InternalServerError as exc:
            detail = "AI 服务内部错误，请稍后重试"
            response = getattr(exc, "response", None)
            if response is not None:
                try:
                    payload = response.json()
                    error_data = payload.get("error", {}) if isinstance(payload, dict) else {}
                    detail = error_data.get("message_zh") or error_data.get("message") or detail
                except Exception:
                    detail = str(exc) or detail
            else:
                detail = str(exc) or detail
            logger.error(
                "LLM stream internal error: model=%s user_id=%s detail=%s",
                config.get("model"),
                user_id,
                detail,
                exc_info=exc,
            )
            raise HTTPException(status_code=503, detail=detail)
        except (httpx.RemoteProtocolError, httpx.ReadTimeout, APIConnectionError, APITimeoutError) as exc:
            if isinstance(exc, httpx.RemoteProtocolError):
                detail = "AI 服务连接被意外中断，请稍后重试"
            elif isinstance(exc, (httpx.ReadTimeout, APITimeoutError)):
                detail = "AI 服务响应超时，请稍后重试"
            else:
                detail = "无法连接到 AI 服务，请稍后重试"
            logger.error(
                "LLM stream failed: model=%s user_id=%s detail=%s",
                config.get("model"),
                user_id,
                detail,
                exc_info=exc,
            )
            raise HTTPException(status_code=503, detail=detail) from exc

        logger.debug(
            "LLM response collected: model=%s user_id=%s finish_reason=%s preview=%s",
            config.get("model"),
            user_id,
            finish_reason,
            full_response[:500],
        )

        if finish_reason == "length":
            logger.warning(
                "LLM response truncated: model=%s user_id=%s response_length=%d",
                config.get("model"),
                user_id,
                len(full_response),
            )
            raise HTTPException(
                status_code=500,
                detail=f"AI 响应因长度限制被截断（已生成 {len(full_response)} 字符），请缩短输入内容或调整模型参数"
            )

        if not full_response:
            logger.error(
                "LLM returned empty response: model=%s user_id=%s finish_reason=%s",
                config.get("model"),
                user_id,
                finish_reason,
            )
            raise HTTPException(
                status_code=500,
                detail=f"AI 未返回有效内容（结束原因: {finish_reason or '未知'}），请稍后重试或联系管理员"
            )

        await self.usage_service.increment("api_request_count")
        logger.info(
            "LLM response success: model=%s user_id=%s chars=%d",
            config.get("model"),
            user_id,
            len(full_response),
        )
        return full_response

    async def _resolve_llm_config(self, user_id: Optional[int]) -> Dict[str, Optional[str]]:
        if user_id:
            config = await self.llm_repo.get_by_user(user_id)
            if config and config.llm_provider_api_key:
                return {
                    "api_key": config.llm_provider_api_key,
                    "base_url": config.llm_provider_url,
                    "model": config.llm_provider_model,
                }

        # 检查每日使用次数限制
        if user_id:
            await self._enforce_daily_limit(user_id)

        api_key = await self._get_config_value("llm.api_key")
        base_url = await self._get_config_value("llm.base_url")
        model = await self._get_config_value("llm.model")

        if not api_key:
            logger.error("未配置默认 LLM API Key，且用户 %s 未设置自定义 API Key", user_id)
            raise HTTPException(
                status_code=500,
                detail="未配置默认 LLM API Key，请联系管理员配置系统默认 API Key 或在个人设置中配置自定义 API Key"
            )

        return {"api_key": api_key, "base_url": base_url, "model": model}

    async def get_embedding(
        self,
        text: str,
        *,
        user_id: Optional[int] = None,
        model: Optional[str] = None,
    ) -> List[float]:
        """生成文本向量，用于章节 RAG 检索，支持 openai 与 ollama 双提供方。"""
        provider = await self._get_config_value("embedding.provider") or "openai"
        default_model = (
            await self._get_config_value("ollama.embedding_model") or "nomic-embed-text:latest"
            if provider == "ollama"
            else await self._get_config_value("embedding.model") or "text-embedding-3-large"
        )
        target_model = model or default_model

        if provider == "ollama":
            if OllamaAsyncClient is None:
                logger.error("未安装 ollama 依赖，无法调用本地嵌入模型。")
                raise HTTPException(status_code=500, detail="缺少 Ollama 依赖，请先安装 ollama 包。")

            base_url = (
                await self._get_config_value("ollama.embedding_base_url")
                or await self._get_config_value("embedding.base_url")
            )
            client = OllamaAsyncClient(host=base_url)
            try:
                response = await client.embeddings(model=target_model, prompt=text)
            except Exception as exc:  # pragma: no cover - 本地服务调用失败
                logger.error(
                    "Ollama 嵌入请求失败: model=%s base_url=%s error=%s",
                    target_model,
                    base_url,
                    exc,
                    exc_info=True,
                )
                return []
            embedding: Optional[List[float]]
            if isinstance(response, dict):
                embedding = response.get("embedding")
            else:
                embedding = getattr(response, "embedding", None)
            if not embedding:
                logger.warning("Ollama 返回空向量: model=%s", target_model)
                return []
            if not isinstance(embedding, list):
                embedding = list(embedding)
        else:
            config = await self._resolve_llm_config(user_id)
            api_key = await self._get_config_value("embedding.api_key") or config["api_key"]
            base_url = await self._get_config_value("embedding.base_url") or config.get("base_url")
            client = AsyncOpenAI(api_key=api_key, base_url=base_url)
            try:
                response = await client.embeddings.create(
                    input=text,
                    model=target_model,
                )
            except Exception as exc:  # pragma: no cover - 网络或鉴权失败
                logger.error(
                    "OpenAI 嵌入请求失败: model=%s base_url=%s user_id=%s error=%s",
                    target_model,
                    base_url,
                    user_id,
                    exc,
                    exc_info=True,
                )
                return []
            if not response.data:
                logger.warning("OpenAI 嵌入请求返回空数据: model=%s user_id=%s", target_model, user_id)
                return []
            embedding = response.data[0].embedding

        if not isinstance(embedding, list):
            embedding = list(embedding)

        dimension = len(embedding)
        if not dimension:
            vector_size_str = await self._get_config_value("embedding.model_vector_size")
            if vector_size_str:
                dimension = int(vector_size_str)
        if dimension:
            self._embedding_dimensions[target_model] = dimension
        return embedding

    async def get_embedding_dimension(self, model: Optional[str] = None) -> Optional[int]:
        """获取嵌入向量维度，优先返回缓存结果，其次读取配置。"""
        provider = await self._get_config_value("embedding.provider") or "openai"
        default_model = (
            await self._get_config_value("ollama.embedding_model") or "nomic-embed-text:latest"
            if provider == "ollama"
            else await self._get_config_value("embedding.model") or "text-embedding-3-large"
        )
        target_model = model or default_model
        if target_model in self._embedding_dimensions:
            return self._embedding_dimensions[target_model]
        vector_size_str = await self._get_config_value("embedding.model_vector_size")
        return int(vector_size_str) if vector_size_str else None

    async def _enforce_daily_limit(self, user_id: int) -> None:
        limit_str = await self.admin_setting_service.get("daily_request_limit", "100")
        limit = int(limit_str or 10)
        used = await self.user_repo.get_daily_request(user_id)
        if used >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="今日请求次数已达上限，请明日再试或设置自定义 API Key。",
            )
        await self.user_repo.increment_daily_request(user_id)
        await self.session.commit()

    async def _get_config_value(self, key: str) -> Optional[str]:
        record = await self.system_config_repo.get_by_key(key)
        if record:
            return record.value
        # 兼容环境变量，首次迁移时无需立即写入数据库
        env_key = key.upper().replace(".", "_")
        return os.getenv(env_key)
