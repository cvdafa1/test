# models/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_mixin, declared_attr
from typing import Optional

# 创建基类
Base = declarative_base()


@declarative_mixin
class BaseMixin:
    """基础混合类，提供通用字段"""

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now,
                        nullable=False, comment="更新时间")

    @declared_attr
    def __tablename__(cls):
        """自动生成表名（类名小写 + 's'）"""
        return cls.__name__.lower() + 's'

    def to_dict(self) -> dict:
        """将模型转换为字典"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result

    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建模型实例"""
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance


class AuditMixin:
    """审计混合类，用于记录操作日志"""
    created_by = Column(Integer, nullable=True, comment="创建人")
    updated_by = Column(Integer, nullable=True, comment="更新人")
    is_deleted = Column(Integer, default=0, comment="软删除标记")