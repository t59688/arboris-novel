# AIMETA P=安全模块_JWT令牌和密码处理|R=JWT生成验证_密码哈希|NR=不含用户管理|E=create_token_verify_password|X=internal|A=安全函数|D=jose,passlib|S=none|RD=./README.ai
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings

# 统一的密码哈希上下文，后续如需切换算法只需在此维护
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """对用户密码进行哈希处理，任何时候都不要存储明文密码。"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码是否匹配哈希值。"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    *,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """生成 JWT 访问令牌，默认过期时间读取自配置。"""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

    now = datetime.utcnow()
    expire = now + expires_delta

    to_encode: Dict[str, Any] = {"sub": subject, "iat": now, "exp": expire}
    if extra_claims:
        to_encode.update(extra_claims)

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Dict[str, Any]:
    """解析并校验 JWT，失败时抛出 401 异常。"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise credentials_exception from exc

    if "sub" not in payload:
        raise credentials_exception
    return payload
