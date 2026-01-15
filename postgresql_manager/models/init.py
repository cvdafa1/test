# models/__init__.py
"""
数据库模型初始化
"""
from .base import Base, BaseMixin, AuditMixin
from .user import User, UserRole, UserStatus
from .address import Address, AddressType
from .category import Category
from .product import Product, ProductStatus
from .order import Order, OrderItem, OrderStatus, PaymentStatus, ShippingStatus

# 所有模型的列表
__all__ = [
    # 基础
    'Base',
    'BaseMixin',
    'AuditMixin',

    # 用户模块
    'User',
    'UserRole',
    'UserStatus',
    'Address',
    'AddressType',

    # 商品模块
    'Category',
    'Product',
    'ProductStatus',

    # 订单模块
    'Order',
    'OrderItem',
    'OrderStatus',
    'PaymentStatus',
    'ShippingStatus',
]

# 按模块分组的模型
MODEL_GROUPS = {
    'user': [User, Address],
    'product': [Category, Product],
    'order': [Order, OrderItem],
    'all': [User, Address, Category, Product, Order, OrderItem]
}


def get_all_models(group='all'):
    """获取指定组的模型列表"""
    return MODEL_GROUPS.get(group, MODEL_GROUPS['all'])