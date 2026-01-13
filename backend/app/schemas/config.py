# AIMETA P=配置模式_系统配置请求响应结构|R=配置读写结构|NR=不含业务逻辑|E=ConfigSchema|X=internal|A=Pydantic模式|D=pydantic|S=none|RD=./README.ai
from typing import Optional

from pydantic import BaseModel, Field


class SystemConfigBase(BaseModel):
    key: str = Field(..., description="配置键，需全局唯一")
    value: str = Field(..., description="配置值，统一存储为字符串")
    description: Optional[str] = Field(default=None, description="配置用途说明")


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    value: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class SystemConfigRead(SystemConfigBase):
    class Config:
        from_attributes = True
