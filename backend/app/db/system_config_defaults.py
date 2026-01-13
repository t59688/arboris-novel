# AIMETA P=系统配置默认值_初始配置数据|R=默认配置字典|NR=不含配置逻辑|E=SYSTEM_CONFIG_DEFAULTS|X=internal|A=配置字典|D=none|S=none|RD=./README.ai
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from ..core.config import Settings


def _to_optional_str(value: Optional[object]) -> Optional[str]:
    return str(value) if value is not None else None


def _bool_to_text(value: bool) -> str:
    return "true" if value else "false"


@dataclass(frozen=True)
class SystemConfigDefault:
    key: str
    value_getter: Callable[[Settings], Optional[str]]
    description: Optional[str] = None


SYSTEM_CONFIG_DEFAULTS: list[SystemConfigDefault] = [
    SystemConfigDefault(
        key="llm.api_key",
        value_getter=lambda config: config.openai_api_key,
        description="默认 LLM API Key，用于后台调用大模型。",
    ),
    SystemConfigDefault(
        key="llm.base_url",
        value_getter=lambda config: _to_optional_str(config.openai_base_url),
        description="默认大模型 API Base URL。",
    ),
    SystemConfigDefault(
        key="llm.model",
        value_getter=lambda config: config.openai_model_name,
        description="默认 LLM 模型名称。",
    ),
    SystemConfigDefault(
        key="smtp.server",
        value_getter=lambda config: config.smtp_server,
        description="用于发送邮件验证码的 SMTP 服务器地址。",
    ),
    SystemConfigDefault(
        key="smtp.port",
        value_getter=lambda config: _to_optional_str(config.smtp_port),
        description="SMTP 服务端口。",
    ),
    SystemConfigDefault(
        key="smtp.username",
        value_getter=lambda config: config.smtp_username,
        description="SMTP 登录用户名。",
    ),
    SystemConfigDefault(
        key="smtp.password",
        value_getter=lambda config: config.smtp_password,
        description="SMTP 登录密码。",
    ),
    SystemConfigDefault(
        key="smtp.from",
        value_getter=lambda config: config.email_from,
        description="邮件显示的发件人名称或邮箱。",
    ),
    SystemConfigDefault(
        key="auth.allow_registration",
        value_getter=lambda config: _bool_to_text(config.allow_registration),
        description="是否允许用户自助注册。",
    ),
    SystemConfigDefault(
        key="auth.linuxdo_enabled",
        value_getter=lambda config: _bool_to_text(config.enable_linuxdo_login),
        description="是否启用 Linux.do OAuth 登录。",
    ),
    SystemConfigDefault(
        key="linuxdo.client_id",
        value_getter=lambda config: config.linuxdo_client_id,
        description="Linux.do OAuth Client ID。",
    ),
    SystemConfigDefault(
        key="linuxdo.client_secret",
        value_getter=lambda config: config.linuxdo_client_secret,
        description="Linux.do OAuth Client Secret。",
    ),
    SystemConfigDefault(
        key="linuxdo.redirect_uri",
        value_getter=lambda config: _to_optional_str(config.linuxdo_redirect_uri),
        description="Linux.do OAuth 回调地址。",
    ),
    SystemConfigDefault(
        key="linuxdo.auth_url",
        value_getter=lambda config: _to_optional_str(config.linuxdo_auth_url),
        description="Linux.do OAuth 授权地址。",
    ),
    SystemConfigDefault(
        key="linuxdo.token_url",
        value_getter=lambda config: _to_optional_str(config.linuxdo_token_url),
        description="Linux.do OAuth Token 获取地址。",
    ),
    SystemConfigDefault(
        key="linuxdo.user_info_url",
        value_getter=lambda config: _to_optional_str(config.linuxdo_user_info_url),
        description="Linux.do 用户信息接口地址。",
    ),
    SystemConfigDefault(
        key="writer.chapter_versions",
        value_getter=lambda config: _to_optional_str(config.writer_chapter_versions),
        description="每次生成章节的候选版本数量。",
    ),
    SystemConfigDefault(
        key="embedding.provider",
        value_getter=lambda config: config.embedding_provider,
        description="嵌入模型提供方，支持 openai 或 ollama。",
    ),
    SystemConfigDefault(
        key="embedding.api_key",
        value_getter=lambda config: config.embedding_api_key,
        description="嵌入模型专用 API Key，留空则使用默认 LLM API Key。",
    ),
    SystemConfigDefault(
        key="embedding.base_url",
        value_getter=lambda config: _to_optional_str(config.embedding_base_url),
        description="嵌入模型使用的 Base URL，留空则使用默认 LLM Base URL。",
    ),
    SystemConfigDefault(
        key="embedding.model",
        value_getter=lambda config: config.embedding_model,
        description="OpenAI 嵌入模型名称。",
    ),
    SystemConfigDefault(
        key="embedding.model_vector_size",
        value_getter=lambda config: _to_optional_str(config.embedding_model_vector_size),
        description="嵌入向量维度，留空则自动检测。",
    ),
    SystemConfigDefault(
        key="ollama.embedding_base_url",
        value_getter=lambda config: _to_optional_str(config.ollama_embedding_base_url),
        description="Ollama 嵌入模型服务地址。",
    ),
    SystemConfigDefault(
        key="ollama.embedding_model",
        value_getter=lambda config: config.ollama_embedding_model,
        description="Ollama 嵌入模型名称。",
    ),
]
