# AIMETA P=依赖注入_FastAPI依赖项定义|R=数据库会话_当前用户获取|NR=不含业务逻辑|E=get_db_get_current_user|X=internal|A=依赖函数|D=fastapi,sqlalchemy|S=db|RD=./README.ai
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import decode_access_token
from ..db.session import get_session
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserInDB
from ..services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserInDB:
    payload = decode_access_token(token)
    username = payload["sub"]
    repo = UserRepository(session)
    user = await repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在或已被禁用")
    service = AuthService(session)
    schema = UserInDB.model_validate(user)
    schema.must_change_password = service.requires_password_reset(user)
    return schema


async def get_current_admin(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="需要管理员权限")
    return current_user
