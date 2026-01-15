# operations/database.py
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
from typing import List, Optional, Dict, Any
from postgresql_manager.config import db_config
from postgresql_manager.models.base import Base
from postgresql_manager.models.init import get_all_models

logger = logging.getLogger(__name__)


class DatabaseManager:
    """数据库管理器"""

    def __init__(self, connection_string: Optional[str] = None):
        """
        初始化数据库管理器

        Args:
            connection_string: 数据库连接字符串，如果为None则使用配置中的
        """
        self.connection_string = connection_string or db_config.connection_string
        self.engine = None
        self.session_factory = None
        self.Session = None
        self._connected = False

    def connect(self, echo: bool = False, pool_size: int = 5, max_overflow: int = 10) -> bool:
        """
        连接到数据库

        Args:
            echo: 是否输出SQL日志
            pool_size: 连接池大小
            max_overflow: 最大溢出连接数

        Returns:
            bool: 连接是否成功
        """
        try:
            # 创建引擎
            self.engine = create_engine(
                self.connection_string,
                echo=echo,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_pre_ping=True,  # 连接前ping检查
                pool_recycle=3600,  # 连接回收时间（秒）
            )

            # 创建会话工厂
            self.session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
            self.Session = scoped_session(self.session_factory)

            # 测试连接
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            self._connected = True
            logger.info("数据库连接成功")
            return True

        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            self._connected = False
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.Session:
            self.Session.remove()
        if self.engine:
            self.engine.dispose()
        self._connected = False
        logger.info("数据库连接已断开")

    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self._connected

    @contextmanager
    def get_session(self):
        """
        获取数据库会话上下文管理器

        使用示例:
        with db.get_session() as session:
            user = session.query(User).first()
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            session.close()

    def execute_raw_sql(self, sql: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        执行原生SQL查询

        Args:
            sql: SQL语句
            params: 参数

        Returns:
            List[Dict]: 查询结果
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), params or {})
                if result.returns_rows:
                    return [dict(row._mapping) for row in result]
                return []
        except Exception as e:
            logger.error(f"执行SQL失败: {e}")
            raise

    def get_table_names(self) -> List[str]:
        """获取数据库中所有表名"""
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            logger.error(f"获取表名失败: {e}")
            return []

    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        try:
            inspector = inspect(self.engine)
            return inspector.has_table(table_name)
        except Exception as e:
            logger.error(f"检查表存在失败: {e}")
            return False

    def get_table_info(self, table_name: str) -> Optional[Dict]:
        """获取表结构信息"""
        try:
            inspector = inspect(self.engine)

            if not inspector.has_table(table_name):
                return None

            # 获取列信息
            columns = []
            for column in inspector.get_columns(table_name):
                columns.append({
                    'name': column['name'],
                    'type': str(column['type']),
                    'nullable': column.get('nullable', True),
                    'default': column.get('default'),
                    'autoincrement': column.get('autoincrement', False),
                    'primary_key': column.get('primary_key', False)
                })

            # 获取索引信息
            indexes = []
            for index in inspector.get_indexes(table_name):
                indexes.append({
                    'name': index['name'],
                    'columns': index['column_names'],
                    'unique': index.get('unique', False)
                })

            # 获取外键信息
            foreign_keys = []
            for fk in inspector.get_foreign_keys(table_name):
                foreign_keys.append({
                    'name': fk.get('name'),
                    'constrained_columns': fk['constrained_columns'],
                    'referred_table': fk['referred_table'],
                    'referred_columns': fk['referred_columns']
                })

            return {
                'table_name': table_name,
                'columns': columns,
                'indexes': indexes,
                'foreign_keys': foreign_keys
            }

        except Exception as e:
            logger.error(f"获取表信息失败: {e}")
            return None

    def get_database_size(self) -> Dict[str, Any]:
        """获取数据库大小信息"""
        try:
            sql = """
            SELECT 
                pg_database_size(current_database()) as db_size,
                pg_size_pretty(pg_database_size(current_database())) as db_size_pretty,
                (SELECT COUNT(*) FROM information_schema.tables 
                 WHERE table_schema = 'public') as table_count
            """
            result = self.execute_raw_sql(sql)
            return result[0] if result else {}
        except Exception as e:
            logger.error(f"获取数据库大小失败: {e}")
            return {}