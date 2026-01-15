import csv
import random
from datetime import datetime, timedelta

# 表头
header = ['timeStamp', 'tag1', 'tag2', 'tag3', 'tag4']
# 中文表头（可选）
header_cn = ['时间戳', '槽温', '单元槽电压', '电流', '碱浓度']

# 生成随机数据（范围100-1000）
start_time = datetime.strptime("2022/3/27 0:26:05", "%Y/%m/%d %H:%M:%S")
data = []

for i in range(10000):
    timestamp = (start_time + timedelta(seconds=5*i)).strftime("%Y/%m/%d %H:%M:%S")
    row = [timestamp] + [round(random.uniform(82, 84), 6),round(random.uniform(2.9, 3), 6),round(random.uniform(14, 15), 6),round(random.uniform(32, 33), 6)]
    data.append(row)

# 写入CSV文件（同时包含中英文表头）
with open('random_electrolysis_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)       # 英文表头
    writer.writerow(header_cn)    # 中文表头（可选）
    writer.writerows(data)

print("CSV文件已生成：random_electrolysis_data.csv")