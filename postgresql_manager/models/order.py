# models/order.py
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum
from datetime import datetime
from decimal import Decimal
from .base import Base, BaseMixin


class OrderStatus(enum.Enum):
    """订单状态枚举"""
    PENDING = "pending"  # 待支付
    PROCESSING = "processing"  # 处理中
    SHIPPED = "shipped"  # 已发货
    DELIVERED = "delivered"  # 已送达
    CANCELLED = "cancelled"  # 已取消
    REFUNDED = "refunded"  # 已退款
    COMPLETED = "completed"  # 已完成


class PaymentStatus(enum.Enum):
    """支付状态枚举"""
    UNPAID = "unpaid"  # 未支付
    PAID = "paid"  # 已支付
    FAILED = "failed"  # 支付失败
    REFUNDED = "refunded"  # 已退款
    PARTIALLY_REFUNDED = "partially_refunded"  # 部分退款


class ShippingStatus(enum.Enum):
    """发货状态枚举"""
    NOT_SHIPPED = "not_shipped"  # 未发货
    SHIPPED = "shipped"  # 已发货
    DELIVERED = "delivered"  # 已送达
    RETURNED = "returned"  # 已退回


class Order(Base, BaseMixin):
    """订单表模型"""
    __tablename__ = "orders"
    __table_args__ = {'comment': '订单表'}

    # 订单信息
    order_number = Column(String(50), unique=True, nullable=False,
                          index=True, comment="订单号")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False,
                     index=True, comment="用户ID")

    # 金额信息
    subtotal = Column(Float(10, 2), nullable=False, comment="商品小计")
    shipping_fee = Column(Float(10, 2), default=0.0, comment="运费")
    discount = Column(Float(10, 2), default=0.0, comment="折扣")
    tax = Column(Float(10, 2), default=0.0, comment="税费")
    total_amount = Column(Float(10, 2), nullable=False, comment="订单总额")
    amount_paid = Column(Float(10, 2), default=0.0, comment="已支付金额")

    # 状态
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING,
                    nullable=False, comment="订单状态")
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.UNPAID,
                            nullable=False, comment="支付状态")
    shipping_status = Column(Enum(ShippingStatus), default=ShippingStatus.NOT_SHIPPED,
                             nullable=False, comment="发货状态")

    # 支付信息
    payment_method = Column(String(50), nullable=True, comment="支付方式")
    payment_id = Column(String(100), nullable=True, comment="支付ID")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")

    # 收货信息
    shipping_address = Column(JSONB, nullable=False, comment="收货地址")
    shipping_method = Column(String(50), nullable=True, comment="配送方式")
    tracking_number = Column(String(100), nullable=True, comment="物流单号")
    shipped_at = Column(DateTime, nullable=True, comment="发货时间")
    delivered_at = Column(DateTime, nullable=True, comment="送达时间")

    # 客户信息
    customer_note = Column(Text, nullable=True, comment="客户备注")
    admin_note = Column(Text, nullable=True, comment="管理员备注")

    # 发票信息
    invoice_needed = Column(Integer, default=0, comment="是否需要发票")
    invoice_info = Column(JSONB, nullable=True, comment="发票信息")

    # 关系
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order",
                         cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}')>"


class OrderItem(Base, BaseMixin):
    """订单项表模型"""
    __tablename__ = "order_items"
    __table_args__ = {'comment': '订单项表'}

    # 关联信息
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False,
                      index=True, comment="订单ID")
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False,
                        index=True, comment="产品ID")

    # 产品信息
    product_name = Column(String(200), nullable=False, comment="产品名称")
    product_sku = Column(String(50), nullable=False, comment="产品SKU")
    product_image = Column(String(500), nullable=True, comment="产品图片")

    # 价格和数量
    unit_price = Column(Float(10, 2), nullable=False, comment="单价")
    quantity = Column(Integer, nullable=False, default=1, comment="数量")
    subtotal = Column(Float(10, 2), nullable=False, comment="小计")

    # 折扣
    discount_amount = Column(Float(10, 2), default=0.0, comment="折扣金额")

    # 扩展
    attributes = Column(JSONB, nullable=True, default=dict, comment="产品属性")

    # 关系
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product='{self.product_name}')>"