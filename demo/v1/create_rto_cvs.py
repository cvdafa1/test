import csv
import random
from datetime import datetime, timedelta

# 表头
header = ['timeStamp', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9', 'tag10', 'tag11', 'tag12', 'tag13', 'tag14', 'tag15', 'tag16']
# 中文表头（可选）
header_cn = ['时间戳', '吨碱电耗', '产品碱浓度', '进电解槽纯水流量', '电解槽槽温', '进电解槽淡盐水流量', '进口碱液温度', '阳极循环罐出口温度', '阴极室去外管氢气压力', '阳极室去外管氯气压力', '碱液循环罐液位', '淡盐水循环罐液位', '电解槽电流', '进电解槽盐酸流量', '进电解槽盐水流量', '进电解槽碱液流量', '氯碱装置电耗']

# 生成随机数据（范围100-1000）
start_time = datetime.strptime("2025/3/27 0:26:05", "%Y/%m/%d %H:%M:%S")
data = []

for i in range(20000):
    timestamp = (start_time + timedelta(seconds=5*i)).strftime("%Y/%m/%d %H:%M:%S")
    row = [timestamp] + [round(random.uniform(100, 1000), 6) for _ in range(len(header_cn)-1)]
    data.append(row)

# 写入CSV文件（同时包含中英文表头）
with open('random_rto_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)       # 英文表头
    writer.writerow(header_cn)    # 中文表头（可选）
    writer.writerows(data)

print("CSV文件已生成：random_rto_data.csv")