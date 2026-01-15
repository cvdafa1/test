# main.py
import logging
from datetime import datetime
from operations.database import DatabaseManager
from operations.table_manager import TableManager
from config import db_config, table_config
from postgresql_manager.models.address import Address
from postgresql_manager.models.category import Category
from postgresql_manager.models.order import Order, OrderItem
from postgresql_manager.models.product import Product, ProductStatus
from postgresql_manager.models.user import User, UserRole, UserStatus
from postgresql_manager.operations.data_operations import CategoryOperations

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_database():
    """设置数据库"""
    logger.info("开始设置数据库...")

    # 创建数据库管理器
    db_manager = DatabaseManager()

    try:
        # 连接数据库
        if not db_manager.connect(echo=False):
            logger.error("数据库连接失败")
            return None

        # 创建表管理器
        table_manager = TableManager(db_manager)

        # 检查表是否存在并创建
        logger.info("检查并创建表...")

        # 同步所有表
        models_to_sync = [User, Address, Category, Product, Order, OrderItem]

        for model in models_to_sync:
            table_name = model.__tablename__
            logger.info(f"同步表: {table_name}")

            result = table_manager.sync_table(
                model,
                update_existing=table_config.auto_upgrade_tables
            )

            if result['created']:
                logger.info(f"  ✓ 表 '{table_name}' 已创建")
            elif result['updated']:
                logger.info(f"  ↻ 表 '{table_name}' 已更新，变更: {len(result['changes'])}")
                for change in result['changes']:
                    logger.info(f"    - {change}")
            elif not result['errors']:
                logger.info(f"  ✓ 表 '{table_name}' 已存在，无需更新")
            else:
                for error in result['errors']:
                    logger.error(f"  ✗ {error}")

        # 显示数据库信息
        db_info = db_manager.get_database_size()
        if db_info:
            logger.info(f"数据库大小: {db_info.get('db_size_pretty', 'N/A')}")
            logger.info(f"表数量: {db_info.get('table_count', 0)}")

        return db_manager

    except Exception as e:
        logger.error(f"设置数据库失败: {e}")
        return None


def demo_data_operations(db_manager: DatabaseManager):
    """演示数据操作"""
    logger.info("\n演示数据操作...")

    from operations.data_operations import UserOperations, ProductOperations, OrderOperations

    try:
        # 用户操作
        user_ops = UserOperations(db_manager)

        # 创建用户
        user_data = {
            'username': 'user1',
            'email': 'demo@example.com',
            'password_hash': 'hashed_password_123',
            'nickname': '演示用户',
            'role': UserRole.USER,
            'status': UserStatus.ACTIVE
        }

        user = user_ops.create_user(user_data)
        if user:
            logger.info(f"创建用户成功: {user.username}")

        # 查询用户
        users = user_ops.get_users()
        logger.info(f"查询到 {len(users)} 个用户")

        # 产品操作
        category_ops = CategoryOperations(db_manager)

        # 创建分类
        category_data = {
            'name': '电子产品',
            'description': '电子设备分类',
            'is_active': True
        }

        category = category_ops.create_category(category_data)

        if category:
            # 创建产品
            product_data = {
                'name': '智能手机',
                'sku': 'SMART-PHONE-002',
                'price': 2999.99,
                'stock_quantity': 100,
                'category_id': category.id,
                'short_description': '高性能智能手机',
                'status': ProductStatus.DRAFT
            }
            product_ops = ProductOperations(db_manager)
            product = product_ops.create_product(product_data)
            if product:
                logger.info(f"创建产品成功: {product.name}")

        # 订单操作
        order_ops = OrderOperations(db_manager)

        if user and product:
            # 创建订单
            order_data = {
                'order_number': f'ORD{datetime.now().strftime("%Y%m%d%H%M%S")}',
                'user_id': user.id,
                'subtotal': 2999.99,
                'total_amount': 2999.99,
                'shipping_address': {
                    'recipient': '张三',
                    'phone': '13800138000',
                    'address': '北京市朝阳区'
                }
            }

            order = order_ops.create_order(order_data)
            if order:
                logger.info(f"创建订单成功: {order.order_number}")

                # 添加订单项
                order_item_data = {
                    'order_id': order.id,
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_sku': product.sku,
                    'unit_price': product.price,
                    'quantity': 1,
                    'subtotal': product.price
                }

                order_item = order_ops.create_order_item(order_item_data)
                if order_item:
                    logger.info(f"添加订单项成功: {order_item.product_name}")

    except Exception as e:
        logger.error(f"数据操作演示失败: {e}")


def demo_table_management(db_manager: DatabaseManager):
    """演示表管理功能"""
    logger.info("\n演示表管理功能...")

    from operations.table_manager import TableManager
    table_manager = TableManager(db_manager)

    try:
        # 获取所有表
        tables = db_manager.get_table_names()
        logger.info(f"数据库中的表: {tables}")

        # 获取表信息
        for table_name in ['users', 'products']:
            if db_manager.table_exists(table_name):
                table_info = db_manager.get_table_info(table_name)
                if table_info:
                    logger.info(f"\n表 '{table_name}' 结构:")
                    for column in table_info['columns']:
                        logger.info(f"  - {column['name']}: {column['type']}")

        # 备份表
        logger.info("\n备份 users 表...")
        if table_manager.backup_table('users'):
            logger.info("表备份成功")

        # # 清空表数据
        # logger.info("\n清空 products 表数据...")
        # if table_manager.truncate_table(Product, cascade=True):
        #     logger.info("表数据已清空")

    except Exception as e:
        logger.error(f"表管理演示失败: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("PostgreSQL 表管理器")
    print("=" * 60)

    # 显示配置
    print(f"\n数据库配置:")
    print(f"  主机: {db_config.host}:{db_config.port}")
    print(f"  数据库: {db_config.database}")
    print(f"  用户: {db_config.user}")

    print(f"\n表配置:")
    print(f"  自动创建表: {table_config.auto_create_tables}")
    print(f"  自动更新表: {table_config.auto_upgrade_tables}")

    # 设置数据库
    db_manager = setup_database()

    if db_manager:
        try:
            # 演示数据操作
            demo_data_operations(db_manager)

            # 演示表管理
            demo_table_management(db_manager)

            print("\n" + "=" * 60)
            print("数据库设置完成！")
            print("=" * 60)

        finally:
            # 断开连接
            db_manager.disconnect()
            print("\n数据库连接已关闭")
    else:
        print("\n数据库设置失败，请检查配置和连接")


if __name__ == "__main__":
    main()