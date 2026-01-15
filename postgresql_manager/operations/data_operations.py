# operations/data_operations.py
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_, desc, asc, func
import logging

from postgresql_manager.models.address import Address
from postgresql_manager.models.category import Category
from postgresql_manager.models.order import Order, OrderItem, OrderStatus, PaymentStatus, ShippingStatus
from postgresql_manager.models.product import Product, ProductStatus
from postgresql_manager.models.user import User, UserRole, UserStatus
from postgresql_manager.operations.database import DatabaseManager

logger = logging.getLogger(__name__)


class BaseOperations:
    """基础数据操作类"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def _get_session(self):
        """获取数据库会话"""
        return self.db_manager.Session()


class UserOperations(BaseOperations):
    """用户数据操作"""

    def create_user(self, user_data: Dict[str, Any]) -> Optional[User]:
        """创建用户"""
        try:
            with self.db_manager.get_session() as session:
                # 检查用户名和邮箱是否已存在
                existing = session.query(User).filter(
                    or_(
                        User.username == user_data.get('username'),
                        User.email == user_data.get('email')
                    )
                ).first()

                if existing:
                    logger.warning(f"用户已存在: {user_data.get('username')}")
                    return None

                # 创建用户实例
                user = User(**user_data)
                session.add(user)
                session.commit()

                logger.info(f"创建用户成功: {user.username}")
                return user

        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        try:
            with self.db_manager.get_session() as session:
                return session.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"获取用户失败: {e}")
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        try:
            with self.db_manager.get_session() as session:
                return session.query(User).filter(User.username == username).first()
        except Exception as e:
            logger.error(f"获取用户失败: {e}")
            return None

    def get_users(self, page: int = 1, per_page: int = 20,
                  status: Optional[str] = None,
                  role: Optional[str] = None) -> List[User]:
        """获取用户列表"""
        try:
            with self.db_manager.get_session() as session:
                query = session.query(User)

                # 添加过滤条件
                if status:
                    query = query.filter(User.status == UserStatus(status))
                if role:
                    query = query.filter(User.role == UserRole(role))

                # 分页
                offset = (page - 1) * per_page
                users = query.order_by(User.created_at.desc()) \
                    .offset(offset) \
                    .limit(per_page) \
                    .all()

                return users

        except Exception as e:
            logger.error(f"获取用户列表失败: {e}")
            return []

    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> bool:
        """更新用户"""
        try:
            with self.db_manager.get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    logger.warning(f"用户不存在: {user_id}")
                    return False

                # 更新字段
                for key, value in update_data.items():
                    if hasattr(user, key) and key not in ['id', 'created_at']:
                        setattr(user, key, value)

                session.commit()
                logger.info(f"更新用户成功: {user_id}")
                return True

        except Exception as e:
            logger.error(f"更新用户失败: {e}")
            return False

    def delete_user(self, user_id: int, soft_delete: bool = True) -> bool:
        """删除用户"""
        try:
            with self.db_manager.get_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    logger.warning(f"用户不存在: {user_id}")
                    return False

                if soft_delete:
                    # 软删除
                    user.is_deleted = 1
                    user.status = UserStatus.DELETED
                    logger.info(f"软删除用户: {user_id}")
                else:
                    # 硬删除
                    session.delete(user)
                    logger.info(f"硬删除用户: {user_id}")

                session.commit()
                return True

        except Exception as e:
            logger.error(f"删除用户失败: {e}")
            return False

    def search_users(self, keyword: str, page: int = 1, per_page: int = 20) -> List[User]:
        """搜索用户"""
        try:
            with self.db_manager.get_session() as session:
                query = session.query(User).filter(
                    or_(
                        User.username.ilike(f"%{keyword}%"),
                        User.email.ilike(f"%{keyword}%"),
                        User.nickname.ilike(f"%{keyword}%"),
                        User.real_name.ilike(f"%{keyword}%")
                    )
                )

                offset = (page - 1) * per_page
                users = query.order_by(User.created_at.desc()) \
                    .offset(offset) \
                    .limit(per_page) \
                    .all()

                return users

        except Exception as e:
            logger.error(f"搜索用户失败: {e}")
            return []

    def get_user_statistics(self) -> Dict[str, Any]:
        """获取用户统计信息"""
        try:
            with self.db_manager.get_session() as session:
                stats = {}

                # 总用户数
                stats['total'] = session.query(func.count(User.id)).scalar()

                # 按状态统计
                status_stats = session.query(
                    User.status,
                    func.count(User.id)
                ).group_by(User.status).all()
                stats['by_status'] = {status.value: count for status, count in status_stats}

                # 按角色统计
                role_stats = session.query(
                    User.role,
                    func.count(User.id)
                ).group_by(User.role).all()
                stats['by_role'] = {role.value: count for role, count in role_stats}

                # 今日新增用户
                today = func.date(User.created_at)
                today_count = session.query(func.count(User.id)) \
                    .filter(today == func.current_date()) \
                    .scalar()
                stats['today_new'] = today_count

                return stats

        except Exception as e:
            logger.error(f"获取用户统计失败: {e}")
            return {}


class ProductOperations(BaseOperations):
    """产品数据操作"""

    def create_product(self, product_data: Dict[str, Any]) -> Optional[Product]:
        """创建产品"""
        try:
            with self.db_manager.get_session() as session:
                # 检查SKU是否已存在
                if 'sku' in product_data:
                    existing = session.query(Product).filter(
                        Product.sku == product_data['sku']
                    ).first()

                    if existing:
                        logger.warning(f"产品SKU已存在: {product_data['sku']}")
                        return None

                # 创建产品实例
                product = Product(**product_data)
                session.add(product)
                session.commit()

                logger.info(f"创建产品成功: {product.name} (SKU: {product.sku})")
                return product

        except Exception as e:
            logger.error(f"创建产品失败: {e}")
            return None

    def get_products(self, category_id: Optional[int] = None,
                     status: Optional[str] = None,
                     page: int = 1, per_page: int = 20) -> List[Product]:
        """获取产品列表"""
        try:
            with self.db_manager.get_session() as session:
                query = session.query(Product)

                # 添加过滤条件
                if category_id:
                    query = query.filter(Product.category_id == category_id)
                if status:
                    query = query.filter(Product.status == ProductStatus(status))

                # 分页
                offset = (page - 1) * per_page
                products = query.order_by(Product.created_at.desc()) \
                    .offset(offset) \
                    .limit(per_page) \
                    .all()

                return products

        except Exception as e:
            logger.error(f"获取产品列表失败: {e}")
            return []

    def update_product_stock(self, product_id: int, quantity_change: int) -> bool:
        """更新产品库存"""
        try:
            with self.db_manager.get_session() as session:
                product = session.query(Product).filter(Product.id == product_id).first()
                if not product:
                    logger.warning(f"产品不存在: {product_id}")
                    return False

                # 计算新库存
                new_stock = product.stock_quantity + quantity_change
                if new_stock < 0:
                    logger.warning(
                        f"库存不足: 产品 {product_id}, 当前库存 {product.stock_quantity}, 需要 {quantity_change}")
                    return False

                product.stock_quantity = new_stock
                session.commit()

                logger.info(f"更新产品库存成功: 产品 {product_id}, 新库存 {new_stock}")
                return True

        except Exception as e:
            logger.error(f"更新产品库存失败: {e}")
            return False


class OrderOperations(BaseOperations):
    """订单数据操作"""

    def create_order(self, order_data: Dict[str, Any]) -> Optional[Order]:
        """创建订单"""
        try:
            with self.db_manager.get_session() as session:
                # 创建订单实例
                order = Order(**order_data)
                session.add(order)
                session.commit()

                logger.info(f"创建订单成功: {order.order_number}")
                return order

        except Exception as e:
            logger.error(f"创建订单失败: {e}")
            return None

    def create_order_item(self, order_item_data: Dict[str, Any]) -> Optional[OrderItem]:
        """创建订单项"""
        try:
            with self.db_manager.get_session() as session:
                # 创建订单项实例
                order_item = OrderItem(**order_item_data)
                session.add(order_item)
                session.commit()

                # 更新产品库存
                product_id = order_item_data.get('product_id')
                quantity = order_item_data.get('quantity', 1)

                if product_id and quantity > 0:
                    # 这里可以调用 ProductOperations 来更新库存
                    pass

                logger.info(f"创建订单项成功: 订单 {order_item.order_id}, 产品 {order_item.product_name}")
                return order_item

        except Exception as e:
            logger.error(f"创建订单项失败: {e}")
            return None


class CategoryOperations(BaseOperations):
    """分类数据操作"""

    def create_category(self, category_data: Dict[str, Any]) -> Optional[Category]:
        """创建分类"""
        try:
            with self.db_manager.get_session() as session:
                # 创建分类实例
                category = Category(**category_data)
                session.add(category)
                session.commit()

                logger.info(f"创建分类成功: {category.name}")
                return category

        except Exception as e:
            logger.error(f"创建分类失败: {e}")
            return None

    def get_categories_tree(self, parent_id: Optional[int] = None) -> List[Dict]:
        """获取分类树"""
        try:
            with self.db_manager.get_session() as session:
                query = session.query(Category).filter(Category.parent_id == parent_id)
                categories = query.order_by(Category.display_order).all()

                result = []
                for category in categories:
                    category_dict = category.to_dict()
                    # 递归获取子分类
                    children = self.get_categories_tree(category.id)
                    if children:
                        category_dict['children'] = children
                    result.append(category_dict)

                return result

        except Exception as e:
            logger.error(f"获取分类树失败: {e}")
            return []