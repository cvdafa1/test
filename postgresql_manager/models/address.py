# models/address.py
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base, BaseMixin
import enum


class AddressType(enum.Enum):
    """地址类型枚举"""
    HOME = "home"
    WORK = "work"
    BILLING = "billing"
    SHIPPING = "shipping"
    OTHER = "other"


class Address(Base, BaseMixin):
    """地址表模型"""
    __tablename__ = "addresses"
    __table_args__ = {'comment': '用户地址表'}

    # 外键
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False, index=True, comment="用户ID")

    # 地址信息
    address_type = Column(Enum(AddressType), default=AddressType.HOME,
                          nullable=False, comment="地址类型")
    recipient = Column(String(50), nullable=False, comment="收件人")
    phone = Column(String(20), nullable=False, comment="联系电话")

    # 详细地址
    country = Column(String(50), nullable=False, default="中国", comment="国家")
    province = Column(String(50), nullable=False, comment="省份")
    city = Column(String(50), nullable=False, comment="城市")
    district = Column(String(50), nullable=True, comment="区县")
    street = Column(String(200), nullable=False, comment="街道地址")
    postal_code = Column(String(20), nullable=True, comment="邮政编码")

    # 地址标签
    is_default = Column(Boolean, default=False, comment="是否默认地址")
    label = Column(String(50), nullable=True, comment="地址标签（家、公司等）")

    # 坐标
    latitude = Column(String(20), nullable=True, comment="纬度")
    longitude = Column(String(20), nullable=True, comment="经度")

    # 关系
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(id={self.id}, recipient='{self.recipient}')>"