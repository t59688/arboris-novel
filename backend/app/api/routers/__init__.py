# AIMETA P=路由聚合_注册所有子路由到主路由|R=路由注册|NR=不含具体端点实现|E=api_router|X=http|A=APIRouter聚合|D=fastapi|S=none|RD=./README.ai
from fastapi import APIRouter
from . import admin, auth, llm_config, novels, optimizer, updates, writer, analytics, analytics_enhanced, foreshadowing

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(novels.router)
api_router.include_router(writer.router)
api_router.include_router(admin.router)
api_router.include_router(updates.router)
api_router.include_router(llm_config.router)
api_router.include_router(optimizer.router)
api_router.include_router(analytics.router)
api_router.include_router(analytics_enhanced.router, prefix='/enhanced')
api_router.include_router(foreshadowing.router)
