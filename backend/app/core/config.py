# AIMETA P=应用配置_环境变量加载和设置类|R=配置加载_环境变量|NR=不含业务逻辑|E=settings|X=internal|A=Settings类|D=pydantic|S=fs|RD=./README.ai
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import AliasChoices, AnyUrl, Field, HttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, make_url


class Settings(BaseSettings):
    """应用全局配置，所有可调参数集中于此，统一加载自环境变量。"""

    # -------------------- 基础应用配置 --------------------
    app_name: str = Field(default="AI Novel Generator API", description="FastAPI 文档标题")
    environment: str = Field(default="development", description="当前环境标识")
    debug: bool = Field(default=True, description="是否开启调试模式")
    allow_registration: bool = Field(
        default=True,
        env="ALLOW_USER_REGISTRATION",
        description="是否允许用户自助注册",
    )
    logging_level: str = Field(
        default="INFO",
        env="LOGGING_LEVEL",
        description="应用日志级别",
    )
    enable_linuxdo_login: bool = Field(
        default=False,
        env="ENABLE_LINUXDO_LOGIN",
        description="是否启用 Linux.do OAuth 登录",
    )

    # -------------------- 安全相关配置 --------------------
    secret_key: str = Field(..., env="SECRET_KEY", description="JWT 加密密钥")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM", description="JWT 加密算法")
    access_token_expire_minutes: int = Field(
        default=60 * 24 * 7,
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="访问令牌过期时间，单位分钟"
    )

    # -------------------- 数据库配置 --------------------
    database_url: Optional[str] = Field(
        default=None,
        env="DATABASE_URL",
        description="完整的数据库连接串，填入后覆盖下方数据库配置"
    )
    db_provider: str = Field(
        default="mysql",
        env="DB_PROVIDER",
        description="数据库类型，仅支持 mysql 或 sqlite"
    )
    mysql_host: str = Field(default="localhost", env="MYSQL_HOST", description="MySQL 主机名")
    mysql_port: int = Field(default=3306, env="MYSQL_PORT", description="MySQL 端口")
    mysql_user: str = Field(default="root", env="MYSQL_USER", description="MySQL 用户名")
    mysql_password: str = Field(default="", env="MYSQL_PASSWORD", description="MySQL 密码")
    mysql_database: str = Field(default="arboris", env="MYSQL_DATABASE", description="MySQL 数据库名称")

    # -------------------- 管理员初始化配置 --------------------
    admin_default_username: str = Field(default="admin", env="ADMIN_DEFAULT_USERNAME", description="默认管理员用户名")
    admin_default_password: str = Field(default="ChangeMe123!", env="ADMIN_DEFAULT_PASSWORD", description="默认管理员密码")
    admin_default_email: Optional[str] = Field(default=None, env="ADMIN_DEFAULT_EMAIL", description="默认管理员邮箱")

    # -------------------- LLM 相关配置 --------------------
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY", description="默认的 LLM API Key")
    openai_base_url: Optional[HttpUrl] = Field(
        default=None,
        env="OPENAI_API_BASE_URL",
        validation_alias=AliasChoices("OPENAI_API_BASE_URL", "OPENAI_BASE_URL"),
        description="LLM API Base URL",
    )
    openai_model_name: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL_NAME", description="默认 LLM 模型名称")
    writer_chapter_versions: int = Field(
        default=2,
        ge=1,
        env="WRITER_CHAPTER_VERSION_COUNT",
        validation_alias=AliasChoices("WRITER_CHAPTER_VERSION_COUNT", "WRITER_CHAPTER_VERSIONS"),
        description="每次生成章节的候选版本数量",
    )
    embedding_provider: str = Field(
        default="openai",
        env="EMBEDDING_PROVIDER",
        description="嵌入模型提供方，支持 openai 或 ollama",
    )
    embedding_base_url: Optional[AnyUrl] = Field(
        default=None,
        env="EMBEDDING_BASE_URL",
        description="嵌入模型使用的 Base URL",
    )
    embedding_api_key: Optional[str] = Field(
        default=None,
        env="EMBEDDING_API_KEY",
        description="嵌入模型专用 API Key",
    )
    embedding_model: str = Field(
        default="text-embedding-3-large",
        env="EMBEDDING_MODEL",
        validation_alias=AliasChoices("EMBEDDING_MODEL", "VECTOR_EMBEDDING_MODEL"),
        description="默认的嵌入模型名称",
    )
    embedding_model_vector_size: Optional[int] = Field(
        default=None,
        env="EMBEDDING_MODEL_VECTOR_SIZE",
        description="嵌入向量维度，未配置时将自动检测",
    )
    ollama_embedding_base_url: Optional[AnyUrl] = Field(
        default=None,
        env="OLLAMA_EMBEDDING_BASE_URL",
        description="Ollama 嵌入模型服务地址",
    )
    ollama_embedding_model: str = Field(
        default="nomic-embed-text:latest",
        env="OLLAMA_EMBEDDING_MODEL",
        description="Ollama 嵌入模型名称",
    )
    vector_db_url: Optional[str] = Field(
        default=None,
        env="VECTOR_DB_URL",
        description="libsql 向量库连接地址",
    )
    vector_db_auth_token: Optional[str] = Field(
        default=None,
        env="VECTOR_DB_AUTH_TOKEN",
        description="libsql 访问令牌",
    )
    vector_top_k_chunks: int = Field(
        default=5,
        ge=0,
        env="VECTOR_TOP_K_CHUNKS",
        description="剧情 chunk 检索条数",
    )
    vector_top_k_summaries: int = Field(
        default=3,
        ge=0,
        env="VECTOR_TOP_K_SUMMARIES",
        description="章节摘要检索条数",
    )
    vector_chunk_size: int = Field(
        default=480,
        ge=128,
        env="VECTOR_CHUNK_SIZE",
        description="章节分块的目标字数",
    )
    vector_chunk_overlap: int = Field(
        default=120,
        ge=0,
        env="VECTOR_CHUNK_OVERLAP",
        description="章节分块重叠字数",
    )

    # -------------------- Linux.do OAuth 配置 --------------------
    linuxdo_client_id: Optional[str] = Field(default=None, env="LINUXDO_CLIENT_ID", description="Linux.do OAuth Client ID")
    linuxdo_client_secret: Optional[str] = Field(
        default=None, env="LINUXDO_CLIENT_SECRET", description="Linux.do OAuth Client Secret"
    )
    linuxdo_redirect_uri: Optional[HttpUrl] = Field(
        default=None, env="LINUXDO_REDIRECT_URI", description="Linux.do OAuth 回调地址"
    )
    linuxdo_auth_url: Optional[HttpUrl] = Field(
        default=None, env="LINUXDO_AUTH_URL", description="Linux.do OAuth 授权地址"
    )
    linuxdo_token_url: Optional[HttpUrl] = Field(
        default=None, env="LINUXDO_TOKEN_URL", description="Linux.do OAuth Token 获取地址"
    )
    linuxdo_user_info_url: Optional[HttpUrl] = Field(
        default=None, env="LINUXDO_USER_INFO_URL", description="Linux.do 用户信息接口地址"
    )

    # -------------------- 邮件配置 --------------------
    smtp_server: Optional[str] = Field(default=None, env="SMTP_SERVER", description="SMTP 服务地址")
    smtp_port: int = Field(default=587, env="SMTP_PORT", description="SMTP 服务端口")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME", description="SMTP 登录用户名")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD", description="SMTP 登录密码")
    email_from: Optional[str] = Field(default=None, env="EMAIL_FROM", description="邮件发送方显示名或邮箱")

    model_config = SettingsConfigDict(
        env_file=("new-backend/.env", ".env", "backend/.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @validator("database_url", pre=True, always=True)
    def _normalize_database_url(cls, value: Optional[str]) -> Optional[str]:
        """当环境变量中提供 DATABASE_URL 时，原样返回，便于自定义。"""
        return value.strip() if isinstance(value, str) and value.strip() else value

    @validator("db_provider", pre=True)
    def _normalize_db_provider(cls, value: Optional[str]) -> str:
        """统一数据库类型大小写，并限制为受支持的驱动。"""
        candidate = (value or "mysql").strip().lower()
        if candidate not in {"mysql", "sqlite"}:
            raise ValueError("DB_PROVIDER 仅支持 mysql 或 sqlite")
        return candidate
    @validator("embedding_provider", pre=True)
    def _normalize_embedding_provider(cls, value: Optional[str]) -> str:
        """限制嵌入模型提供方的取值范围。"""
        candidate = (value or "openai").strip().lower()
        if candidate not in {"openai", "ollama"}:
            raise ValueError("EMBEDDING_PROVIDER 仅支持 openai 或 ollama")
        return candidate

    @validator("logging_level", pre=True)
    def _normalize_logging_level(cls, value: Optional[str]) -> str:
        """规范日志级别配置。"""
        candidate = (value or "INFO").strip().upper()
        valid_levels = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
        if candidate not in valid_levels:
            raise ValueError("LOGGING_LEVEL 仅支持 CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET")
        return candidate

    @property
    def sqlalchemy_database_uri(self) -> str:
        """生成 SQLAlchemy 兼容的异步连接串，数据库类型由 DB_PROVIDER 控制。"""
        if self.database_url:
            url = make_url(self.database_url)
            database = (url.database or "").strip("/")
            normalized = URL.create(
                drivername=url.drivername,
                username=url.username,
                password=url.password,
                host=url.host,
                port=url.port,
                database=database or None,
                query=url.query,
            )
            return normalized.render_as_string(hide_password=False)

        if self.db_provider == "sqlite":
            # SQLite 固定使用 storage/arboris.db，并转换为绝对路径以避免运行目录差异
            project_root = Path(__file__).resolve().parents[2]
            db_path = (project_root / "storage" / "arboris.db").resolve()
            return f"sqlite+aiosqlite:///{db_path}"

        # MySQL 分支：统一对密码进行 URL 编码，避免特殊字符破坏连接串
        from urllib.parse import quote_plus

        encoded_password = quote_plus(self.mysql_password)
        database = (self.mysql_database or "").strip("/")
        return (
            f"mysql+asyncmy://{self.mysql_user}:{encoded_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{database}"
        )

    @property
    def is_sqlite_backend(self) -> bool:
        """辅助属性：判断当前连接串是否指向 SQLite，用于差异化初始化流程。"""
        return make_url(self.sqlalchemy_database_uri).get_backend_name() == "sqlite"

    @property
    def vector_store_enabled(self) -> bool:
        """是否已经配置向量库，用于在业务逻辑中快速判断。"""
        return bool(self.vector_db_url)


@lru_cache
def get_settings() -> Settings:
    """使用 LRU 缓存确保配置只初始化一次，减少 IO 与解析开销。"""
    return Settings()


settings = get_settings()
