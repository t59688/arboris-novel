# AIMETA P=提示词模式_提示模板请求响应|R=提示词结构|NR=不含业务逻辑|E=PromptSchema|X=internal|A=Pydantic模式|D=pydantic|S=none|RD=./README.ai
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class PromptBase(BaseModel):
    """Prompt 基础模型。"""

    name: str = Field(..., description="唯一标识，用于代码引用")
    title: Optional[str] = Field(default=None, description="可读标题")
    content: str = Field(..., description="提示词具体内容")
    tags: Optional[List[str]] = Field(default=None, description="标签集合")


class PromptCreate(PromptBase):
    """创建 Prompt 时使用的模型。"""

    pass


class PromptUpdate(BaseModel):
    """更新 Prompt 时使用的模型。"""

    title: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)


class PromptRead(PromptBase):
    """对外暴露的 Prompt 数据结构。"""

    id: int

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj: Any, *args: Any, **kwargs: Any) -> "PromptRead":  # type: ignore[override]
        """在转换 ORM 模型时，将字符串标签拆分为列表。"""
        if hasattr(obj, "id") and hasattr(obj, "name"):
            raw_tags = getattr(obj, "tags", None)
            if isinstance(raw_tags, str):
                processed = [tag for tag in raw_tags.split(",") if tag]
            elif isinstance(raw_tags, list):
                processed = raw_tags
            else:
                processed = None
            data = {
                "id": getattr(obj, "id"),
                "name": getattr(obj, "name"),
                "title": getattr(obj, "title", None),
                "content": getattr(obj, "content", None),
                "tags": processed,
            }
            return super().model_validate(data, *args, **kwargs)
        return super().model_validate(obj, *args, **kwargs)
