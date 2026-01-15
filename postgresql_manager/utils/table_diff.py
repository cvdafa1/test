# utils/table_diff.py
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class TableDiff:
    """表结构差异对比工具"""

    def compare_tables(self, db_table: Dict, model_table: Dict) -> Dict[str, Any]:
        """
        比较数据库中的表和模型定义的表

        Args:
            db_table: 数据库中的表信息
            model_table: 模型定义的表信息

        Returns:
            Dict: 差异结果
        """
        result = {
            'has_changes': False,
            'changes': [],
            'columns_to_add': [],
            'columns_to_modify': [],
            'columns_to_drop': [],
            'indexes_to_add': [],
            'indexes_to_drop': [],
            'foreign_keys_to_add': [],
            'foreign_keys_to_drop': []
        }

        # 比较列
        column_diff = self._compare_columns(
            db_table.get('columns', []),
            model_table.get('columns', [])
        )

        if column_diff['has_changes']:
            result['has_changes'] = True
            result['changes'].extend(column_diff['changes'])
            result['columns_to_add'] = column_diff['columns_to_add']
            result['columns_to_modify'] = column_diff['columns_to_modify']

        # 比较索引
        index_diff = self._compare_indexes(
            db_table.get('indexes', []),
            model_table.get('indexes', [])
        )

        if index_diff['has_changes']:
            result['has_changes'] = True
            result['changes'].extend(index_diff['changes'])
            result['indexes_to_add'] = index_diff['indexes_to_add']
            result['indexes_to_drop'] = index_diff['indexes_to_drop']

        # 比较外键
        fk_diff = self._compare_foreign_keys(
            db_table.get('foreign_keys', []),
            model_table.get('foreign_keys', [])
        )

        if fk_diff['has_changes']:
            result['has_changes'] = True
            result['changes'].extend(fk_diff['changes'])
            result['foreign_keys_to_add'] = fk_diff['foreign_keys_to_add']
            result['foreign_keys_to_drop'] = fk_diff['foreign_keys_to_drop']

        return result

    def _compare_columns(self, db_columns: List[Dict], model_columns: List[Dict]) -> Dict[str, Any]:
        """比较列差异"""
        result = {
            'has_changes': False,
            'changes': [],
            'columns_to_add': [],
            'columns_to_modify': [],
            'columns_to_drop': []
        }

        db_column_dict = {col['name']: col for col in db_columns}
        model_column_dict = {col['name']: col for col in model_columns}

        # 找出需要添加的列
        for col_name, model_col in model_column_dict.items():
            if col_name not in db_column_dict:
                result['has_changes'] = True
                result['changes'].append(f"需要添加列: {col_name}")
                result['columns_to_add'].append(model_col)

        # 找出需要修改的列
        for col_name, db_col in db_column_dict.items():
            if col_name in model_column_dict:
                model_col = model_column_dict[col_name]
                if not self._columns_equal(db_col, model_col):
                    result['has_changes'] = True
                    result['changes'].append(f"需要修改列: {col_name}")
                    result['columns_to_modify'].append({
                        'old': db_col,
                        'new': model_col
                    })

        return result

    def _columns_equal(self, col1: Dict, col2: Dict) -> bool:
        """比较两个列是否相等（简化版，只比较类型和是否可空）"""
        # 简化比较逻辑，实际使用中可能需要更详细的比较
        type1 = str(col1.get('type', '')).lower()
        type2 = str(col2.get('type', '')).lower()

        # 规范化类型字符串
        type1 = type1.replace('varchar', 'character varying')
        type2 = type2.replace('varchar', 'character varying')

        nullable_equal = col1.get('nullable', True) == col2.get('nullable', True)
        type_equal = type1 == type2

        return nullable_equal and type_equal

    def _compare_indexes(self, db_indexes: List[Dict], model_indexes: List[Dict]) -> Dict[str, Any]:
        """比较索引差异"""
        result = {
            'has_changes': False,
            'changes': [],
            'indexes_to_add': [],
            'indexes_to_drop': []
        }

        db_index_dict = {idx['name']: idx for idx in db_indexes if idx.get('name')}
        model_index_dict = {idx['name']: idx for idx in model_indexes if idx.get('name')}

        # 找出需要添加的索引
        for idx_name, model_idx in model_index_dict.items():
            if idx_name not in db_index_dict:
                result['has_changes'] = True
                result['changes'].append(f"需要添加索引: {idx_name}")
                result['indexes_to_add'].append(model_idx)

        # 找出需要删除的索引
        for idx_name, db_idx in db_index_dict.items():
            if idx_name not in model_index_dict:
                result['has_changes'] = True
                result['changes'].append(f"需要删除索引: {idx_name}")
                result['indexes_to_drop'].append(db_idx)

        return result

    def _compare_foreign_keys(self, db_fks: List[Dict], model_fks: List[Dict]) -> Dict[str, Any]:
        """比较外键差异"""
        result = {
            'has_changes': False,
            'changes': [],
            'foreign_keys_to_add': [],
            'foreign_keys_to_drop': []
        }

        # 简化比较：按名称比较
        db_fk_names = {fk.get('name', '') for fk in db_fks if fk.get('name')}
        model_fk_names = {fk.get('name', '') for fk in model_fks if fk.get('name')}

        # 找出需要添加的外键
        for fk_name in model_fk_names - db_fk_names:
            result['has_changes'] = True
            result['changes'].append(f"需要添加外键: {fk_name}")
            # 这里可以添加更详细的外键信息

        # 找出需要删除的外键
        for fk_name in db_fk_names - model_fk_names:
            result['has_changes'] = True
            result['changes'].append(f"需要删除外键: {fk_name}")

        return result