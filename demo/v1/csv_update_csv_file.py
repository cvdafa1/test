# import pandas as pd
#
# input_file = 'input.csv'
# output_file = 'output.csv'
# column_index = 1  # 要修改的列索引（0 开始）
#
# # 读取 CSV 文件（pandas 自动处理表头）
# df = pd.read_csv(input_file, encoding='utf-8')
#
# # # 修改指定列的值（从第 2 行开始）
# # df.iloc[1:, column_index] = "107.423958"
# # 要删除的列名（可以是单个列名或列表）
# columns_to_drop = ["GXHYNH_133_AI_2101C.PV"]  # 示例：删除 "GXHYNH_133_AI_2101C.PV"列
# # 2️⃣ 删除指定列
# df = df.drop(columns=columns_to_drop)
#
# # 写入修改后的数据
# df.to_csv(output_file, index=False, encoding='utf-8')
#
# print(f"修改完成，结果已保存到 {output_file}")
from datetime import timedelta

import pandas as pd

# 文件路径配置
# input_file = 'input31.csv'
# output_file = 'output.csv'

# 要删除的列名
columns_to_drop = "GXHYNH_133_AI_2101C.PV"  #

# try:
    # 读取CSV文件
    # df = pd.read_csv(input_file, encoding='utf-8')
    # 读取CSV文件，指定前两行为表头
    # df = pd.read_csv(input_file, encoding='utf-8', header=[0, 1])

    # df = pd.read_csv(input_file, encoding='utf-8')
    # print(df)
    # df = []
    # try:
        # df = pd.read_csv(input_file, encoding='gbk')
    # except Exception as e:
        # print(e)
    # print(df)
    # 删除列
    # df.drop(columns=columns_to_drop,inplace=True)
    # 修改列
    # column_index = 1  # 要修改的列索引（0 开始）
    # # 修改指定列的值（从第 2 行开始）
    # df.iloc[1:, column_index] = "107.423958"
    # 修改前打印第一行时间戳

    # df[('timeStamp', '时间戳')] = pd.to_datetime(df[('timeStamp', '时间戳')], format='%Y/%m/%d %H:%M:%S') + timedelta(
        # seconds=5)
    # 获取起始时间
    # start_time = df[('timeStamp', '时间戳')].min()
    # 生成新的时间序列（60秒间隔）
    # new_timestamps = pd.date_range(
    #     start=start_time,
    #     periods=len(df),  # 保持数据行数不变
    #     freq="70s"  # 60秒间隔
    # )
    # 替换原时间列
    # df[('timeStamp', '时间戳')] = new_timestamps
    # 写入修改后的数据
    # df.to_csv(output_file, index=False, encoding='utf-8')
    # print(f"结果已保存到 {output_file}")

# except FileNotFoundError:
#     print(f"错误：输入文件 {input_file} 未找到")
# except Exception as e:
#     print(f"处理过程中发生错误: {str(e)}")
import pandas as pd



# Step 3: 尝试读取并期望报错
input_file = 'dev_input.csv'

try:
    df = pd.read_csv(input_file, encoding='utf-8')
    print('utf8格式')
except Exception as e:
    print(f'❌ 无法以 UTF-8 读取：{e}')

# try:
#     df = pd.read_csv(input_file, encoding='gbk')
#     print('gbk格式')
# except Exception as e:
#     print(f'❌ 无法以 GBK 读取：{e}')
#     raise ValueError("✅ 文件编码无法解析，报错成功！（这是你想要的）")

# 如果居然执行到这里，说明没有报错（不应该！）
print(df)  # 不应该执行到这一步

# df = pd.read_csv(fs.open(file_info, 'rb'))
# first_row = df.iloc[0]
# for col in df.columns:
#     if not isinstance(col, str) or not isinstance(first_row[col], str):
#         raise ValueError(f"第1或第2行中列'{col}'不是位号名或描述")
# # 2. 取出除前两行之外的数据
# data_part = df.iloc[2:].reset_index(drop=True)
# if data_part.empty:
#     raise ValueError("数据部分为空")
# # 3. 检查第一列是否可以转换为时间类型
# try:
#     pd.to_datetime(data_part.iloc[:, 0])
# except Exception as e:
#     raise ValueError("数据部分的第一列无法解析为时间") from e
#
# # 4. 检查其余列是否为浮点数
# for col in data_part.columns[1:]:
#     try:
#         # 尝试将每列转为 float 类型
#         pd.to_numeric(data_part[col], errors='raise')
#     except Exception as e:
#         raise ValueError(f"列 '{col}' 数据格式有问题") from e


