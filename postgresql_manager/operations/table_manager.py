# operations/table_manager.py
from sqlalchemy import MetaData, Table, Column, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.schema import CreateTable, DropTable
import logging
from typing import List, Dict, Any, Optional, Set

from postgresql_manager.models.base import Base
from postgresql_manager.models.init import get_all_models
from postgresql_manager.operations.database import DatabaseManager
from postgresql_manager.utils.table_diff import TableDiff


logger = logging.getLogger(__name__)


class TableManager:
    """表管理器 - 处理表的创建、更新、删除等操作"""

    def __init__(self, db_manager: DatabaseManager):
        """
        初始化表管理器

        Args:
            db_manager: 数据库管理器实例
        """
        self.db_manager = db_manager
        self.metadata = Base.metadata
        self.table_diff = TableDiff()

    def create_all_tables(self, group: str = 'all') -> bool:
        """
        创建所有表（如果不存在）

        Args:
            group: 模型分组，可选 'all', 'user', 'product', 'order'

        Returns:
            bool: 是否成功
        """
        try:
            models = get_all_models(group)

            for model in models:
                table_name = model.__tablename__
                if not self.db_manager.table_exists(table_name):
                    try:
                        # 创建表
                        self.metadata.tables[table_name].create(
                            self.db_manager.engine,
                            checkfirst=True
                        )
                        logger.info(f"表 '{table_name}' 创建成功")
                    except Exception as e:
                        logger.error(f"创建表 '{table_name}' 失败: {e}")
                        return False

            logger.info(f"所有表创建完成（分组: {group}）")
            return True

        except Exception as e:
            logger.error(f"创建表失败: {e}")
            return False

    def drop_all_tables(self, group: str = 'all') -> bool:
        """
        删除所有表（如果存在）

        Args:
            group: 模型分组

        Returns:
            bool: 是否成功
        """
        try:
            models = get_all_models(group)

            for model in reversed(models):  # 反向删除，避免外键约束
                table_name = model.__tablename__
                if self.db_manager.table_exists(table_name):
                    try:
                        # 删除表
                        self.metadata.tables[table_name].drop(
                            self.db_manager.engine,
                            checkfirst=True
                        )
                        logger.info(f"表 '{table_name}' 删除成功")
                    except Exception as e:
                        logger.error(f"删除表 '{table_name}' 失败: {e}")
                        return False

            logger.info(f"所有表删除完成（分组: {group}）")
            return True

        except Exception as e:
            logger.error(f"删除表失败: {e}")
            return False

    def create_table(self, model_class) -> bool:
        """
        创建单个表

        Args:
            model_class: 模型类

        Returns:
            bool: 是否成功
        """
        try:
            table_name = model_class.__tablename__

            if self.db_manager.table_exists(table_name):
                logger.warning(f"表 '{table_name}' 已存在")
                return True

            # 创建表
            self.metadata.tables[table_name].create(
                self.db_manager.engine,
                checkfirst=False
            )

            logger.info(f"表 '{table_name}' 创建成功")
            return True

        except Exception as e:
            logger.error(f"创建表失败: {e}")
            return False

    def drop_table(self, model_class) -> bool:
        """
        删除单个表

        Args:
            model_class: 模型类

        Returns:
            bool: 是否成功
        """
        try:
            table_name = model_class.__tablename__

            if not self.db_manager.table_exists(table_name):
                logger.warning(f"表 '{table_name}' 不存在")
                return True

            # 删除表
            self.metadata.tables[table_name].drop(
                self.db_manager.engine,
                checkfirst=False
            )

            logger.info(f"表 '{table_name}' 删除成功")
            return True

        except Exception as e:
            logger.error(f"删除表失败: {e}")
            return False

    def sync_table(self, model_class, update_existing: bool = True) -> Dict[str, Any]:
        """
        同步表结构（如果表不存在则创建，存在则根据配置更新）

        Args:
            model_class: 模型类
            update_existing: 是否更新已存在的表

        Returns:
            Dict: 同步结果
        """
        result = {
            'table_name': model_class.__tablename__,
            'created': False,
            'updated': False,
            'changes': [],
            'errors': []
        }

        try:
            table_name = model_class.__tablename__

            # 检查表是否存在
            if not self.db_manager.table_exists(table_name):
                # 表不存在，直接创建
                if self.create_table(model_class):
                    result['created'] = True
                    logger.info(f"表 '{table_name}' 创建成功")
                else:
                    result['errors'].append("创建表失败")
            elif update_existing:
                # 表存在，检查并更新
                update_result = self.upgrade_table(model_class)
                result['updated'] = update_result['updated']
                result['changes'] = update_result['changes']
                result['errors'] = update_result['errors']
            else:
                logger.info(f"表 '{table_name}' 已存在，跳过更新")

            return result

        except Exception as e:
            error_msg = f"同步表 '{table_name}' 失败: {e}"
            logger.error(error_msg)
            result['errors'].append(error_msg)
            return result

    def upgrade_table(self, model_class) -> Dict[str, Any]:
        """
        升级表结构（添加缺失的列）

        Args:
            model_class: 模型类

        Returns:
            Dict: 升级结果
        """
        result = {
            'table_name': model_class.__tablename__,
            'updated': False,
            'changes': [],
            'errors': []
        }

        try:
            table_name = model_class.__tablename__

            # 获取数据库中的表结构
            db_table_info = self.db_manager.get_table_info(table_name)
            if not db_table_info:
                result['errors'].append(f"表 '{table_name}' 不存在")
                return result

            # 获取模型定义的表结构
            model_table_info = self._get_model_table_info(model_class)

            # 比较差异
            diff_result = self.table_diff.compare_tables(
                db_table_info,
                model_table_info
            )

            if not diff_result['has_changes']:
                logger.info(f"表 '{table_name}' 无需更新")
                return result

            # 应用更改
            if self._apply_table_changes(table_name, diff_result):
                result['updated'] = True
                result['changes'] = diff_result['changes']
                logger.info(f"表 '{table_name}' 更新成功")
            else:
                result['errors'].append("应用更改失败")

            return result

        except Exception as e:
            error_msg = f"升级表 '{table_name}' 失败: {e}"
            logger.error(error_msg)
            result['errors'].append(error_msg)
            return result

    def _get_model_table_info(self, model_class) -> Dict[str, Any]:
        """获取模型定义的表结构信息"""
        table = model_class.__table__

        columns = []
        for column in table.columns:
            columns.append({
                'name': column.name,
                'type': str(column.type),
                'nullable': column.nullable,
                'default': column.default.arg if column.default else None,
                'autoincrement': column.autoincrement,
                'primary_key': column.primary_key
            })

        indexes = []
        for index in table.indexes:
            indexes.append({
                'name': index.name,
                'columns': [c.name for c in index.columns],
                'unique': index.unique
            })

        foreign_keys = []
        for fk in table.foreign_keys:
            foreign_keys.append({
                'name': fk.constraint.name if fk.constraint else None,
                'constrained_columns': [fk.column.name],
                'referred_table': fk.column.table.name,
                'referred_columns': [fk.column.name]
            })

        return {
            'table_name': table.name,
            'columns': columns,
            'indexes': indexes,
            'foreign_keys': foreign_keys
        }

    def _apply_table_changes(self, table_name: str, diff_result: Dict) -> bool:
        """应用表结构更改"""
        try:
            with self.db_manager.get_session() as session:
                # 添加缺失的列
                for column in diff_result.get('columns_to_add', []):
                    sql = f"ALTER TABLE {table_name} ADD COLUMN {column['name']} {column['type']}"
                    if not column['nullable']:
                        sql += " NOT NULL"
                    if column['default'] is not None:
                        sql += f" DEFAULT {column['default']}"

                    session.execute(text(sql))
                    logger.info(f"添加列: {column['name']}")

                # 这里可以扩展支持其他更改（修改列、删除列等）
                # 注意：生产环境中修改列需要谨慎处理

                session.commit()
                return True

        except Exception as e:
            logger.error(f"应用表更改失败: {e}")
            return False

    def truncate_table(self, model_class, cascade: bool = False) -> bool:
        """
        清空表数据

        Args:
            model_class: 模型类
            cascade: 是否级联删除

        Returns:
            bool: 是否成功
        """
        try:
            table_name = model_class.__tablename__

            if not self.db_manager.table_exists(table_name):
                logger.warning(f"表 '{table_name}' 不存在")
                return False

            cascade_sql = " CASCADE" if cascade else ""
            sql = f"TRUNCATE TABLE {table_name}{cascade_sql}"

            with self.db_manager.get_session() as session:
                session.execute(text(sql))
                session.commit()

            logger.info(f"表 '{table_name}' 数据已清空")
            return True

        except Exception as e:
            logger.error(f"清空表数据失败: {e}")
            return False

    def rename_table(self, old_name: str, new_name: str) -> bool:
        """
        重命名表

        Args:
            old_name: 原表名
            new_name: 新表名

        Returns:
            bool: 是否成功
        """
        try:
            if not self.db_manager.table_exists(old_name):
                logger.error(f"原表 '{old_name}' 不存在")
                return False

            if self.db_manager.table_exists(new_name):
                logger.error(f"新表名 '{new_name}' 已存在")
                return False

            sql = f"ALTER TABLE {old_name} RENAME TO {new_name}"

            with self.db_manager.get_session() as session:
                session.execute(text(sql))
                session.commit()

            logger.info(f"表 '{old_name}' 已重命名为 '{new_name}'")
            return True

        except Exception as e:
            logger.error(f"重命名表失败: {e}")
            return False

    def backup_table(self, table_name: str, backup_suffix: str = "_backup") -> bool:
        """
        备份表

        Args:
            table_name: 表名
            backup_suffix: 备份表后缀

        Returns:
            bool: 是否成功
        """
        try:
            if not self.db_manager.table_exists(table_name):
                logger.error(f"表 '{table_name}' 不存在")
                return False

            backup_table = f"{table_name}{backup_suffix}"

            # 检查备份表是否已存在
            if self.db_manager.table_exists(backup_table):
                # 删除已存在的备份
                drop_sql = f"DROP TABLE {backup_table}"
                with self.db_manager.get_session() as session:
                    session.execute(text(drop_sql))

            # 创建备份表
            backup_sql = f"CREATE TABLE {backup_table} AS TABLE {table_name}"

            with self.db_manager.get_session() as session:
                session.execute(text(backup_sql))
                session.commit()

            logger.info(f"表 '{table_name}' 已备份到 '{backup_table}'")
            return True

        except Exception as e:
            logger.error(f"备份表失败: {e}")
            return False