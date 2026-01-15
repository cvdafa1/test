# models/product.py
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
import enum
from decimal import Decimal
from .base import Base, BaseMixin, AuditMixin


class ProductStatus(enum.Enum):
    """产品状态枚举"""
    DRAFT = "draft"
    PUBLISHED = "published"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class Product(Base, BaseMixin, AuditMixin):
    """产品表模型"""
    __tablename__ = "products"
    __table_args__ = {'comment': '产品表'}

    # 产品基本信息
    sku = Column(String(50), unique=True, nullable=False, index=True, comment="SKU编码")
    name = Column(String(200), nullable=False, index=True, comment="产品名称")
    slug = Column(String(200), unique=True, nullable=True, comment="URL友好名称")

    # 分类信息
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True,
                         index=True, comment="分类ID")

    # 价格信息
    price = Column(Float(10, 2), nullable=False, comment="售价")
    cost_price = Column(Float(10, 2), nullable=True, comment="成本价")
    original_price = Column(Float(10, 2), nullable=True, comment="原价")

    # 库存信息
    stock_quantity = Column(Integer, default=0, nullable=False, comment="库存数量")
    low_stock_threshold = Column(Integer, default=10, comment="低库存阈值")
    manage_stock = Column(Boolean, default=True, comment="是否管理库存")

    # 产品详情
    short_description = Column(Text, nullable=True, comment="简短描述")
    description = Column(Text, nullable=True, comment="详细描述")
    specifications = Column(JSONB, nullable=True, default=dict, comment="规格参数")

    # 多媒体
    main_image = Column(String(500), nullable=True, comment="主图")
    images = Column(JSONB, nullable=True, default=list, comment="产品图集")

    # 状态
    status = Column(Enum(ProductStatus), default=ProductStatus.DRAFT,
                    nullable=False, comment="产品状态")
    is_featured = Column(Boolean, default=False, comment="是否推荐")
    is_virtual = Column(Boolean, default=False, comment="是否虚拟产品")

    # 物流信息
    weight = Column(Float, nullable=True, comment="重量(kg)")
    dimensions = Column(JSONB, nullable=True, comment="尺寸")

    # SEO
    meta_title = Column(String(200), nullable=True, comment="SEO标题")
    meta_description = Column(Text, nullable=True, comment="SEO描述")
    meta_keywords = Column(Text, nullable=True, comment="SEO关键词")

    # 统计
    view_count = Column(Integer, default=0, comment="浏览数")
    sales_count = Column(Integer, default=0, comment="销量")

    # 关系
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"