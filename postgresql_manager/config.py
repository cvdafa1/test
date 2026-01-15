# config.py
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class DatabaseConfig:
    """数据库配置类"""
    host= "localhost"
    port= "5432"
    user= "postgres"
    password= "123456"
    database= "myapp_db"

    @property
    def connection_string(self) -> str:
        """获取连接字符串"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def connection_params(self) -> Dict[str, Any]:
        """获取连接参数字典"""
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database
        }


@dataclass
class TableConfig:
    """表配置类"""
    auto_create_tables: bool = True
    auto_upgrade_tables: bool = True
    drop_existing: bool = False
    verbose: bool = True


# 创建配置实例
db_config = DatabaseConfig()
table_config = TableConfig()