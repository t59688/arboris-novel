# AIMETA P=认证API_登录注册和令牌管理|R=用户认证_令牌生成|NR=不含用户管理|E=route:POST_/api/auth/*|X=http|A=登录_注册_令牌|D=fastapi,jose|S=db|RD=./README.ai
import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.config import settings
from ...core.dependencies import get_current_user
from ...db.session import get_session
from ...schemas.user import AuthOptions, Token, User, UserInDB, UserRegistration
from ...services.auth_service import AuthService


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)


@router.post("/send-code", status_code=204)
async def send_verification_code(email: str, service: AuthService = Depends(get_auth_service)):
    await service.send_verification_code(email)
    logger.info("向 %s 发送验证码", email)


@router.get("/options", response_model=AuthOptions)
async def read_auth_options(service: AuthService = Depends(get_auth_service)):
    """读取认证功能开关，供前端动态渲染。"""
    options = await service.get_auth_options()
    return options


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserRegistration, service: AuthService = Depends(get_auth_service)):
    user = await service.register_user(payload)
    logger.info("注册新用户：%s", user.username)
    return User.model_validate(user)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    user = await service.authenticate_user(form_data.username, form_data.password)
    must_change_password = service.requires_password_reset(user)
    token = await service.create_access_token(user, must_change_password=must_change_password)
    logger.info("用户 %s 登录成功，需改密=%s", form_data.username, must_change_password)
    return token


@router.get("/users/me", response_model=User)
async def read_current_user(current_user: UserInDB = Depends(get_current_user)):
    logger.debug("读取当前用户：%s", current_user.username)
    return current_user


@router.get("/linuxdo/login")
async def login_with_linuxdo(service: AuthService = Depends(get_auth_service)):
    if not await service.is_linuxdo_login_enabled():
        logger.warning("Linux.do 登录未启用")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未启用 Linux.do 登录")
    client_id = await service.get_config_value("linuxdo.client_id")
    redirect_uri = await service.get_config_value("linuxdo.redirect_uri")
    auth_url = await service.get_config_value("linuxdo.auth_url")
    if not all([client_id, redirect_uri, auth_url]):
        logger.error("Linux.do OAuth 参数未配置完整")
        raise HTTPException(status_code=500, detail="未配置 Linux.do OAuth 参数")
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "user",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    logger.info("跳转 Linux.do 授权，client_id=%s", client_id)
    return RedirectResponse(url=f"{auth_url}?{query}")


@router.get("/linuxdo/register", response_class=HTMLResponse)
async def register_with_linuxdo(code: str, service: AuthService = Depends(get_auth_service)):
    token = await service.handle_linuxdo_callback(code)
    logger.info("Linux.do 授权回调成功")
    token_json = token.model_dump_json()
    html_content = f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
<head><meta charset=\"UTF-8\"><title>正在跳转</title></head>
<body>
    <p>正在跳转，请稍候...</p>
    <script>
        (function() {{
            const token = JSON.parse('{token_json}');
            try {{
                window.localStorage.setItem('token', token.access_token);
            }} catch (err) {{
                console.error('无法写入本地存储', err);
            }}
            window.location.replace('/');
        }})();
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)
