# AIMETA P=ORM基类_SQLAlchemy声明基类|R=声明基类_元数据|NR=不含具体表定义|E=Base|X=internal|A=Base类|D=sqlalchemy|S=none|RD=./README.ai
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """SQLAlchemy 基类，自动根据类名生成表名。"""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()
