from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# 1. 数据库连接配置
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/mydb"
# 请将 username, password, mydatabase 替换为你的实际配置

# 2. 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)  # echo=True 会打印SQL语句

# 3. 创建基类
Base = declarative_base()


# 4. 定义数据模型（表结构）
class SimpleMessage(Base):
    """简单的消息表"""
    __tablename__ = "simple_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    msg = Column(String(500), nullable=False)  # 消息内容

    def __repr__(self):
        return f"<Message(id={self.id}, msg='{self.msg[:20]}...')>"


# 5. 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 6. 创建表
def create_tables():
    """创建数据库表"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 表创建成功！")
    except Exception as e:
        print(f"❌ 创建表失败: {e}")


# 7. CRUD 操作函数
def create_message(db, message_text):
    """创建新消息"""
    try:
        new_message = SimpleMessage(msg=message_text)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        print(f"✅ 创建成功: ID={new_message.id}")
        return new_message
    except Exception as e:
        db.rollback()
        print(f"❌ 创建失败: {e}")
        return None


def get_message_by_id(db, message_id):
    """根据ID查询消息"""
    try:
        message = db.query(SimpleMessage).filter(SimpleMessage.id == message_id).first()
        if message:
            print(f"✅ 查询成功: {message}")
        else:
            print(f"⚠️ 未找到ID={message_id}的消息")
        return message
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return None


def get_all_messages(db):
    """查询所有消息"""
    try:
        messages = db.query(SimpleMessage.msg).all()
        print(f"✅ 查询到 {len(messages)} 条消息")
        messages = [list(msg) for msg in messages]
        return messages
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return []


def update_message(db, message_id, new_msg):
    """更新消息"""
    try:
        message = get_message_by_id(db, message_id)
        if message:
            message.msg = new_msg
            db.commit()
            print(f"✅ 更新成功: ID={message_id}")
            return message
        return None
    except Exception as e:
        db.rollback()
        print(f"❌ 更新失败: {e}")
        return None


def delete_message(db, message_id):
    """删除消息"""
    try:
        message = get_message_by_id(db, message_id)
        if message:
            db.delete(message)
            db.commit()
            print(f"✅ 删除成功: ID={message_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"❌ 删除失败: {e}")
        return False


def search_messages(db, keyword):
    """搜索包含关键词的消息"""
    try:
        messages = db.query(SimpleMessage).filter(SimpleMessage.msg.contains(keyword)).all()
        print(f"✅ 搜索到 {len(messages)} 条包含 '{keyword}' 的消息")
        return messages
    except Exception as e:
        print(f"❌ 搜索失败: {e}")
        return []


# 8. 主程序示例
def main():
    """主程序演示所有操作"""
    print("🚀 开始演示 PostgreSQL + SQLAlchemy 基本操作")
    print("=" * 50)

    # 创建表
    create_tables()

    # 创建数据库会话
    db = SessionLocal()

    try:
        # 1. 创建数据
        print("\n1. 创建消息:")
        msg1 = create_message(db, "Hello, PostgreSQL!")
        msg2 = create_message(db, "SQLAlchemy 是很好的ORM工具")
        msg3 = create_message(db, "Python 连接数据库很简单")

        # 2. 查询所有数据
        print("\n2. 查询所有消息:")
        all_msgs = get_all_messages(db)
        for msg in all_msgs:
            print(f"  - ID: {msg.id}, 消息: {msg.msg}")

        # 3. 根据ID查询
        print("\n3. 根据ID查询:")
        msg = get_message_by_id(db, 1)

        # 4. 更新数据
        print("\n4. 更新消息:")
        update_message(db, 2, "SQLAlchemy 是优秀的Python ORM工具")

        # 5. 搜索数据
        print("\n5. 搜索消息:")
        search_results = search_messages(db, "SQLAlchemy")
        for result in search_results:
            print(f"  - 找到: {result.msg}")

        # 6. 删除数据
        print("\n6. 删除消息:")
        delete_message(db, 3)

        # 7. 再次查看所有数据
        print("\n7. 最终数据:")
        final_msgs = get_all_messages(db)
        for msg in final_msgs:
            print(f"  - ID: {msg.id}, 消息: {msg.msg}")

    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
    finally:
        db.close()
        print("\n✅ 数据库连接已关闭")


# 9. 快速使用示例
def quick_example():
    """快速使用示例"""
    print("🚀 快速使用示例")
    print("=" * 30)

    # 修改这里的数据库连接信息
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/testdb"

    # 1. 创建引擎和会话
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()

    # 2. 定义模型
    class Message(Base):
        __tablename__ = "messages"
        id = Column(Integer, primary_key=True)
        msg = Column(String(200))

    # 3. 创建表
    Base.metadata.create_all(engine)

    # 4. 基本操作
    db = SessionLocal()

    # 增
    new_msg = Message(msg="第一条消息")
    db.add(new_msg)
    db.commit()

    # 查
    messages = db.query(Message).all()
    for m in messages:
        print(f"ID: {m.id}, MSG: {m.msg}")

    # 改
    if messages:
        messages[0].msg = "更新后的消息"
        db.commit()

    # 删
    if messages:
        db.delete(messages[0])
        db.commit()

    db.close()


if __name__ == "__main__":
    # 运行完整演示
    main()

    # 或者运行快速示例
    # quick_example()