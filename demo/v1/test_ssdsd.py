
import pandas as pd

# 写入合法 + 非法 GBK 字节（一定会触发解码错误）
with open("force_gbk_error.csv", "wb") as f:
    f.write(b'\xD6\xD0\x81\xFE\x81\x7F')  # '中' + 非法

# 尝试读取（一定会报错）
try:
    df = pd.read_csv("force_gbk_error.csv", encoding='gbk')
    print("❌ 不应该成功！")
    print(df)
except Exception as e:
    print("✅ 报错成功！（这就是你想要的）")
    print(f"错误类型：{type(e).__name__}")
    print(f"错误详情：{e}")
