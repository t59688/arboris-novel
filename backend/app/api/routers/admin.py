# AIMETA P=管理员API_用户管理和系统配置|R=管理员CRUD_系统配置_统计|NR=不含普通用户功能|E=route:POST_GET_/api/admin/*|X=http|A=用户CRUD_配置_统计|D=fastapi,sqlalchemy|S=db|RD=./README.ai
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.dependencies import get_current_admin
from ...db.session import get_session
from ...models import NovelProject, UsageMetric, User
from ...schemas.admin import (
    AdminNovelSummary,
    DailyRequestLimit,
    Statistics,
    UpdateLogCreate,
    UpdateLogRead,
    UpdateLogUpdate,
)
from ...schemas.config import SystemConfigCreate, SystemConfigRead, SystemConfigUpdate
from ...schemas.prompt import PromptCreate, PromptRead, PromptUpdate
from ...schemas.novel import (
    Chapter as ChapterSchema,
    NovelProject as NovelProjectSchema,
    NovelSectionResponse,
    NovelSectionType,
)
from ...schemas.user import (
    PasswordChangeRequest,
    User as UserSchema,
    UserCreateAdmin,
    UserUpdateAdmin,
)
from ...services.auth_service import AuthService
from ...services.admin_setting_service import AdminSettingService
from ...services.config_service import ConfigService
from ...services.novel_service import NovelService
from ...services.prompt_service import PromptService
from ...services.update_log_service import UpdateLogService
from ...services.user_service import UserService
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def get_prompt_service(session: AsyncSession = Depends(get_session)) -> PromptService:
    return PromptService(session)


def get_update_log_service(session: AsyncSession = Depends(get_session)) -> UpdateLogService:
    return UpdateLogService(session)


def get_admin_setting_service(session: AsyncSession = Depends(get_session)) -> AdminSettingService:
    return AdminSettingService(session)


def get_config_service(session: AsyncSession = Depends(get_session)) -> ConfigService:
    return ConfigService(session)


def get_novel_service(session: AsyncSession = Depends(get_session)) -> NovelService:
    return NovelService(session)


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)


@router.get("/stats", response_model=Statistics)
async def read_statistics(
    session: AsyncSession = Depends(get_session),
    _: None = Depends(get_current_admin),
) -> Statistics:
    novel_count = await session.scalar(select(func.count(NovelProject.id))) or 0
    user_count = await session.scalar(select(func.count(User.id))) or 0
    usage = await session.get(UsageMetric, "api_request_count")
    api_request_count = usage.value if usage else 0
    logger.info("管理员获取统计数据：小说=%s，用户=%s，请求=%s", novel_count, user_count, api_request_count)
    return Statistics(novel_count=novel_count, user_count=user_count, api_request_count=api_request_count)


@router.get("/users", response_model=List[UserSchema])
async def list_users(
    service: UserService = Depends(get_user_service),
    _: None = Depends(get_current_admin),
) -> List[UserSchema]:
    users = await service.list_users()
    logger.info("管理员请求用户列表，共 %s 条", len(users))
    return [UserSchema.model_validate(user) for user in users]


@router.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreateAdmin,
    service: UserService = Depends(get_user_service),
    current_admin=Depends(get_current_admin),
) -> UserSchema:
    try:
        user = await service.create_user_admin(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    logger.info("管理员 %s 创建用户：%s", current_admin.username, user.id)
    return UserSchema.model_validate(user)


@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: None = Depends(get_current_admin),
) -> UserSchema:
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return UserSchema.model_validate(user)


@router.patch("/users/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    payload: UserUpdateAdmin,
    service: UserService = Depends(get_user_service),
    current_admin=Depends(get_current_admin),
) -> UserSchema:
    try:
        user = await service.update_user_admin(user_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    logger.info("管理员 %s 更新用户：%s", current_admin.username, user_id)
    return UserSchema.model_validate(user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_admin=Depends(get_current_admin),
) -> None:
    try:
        deleted = await service.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="用户不存在")
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    logger.info("管理员 %s 删除用户：%s", current_admin.username, user_id)


@router.get("/novel-projects", response_model=List[AdminNovelSummary])
async def list_novel_projects(
    service: NovelService = Depends(get_novel_service),
    _: None = Depends(get_current_admin),
) -> List[AdminNovelSummary]:
    projects = await service.list_projects_for_admin()
    logger.info("管理员查看项目列表，共 %s 个", len(projects))
    return projects


@router.get("/novel-projects/{project_id}", response_model=NovelProjectSchema)
async def get_novel_project(
    project_id: str,
    service: NovelService = Depends(get_novel_service),
    _: None = Depends(get_current_admin),
) -> NovelProjectSchema:
    logger.info("管理员查看项目详情：%s", project_id)
    return await service.get_project_schema_for_admin(project_id)


@router.get("/novel-projects/{project_id}/sections/{section}", response_model=NovelSectionResponse)
async def get_novel_project_section(
    project_id: str,
    section: NovelSectionType,
    service: NovelService = Depends(get_novel_service),
    _: None = Depends(get_current_admin),
) -> NovelSectionResponse:
    logger.info("管理员查看项目 %s 的 %s 区段", project_id, section)
    return await service.get_section_data_for_admin(project_id, section)


@router.get("/novel-projects/{project_id}/chapters/{chapter_number}", response_model=ChapterSchema)
async def get_novel_project_chapter(
    project_id: str,
    chapter_number: int,
    service: NovelService = Depends(get_novel_service),
    _: None = Depends(get_current_admin),
) -> ChapterSchema:
    logger.info("管理员查看项目 %s 第 %s 章详情", project_id, chapter_number)
    return await service.get_chapter_schema_for_admin(project_id, chapter_number)


@router.get("/prompts", response_model=List[PromptRead])
async def list_prompts(
    service: PromptService = Depends(get_prompt_service),
    _: None = Depends(get_current_admin),
) -> List[PromptRead]:
    prompts = await service.list_prompts()
    logger.info("管理员请求提示词列表，共 %s 条", len(prompts))
    return prompts


@router.post("/prompts", response_model=PromptRead, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    payload: PromptCreate,
    service: PromptService = Depends(get_prompt_service),
    _: None = Depends(get_current_admin),
) -> PromptRead:
    prompt = await service.create_prompt(payload)
    logger.info("管理员创建提示词：%s", prompt.id)
    return prompt


@router.get("/prompts/{prompt_id}", response_model=PromptRead)
async def get_prompt(
    prompt_id: int,
    service: PromptService = Depends(get_prompt_service),
    _: None = Depends(get_current_admin),
) -> PromptRead:
    prompt = await service.get_prompt_by_id(prompt_id)
    if not prompt:
        logger.warning("提示词 %s 不存在", prompt_id)
        raise HTTPException(status_code=404, detail="提示词不存在")
    logger.info("管理员获取提示词：%s", prompt_id)
    return prompt


@router.patch("/prompts/{prompt_id}", response_model=PromptRead)
async def update_prompt(
    prompt_id: int,
    payload: PromptUpdate,
    service: PromptService = Depends(get_prompt_service),
    _: None = Depends(get_current_admin),
) -> PromptRead:
    result = await service.update_prompt(prompt_id, payload)
    if not result:
        logger.warning("提示词 %s 不存在，无法更新", prompt_id)
        raise HTTPException(status_code=404, detail="提示词不存在")
    logger.info("管理员更新提示词：%s", prompt_id)
    return result


@router.delete("/prompts/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: int,
    service: PromptService = Depends(get_prompt_service),
    _: None = Depends(get_current_admin),
) -> None:
    deleted = await service.delete_prompt(prompt_id)
    if not deleted:
        logger.warning("提示词 %s 不存在，无法删除", prompt_id)
        raise HTTPException(status_code=404, detail="提示词不存在")
    logger.info("管理员删除提示词：%s", prompt_id)


@router.get("/update-logs", response_model=List[UpdateLogRead])
async def list_update_logs(
    service: UpdateLogService = Depends(get_update_log_service),
    _: None = Depends(get_current_admin),
) -> List[UpdateLogRead]:
    logs = await service.list_logs()
    logger.info("管理员查看更新日志列表，共 %s 条", len(logs))
    return [UpdateLogRead.model_validate(log) for log in logs]


@router.post("/update-logs", response_model=UpdateLogRead, status_code=status.HTTP_201_CREATED)
async def create_update_log(
    payload: UpdateLogCreate,
    service: UpdateLogService = Depends(get_update_log_service),
    current_admin=Depends(get_current_admin),
) -> UpdateLogRead:
    log = await service.create_log(
        payload.content,
        creator=current_admin.username,
        is_pinned=payload.is_pinned or False,
    )
    logger.info("管理员 %s 创建更新日志：%s", current_admin.username, log.id)
    return UpdateLogRead.model_validate(log)


@router.delete("/update-logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_update_log(
    log_id: int,
    service: UpdateLogService = Depends(get_update_log_service),
    _: None = Depends(get_current_admin),
) -> None:
    await service.delete_log(log_id)
    logger.info("管理员删除更新日志：%s", log_id)


@router.patch("/update-logs/{log_id}", response_model=UpdateLogRead)
async def update_update_log(
    log_id: int,
    payload: UpdateLogUpdate,
    service: UpdateLogService = Depends(get_update_log_service),
    _: None = Depends(get_current_admin),
) -> UpdateLogRead:
    log = await service.update_log(
        log_id,
        content=payload.content,
        is_pinned=payload.is_pinned,
    )
    logger.info("管理员更新日志 %s", log_id)
    return UpdateLogRead.model_validate(log)


@router.get("/settings/daily-request-limit", response_model=DailyRequestLimit)
async def get_daily_limit(
    service: AdminSettingService = Depends(get_admin_setting_service),
    _: None = Depends(get_current_admin),
) -> DailyRequestLimit:
    value = await service.get("daily_request_limit", "100")
    logger.info("管理员查询每日请求上限：%s", value)
    return DailyRequestLimit(limit=int(value or 100))


@router.put("/settings/daily-request-limit", response_model=DailyRequestLimit)
async def update_daily_limit(
    payload: DailyRequestLimit,
    service: AdminSettingService = Depends(get_admin_setting_service),
    _: None = Depends(get_current_admin),
) -> DailyRequestLimit:
    await service.set("daily_request_limit", str(payload.limit))
    logger.info("管理员设置每日请求上限为 %s", payload.limit)
    return payload


@router.get("/system-configs", response_model=List[SystemConfigRead])
async def list_system_configs(
    service: ConfigService = Depends(get_config_service),
    _: None = Depends(get_current_admin),
) -> List[SystemConfigRead]:
    configs = await service.list_configs()
    logger.info("管理员获取系统配置，共 %s 条", len(configs))
    return configs


@router.get("/system-configs/{key}", response_model=SystemConfigRead)
async def get_system_config(
    key: str,
    service: ConfigService = Depends(get_config_service),
    _: None = Depends(get_current_admin),
) -> SystemConfigRead:
    config = await service.get_config(key)
    if not config:
        logger.warning("系统配置 %s 不存在", key)
        raise HTTPException(status_code=404, detail="配置项不存在")
    logger.info("管理员查询系统配置：%s", key)
    return config


@router.put("/system-configs/{key}", response_model=SystemConfigRead)
async def upsert_system_config(
    key: str,
    payload: SystemConfigCreate,
    service: ConfigService = Depends(get_config_service),
    _: None = Depends(get_current_admin),
) -> SystemConfigRead:
    logger.info("管理员写入系统配置：%s", key)
    return await service.upsert_config(
        SystemConfigCreate(key=key, value=payload.value, description=payload.description)
    )


@router.patch("/system-configs/{key}", response_model=SystemConfigRead)
async def patch_system_config(
    key: str,
    payload: SystemConfigUpdate,
    service: ConfigService = Depends(get_config_service),
    _: None = Depends(get_current_admin),
) -> SystemConfigRead:
    config = await service.patch_config(key, payload)
    if not config:
        logger.warning("系统配置 %s 不存在，无法更新", key)
        raise HTTPException(status_code=404, detail="配置项不存在")
    logger.info("管理员部分更新系统配置：%s", key)
    return config


@router.delete("/system-configs/{key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_config(
    key: str,
    service: ConfigService = Depends(get_config_service),
    _: None = Depends(get_current_admin),
) -> None:
    deleted = await service.remove_config(key)
    if not deleted:
        logger.warning("系统配置 %s 不存在，无法删除", key)
        raise HTTPException(status_code=404, detail="配置项不存在")
    logger.info("管理员删除系统配置：%s", key)


@router.post("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    payload: PasswordChangeRequest,
    current_admin=Depends(get_current_admin),
    service: AuthService = Depends(get_auth_service),
) -> None:
    await service.change_password(current_admin.username, payload.old_password, payload.new_password)
    logger.info("管理员 %s 修改密码", current_admin.username)
