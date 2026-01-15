# models/category.py
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base, BaseMixin


class Category(Base, BaseMixin):
    """分类表模型"""
    __tablename__ = "categories"
    __table_args__ = {'comment': '产品分类表'}

    # 分类信息
    name = Column(String(100), nullable=False, index=True, comment="分类名称")
    slug = Column(String(100), unique=True, nullable=True, comment="URL友好名称")
    description = Column(Text, nullable=True, comment="分类描述")

    # 树形结构
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True,
                       index=True, comment="父分类ID")

    # 显示设置
    image = Column(String(500), nullable=True, comment="分类图片")
    display_order = Column(Integer, default=0, comment="显示顺序")
    is_active = Column(Boolean, default=True, comment="是否启用")

    # SEO
    meta_title = Column(String(200), nullable=True, comment="SEO标题")
    meta_description = Column(Text, nullable=True, comment="SEO描述")
    meta_keywords = Column(Text, nullable=True, comment="SEO关键词")

    # 扩展
    attributes = Column(JSONB, nullable=True, default=dict, comment="扩展属性")

    # 关系
    parent = relationship("Category", remote_side="Category.id",
                          back_populates="children")
    children = relationship("Category", back_populates="parent",
                            cascade="all, delete-orphan")
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"