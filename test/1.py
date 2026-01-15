import yaml
class User:
    def __init__(self, name):
        self.name = name

# 定义函数
def greet(name):
    return f"Hello, sds!"

def get_info(name):
    return f"User: ds"

# 创建实例
user1 = User("Alice")

# 动态设置方法
setattr(user1, "greet", greet)
setattr(user1, "get_info", get_info)

# 调用动态添加的方法
print(user1.greet("1"))  # Hello, Alice!
print(user1.get_info("2"))  # User: Alice

s = getattr(user1, "get_info", greet)
print(s("ds"))


print(hasattr(user1, "get_info1"))


delattr(user1, "get_info")
s = getattr(user1, "get_info", greet)
print(s("ds"))


class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


calc = Calculator()
while True:
    operation = input("Enter operation (add/multiply): ")  # 用户输入
    numbers = (5, 3)
    if operation == 'q':
        print('退出')
        break
    if hasattr(calc, operation):
        method = getattr(calc, operation)
        result = method(*numbers)
        print(f"Result: {result}")  # 根据输入调用对应方法
