import pandas as pd


def generate_problematic_csv():
    # --------------------------
    # 1. 构造正常CSV内容的UTF-8字节
    # --------------------------
    # 表头：id,name,备注（UTF-8编码）
    header = "id,name,备注".encode('utf-8')
    # 第一行：包含𠀀（U+20000，GBK不支持，但用UTF-8编码写入）
    row1 = "1,𠀀,正常字段".encode('utf-8')  # 𠀀的UTF-8是E2 84 80
    # 第二行前缀：2,测试,
    row2_prefix = "2,测试,".encode('utf-8')
    # 第二行后缀：,另一个字段
    row2_suffix = ",另一个字段".encode('utf-8')
    # 第三行：3,其他,字段
    footer = "3,其他,字段".encode('utf-8')

    # --------------------------
    # 2. 构造无效字节序列（同时触发GBK和UTF-8报错）
    # --------------------------
    # 无效GBK序列：0x81（GBK双字节起始符） + 0x00（非法后续字节）→ GBK解码报错
    invalid_gbk = b'\x81\x00'
    # 无效UTF-8序列：0xE0（三字节起始符） → UTF-8解码报错（缺少后续字节）
    invalid_utf8 = b'\xE0'
    # 合并无效字节（顺序不影响，只要同时存在）
    invalid_part = invalid_gbk + invalid_utf8

    # --------------------------
    # 3. 合并所有字节，生成最终文件
    # --------------------------
    final_bytes = (
            header + b'' +          # 表头
        row1 + b'' +        # 第一行
        row2_prefix +  # 第二行前缀
        invalid_part +  # 插入无效字节
        row2_suffix + b'' + # 第二行后缀
        footer + b''       # 第三行
    )

    # --------------------------
    # 4. 以二进制模式写入文件（避免编码检查）
    # --------------------------
    with open('problematic.csv', 'wb') as f:
        f.write(final_bytes)

    print("文件已生成：problematic.csv")


# 执行生成
# generate_problematic_csv()

input_file = 'problematic.csv'

try:
    df = pd.read_csv(input_file, encoding='utf-8')
    print('utf8格式')
except Exception as e:
    print(f'❌ 无法以 UTF-8 读取：{e}')

try:
    df = pd.read_csv(input_file, encoding='gbk', encoding_errors='ignore')
    print('gbk格式')
except Exception as e:
    print(f'❌ 无法以 GBK 读取：{e}')
    raise ValueError("✅ 文件编码无法解析，报错成功！（这是你想要的）")

# 如果居然执行到这里，说明没有报错（不应该！）
print(df)  # 不应该执行到这一步
first_row = df.iloc[0]
for col in df.columns:
    if not isinstance(col, str) or not isinstance(first_row[col], str) :
        raise ValueError(f"第1或第2行中列'{col}'不是位号名或描述")
# 2. 取出除前两行之外的数据
data_part = df.iloc[2:].reset_index(drop=True)
if data_part.empty:
    raise ValueError("数据部分为空")
# 3. 检查第一列是否可以转换为时间类型
try:
    pd.to_datetime(data_part.iloc[:, 0])
except Exception as e:
    raise ValueError("数据部分的第一列无法解析为时间") from e

# 4. 检查其余列是否为浮点数
for col in data_part.columns[1:]:
    try:
        # 尝试将每列转为 float 类型
        pd.to_numeric(data_part[col], errors='raise')
    except Exception as e:
        raise ValueError(f"列 '{col}' 数据格式有问题") from e
# 5. 检查数据条数是否符合要求
if len(df) < 100:
    raise ValueError("数据必须至少含有100条数据")