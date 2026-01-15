import pandas as pd
from datetime import datetime, timedelta

input_file = '硫化氢预测数据-automl-min.csv'
output_file = 'input.csv'
column_name = 'timeStamp'  # 要修改的列名（或列索引）

# 初始时间
start_time = datetime.strptime("2025/3/27 0:26:05", "%Y/%m/%d %H:%M:%S")

# 读取 CSV 文件（假设第一行是表头）
df = pd.read_csv(input_file, encoding='utf-8')

# 生成时间序列（从第3行开始，每行 +5 秒）
timestamps = [start_time + timedelta(seconds=5 * i) for i in range(len(df)-1)]  # 跳过表头和第一行数据
df.iloc[1:, df.columns.get_loc(column_name)] = [t.strftime("%Y/%m/%d %H:%M:%S") for t in timestamps]

# 保存修改后的数据
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"修改完成，结果已保存到 {output_file}")