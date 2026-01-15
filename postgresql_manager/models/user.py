# models/user.py
from sqlalchemy import Column, String, Integer, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import enum
from datetime import datetime
from .base import Base, BaseMixin, AuditMixin
import uuid


class UserRole(enum.Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    MANAGER = "manager"


class UserStatus(enum.Enum):
    """用户状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class User(Base, BaseMixin, AuditMixin):
    """用户表模型"""
    __tablename__ = "users"
    __table_args__ = {
        'comment': '用户表',
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    # 用户唯一标识
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4,
                  nullable=False, comment="用户UUID")

    # 基本信息
    username = Column(String(50), unique=True, nullable=False, index=True,
                      comment="用户名")
    email = Column(String(100), unique=True, nullable=False, index=True,
                   comment="邮箱")
    phone = Column(String(20), nullable=True, unique=True, comment="手机号")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")

    # 个人信息
    nickname = Column(String(50), nullable=True, comment="昵称")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    avatar = Column(String(500), nullable=True, comment="头像URL")
    gender = Column(Enum('male', 'female', 'other', name="gender_enum"),
                    nullable=True, comment="性别")
    birthday = Column(String(20), nullable=True, comment="生日")

    # 账户信息
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False,
                  comment="用户角色")
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False,
                    comment="用户状态")
    is_verified = Column(Boolean, default=False, comment="是否验证")
    is_superuser = Column(Boolean, default=False, comment="是否超级用户")

    # 登录信息
    last_login = Column(String(30), nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(45), nullable=True, comment="最后登录IP")
    login_count = Column(Integer, default=0, comment="登录次数")

    # 扩展信息
    bio = Column(Text, nullable=True, comment="个人简介")
    website = Column(String(500), nullable=True, comment="个人网站")
    location = Column(String(100), nullable=True, comment="所在地")
    company = Column(String(100), nullable=True, comment="公司")

    # JSON 扩展字段
    preferences = Column(JSONB, nullable=True, default=dict, comment="用户偏好")

    # 关系
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    @classmethod
    def get_columns_info(cls) -> dict:
        """获取表的列信息"""
        columns_info = {}
        for column in cls.__table__.columns:
            columns_info[column.name] = {
                'type': str(column.type),
                'nullable': column.nullable,
                'default': column.default.arg if column.default else None,
                'primary_key': column.primary_key,
                'unique': column.unique,
                'comment': column.comment
            }
        return columns_info