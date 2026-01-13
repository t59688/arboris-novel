# AIMETA P=用户服务_用户管理业务逻辑|R=用户CRUD_权限|NR=不含认证逻辑|E=UserService|X=internal|A=服务类|D=sqlalchemy|S=db|RD=./README.ai
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import hash_password
from ..models import User
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserCreateAdmin, UserInDB, UserUpdateAdmin


class UserService:
    """用户领域服务，负责注册、查询与配额统计。"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def create_user(self, payload: UserCreate, *, external_id: str | None = None) -> UserInDB:
        hashed_password = hash_password(payload.password)
        user = User(
            username=payload.username,
            email=payload.email,
            hashed_password=hashed_password,
            external_id=external_id,
        )

        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ValueError("用户名或邮箱已存在") from exc

        return UserInDB.model_validate(user)

    async def get_by_username(self, username: str) -> Optional[UserInDB]:
        user = await self.repo.get_by_username(username)
        return UserInDB.model_validate(user) if user else None

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        user = await self.repo.get_by_email(email)
        return UserInDB.model_validate(user) if user else None

    async def get_by_external_id(self, external_id: str) -> Optional[UserInDB]:
        user = await self.repo.get_by_external_id(external_id)
        return UserInDB.model_validate(user) if user else None

    async def get_user(self, user_id: int) -> Optional[UserInDB]:
        user = await self.repo.get(id=user_id)
        return UserInDB.model_validate(user) if user else None

    async def list_users(self) -> list[UserInDB]:
        users = await self.repo.list_all()
        return [UserInDB.model_validate(item) for item in users]

    async def increment_daily_request(self, user_id: int) -> None:
        await self.repo.increment_daily_request(user_id)
        await self.session.commit()

    async def get_daily_request(self, user_id: int) -> int:
        return await self.repo.get_daily_request(user_id)

    async def create_user_admin(self, payload: UserCreateAdmin) -> UserInDB:
        if payload.is_admin:
            raise ValueError("不允许直接创建管理员账号")
            
        hashed_password = hash_password(payload.password)
        user = User(
            username=payload.username,
            email=payload.email,
            hashed_password=hashed_password,
            is_admin=False,  # 强制为 False
            is_active=payload.is_active,
        )

        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ValueError("用户名或邮箱已存在") from exc

        return UserInDB.model_validate(user)

    async def update_user_admin(self, user_id: int, payload: UserUpdateAdmin) -> Optional[UserInDB]:
        user = await self.repo.get(id=user_id)
        if not user:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        await self.repo.update_fields(user, **update_data)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ValueError("用户名或邮箱已存在") from exc
            
        return UserInDB.model_validate(user)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.repo.get(id=user_id)
        if not user:
            return False
            
        if user.is_admin:
            raise ValueError("无法删除管理员账号")
            
        await self.repo.delete(user)
        await self.session.commit()
        return True
