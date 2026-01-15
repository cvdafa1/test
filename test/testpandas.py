import numpy as np
import pandas as pd

data = {'name': ['Alice', 'Bob', 'Charlie', 'Bob'], 'age': [25, 30, 35, None]}
df = pd.DataFrame(data)
# print(df)
# # 查看前几行
# print(df.head(1))
#
# # 查看基本信息
# print(df.info())
# print(df.describe())
#
# # 选择列
# print(df['name'])  # 选择单列
# print(df[['name', 'age']])  # 选择多列

# # 选择行
# print(df.iloc[0])  # 按位置选择第一行
# print(df.loc[0])   # 按索引选择
#
# # 布尔索引
# print(df[df['age'] > 30])  # 选择年龄大于30的行

# 添加列
# df['new_column'] = df['age'] * 2
# print(df)
# # 删除列
# df = df.drop('new_column', axis=1)
#
# # 排序
# df_sorted = df.sort_values('age', ascending=False)
# print(df_sorted)
#
# # 分组和聚合
# # 已name内容分组
# grouped = df.groupby('name')
# print(grouped.sum())
# print(grouped.mean())
#
# # 处理缺失值
# df_fill = df.fillna(0)  # 用0填充缺失值
# print(df_fill)
# df_dr = df.dropna()   # 删除包含缺失值的行
# print(df_dr)

# # 连接DataFrame
# df1 = pd.DataFrame({'A': ['A0', 'A1'], 'B': ['B0', 'B1']})
# df2 = pd.DataFrame({'A': ['A2', 'A3'], 'B': ['B2', 'B3']})
# result = pd.concat([df1, df2])
# print(result)
#
# # 合并DataFrame
# left = pd.DataFrame({'keys': ['K0', 'K1'], 'A': ['A0', 'A1'], 'B': ['B0', 'B1']})
# right = pd.DataFrame({'keys': ['K0', 'K1'], 'C': ['C0', 'C1'], 'D': ['D0', 'D1']})
# result = pd.merge(left, right, on='keys')
# print(result)


# # 将DataFrame转换为NumPy数组
# array = df.values
# # print(array)
# # 将NumPy数组转换为DataFrame
# df = pd.DataFrame(array, columns=['name', 'age'])
# # print(df)
# df = df.fillna(0)
# # 在Pandas中使用NumPy函数
# df['age_sqrt'] = np.sqrt(df['age'])
# print(df)
# # 使用Pandas处理时间序列
# dates = pd.date_range('20230101', periods=6)
# df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
# print(df)

# # 处理缺失值
# df.fillna({'age': df['age'].mean(), 'income': 0}, inplace=True)
#
# # 删除重复行
# df.drop_duplicates(inplace=True)
#
# # 替换异常值
# df.loc[df['age'] > 100, 'age'] = df['age'].median()
#
# # 标准化数据
# df['normalized'] = (df['value'] - df['value'].mean()) / df['value'].std()


# a = np.array([1, 2, 3])        # shape (3,)
# b = np.array([[10], [20], [30]])  # shape (3, 1)
# c = a + b  # 广播后，变成 (3,3) 的逐元素相加
# print(c)

# import matplotlib.pyplot as plt
#
# # 绘制直方图
# df['age'].plot.hist(bins=20)
# plt.show()
#
# # 绘制箱线图
# df.boxplot(column='salary', by='department')
# plt.show()
#
# # 绘制散点图
# df.plot.scatter(x='age', y='salary')
# plt.show()


# # 创建 3x3 的随机整数矩阵，范围 1~10
# matrix_3x3 = np.random.randint(1, 11, size=(3, 3))
# print("原始 3x3 矩阵:")
# print(matrix_3x3)
# # 0是列
# print(np.sum(matrix_3x3, axis=0))
# # 1是行
# print(np.sum(matrix_3x3, axis=1))
# print(np.max(matrix_3x3))
# print(np.min(matrix_3x3))
# print(np.mean(matrix_3x3))
# # 复制一份，避免直接修改原矩阵（可选）
# modified_matrix = matrix_3x3.copy()
# modified_matrix[modified_matrix > 5] = 0
# print("\n将 >5 的元素替换为 0 后的矩阵:")
# print(modified_matrix)

# arr1 = np.array([[1,2],[2,1],[3,4]])
# arr2 = np.array([[1,2,6],[2,1,4]])
# print(np.dot(arr1, arr2))
# print(arr1@arr2)

# matrix_4x3 = np.random.randint(-4, 11, size=(4, 3))
# print(matrix_4x3)
# matrix_4x3[matrix_4x3 < 0] = 0
# print(matrix_4x3)
# matrix_4x3 = np.random.randint(-4, 11, size=(4,))
# print(matrix_4x3)

# import time
#
# # Python 列表
# py_list = list(range(1000000))
# start = time.time()
# total = sum(py_list)
# end = time.time()
# print("Python 列表求和耗时：", end - start)
#
# # Numpy 数组
# np_array = np.arange(1000000)
# start = time.time()
# total = np.sum(np_array)
# end = time.time()
# print("Numpy 求和耗时：", end - start)

# # Python 列表 + 循环
# py_list1 = list(range(1000000))
# py_list2 = list(range(1000000, 2000000))
# start = time.time()
# result = [a + b for a, b in zip(py_list1, py_list2)]
# end = time.time()
# print("Python 列表相加耗时：", end - start)
#
# # Numpy 数组
# np_array1 = np.arange(1000000)
# np_array2 = np.arange(1000000, 2000000)
# start = time.time()
# result = np_array1 + np_array2
# end = time.time()
# print("Numpy 数组相加耗时：", end - start)

# data = {'name': ['Alice', 'Bob', 'Charlie'], 'scord':[14, 15, 78, 19]}
# df = pd.DataFrame(data, columns=['name', 'age'])
# print(f"行数(记录数): {len(df)} 或 df.shape[0] = {df.shape[0]}")
# print(f"列数(字段数): {len(df.columns)} 或 df.shape[1] = {df.shape[1]}")
# print("\n列名:")
# print(df.columns.tolist())
# print("\n所有列名和数据类型:")
# print(df.dtypes)
# print("\nDataFrame形状(行数, 列数):", df.shape)

# mydata = {"name":['zhuheng'],"age":['28'],'city':['xian']}
# mydata_df = pd.DataFrame(mydata, columns=['name','age','city'])
# print(mydata_df)
#
# wather = pd.Series([15,48,56,56], index=['周一','周二','周三','周四'])
# print(wather)



# print(df)
# print(df.head())
# print(df.info())
# print(df.describe())
# print(df.iloc[0].sum())
# print(df.iloc[1].sum())
# print(df['timeStamp'].sum())
# print(df.loc[0])
# print(df.iloc[0])


# # 选择单列，返回一个 Series
# col_a = df['timeStamp']
# print(col_a)
# # 选择多列，返回一个 DataFrame
# cols_ab = df[['timeStamp', 'GXHYNH_133_PI_2101.PV']]
# print(cols_ab)

# # 选择索引为 1 的行
# row_1 = df.loc[1]  # 返回 Series
# print(row_1)
# # 选择多行：索引为 1 和 2 的行
# rows_1_2 = df.loc[[1, 2]]  # 返回 DataFrame
# print(rows_1_2)
df = pd.read_csv(filepath_or_buffer='test.csv')
# # 选择索引为 1 的行，列名为 'A' 的数据
# value = df.loc[1, 'timeStamp']
# print(value)
# # 选择多行多列
# subset = df.loc[[1, 2], ['timeStamp', 'GXHYNH_133_FI_2101A.PV']]
# print(subset)
# # 切片选择（注意：loc 的切片是包含两端的！）
# subset_slice = df.loc[0:5, 'timeStamp':'GXHYNH_133_FI_2101A.PV']  # 包括索引 0 和 1，列 A 和 B
# print(subset_slice)
# # 选择 GXHYNH_133_FI_2101A.PV 列大于 3100 的行中的 GXHYNH_133_FI_2101A.PV 和 GXHYNH_133_FI_2104A.PV 列
# result = df.loc[df['GXHYNH_133_FI_2101A.PV'] > 3100, ['GXHYNH_133_FI_2101A.PV', 'GXHYNH_133_FI_2104A.PV']]
# print(result)
# print(df.isnull())      # 每个值是否为缺失
# print(df.isnull().sum())  # 每列缺失值数量
# # df.dropna()           # 删除含有缺失值的行
# # df.fillna(0)          # 用 0 填充缺失值
# # df.fillna(df.mean())  # 用列均值填充（适用于数值）
# print(df.duplicated())      # 是否重复
# print(df.duplicated().sum())  # 重复行数

# import pandas as pd
#
# # 创建示例数据
# data = {
#     '部门': ['销售', '销售', '技术', '技术', '人事', '人事'],
#     '员工': ['张三', '李四', '王五', '赵六', '钱七', '孙八'],
#     '工资': [5000, 6000, 8000, 9000, 4000, 4500],
#     '奖金': [1000, 1200, 1500, 1800, 800, 900]
# }
# df = pd.DataFrame(data)
#
# # 按部门分组并计算平均工资
# avg_salary = df.groupby('部门')['工资'].mean()
# print("各部门平均工资:")
# print(avg_salary)
#
# # 按部门分组，计算多个统计量
# dept_stats = df.groupby('部门').agg({
#     '工资': ['mean', 'sum', 'count', 'max', 'min'],
#     '奖金': ['mean', 'sum']
# })
#
# print("\n各部门详细统计:")
# print(dept_stats)
#
# # 更简洁的写法
# simple_stats = df.groupby('部门').agg(
#     平均工资=('工资', 'mean'),
#     总工资=('工资', 'sum'),
#     员工数=('工资', 'count'),
#     平均奖金=('奖金', 'mean')
# )
#
# print("\n简化版部门统计:")
# print(simple_stats)

# # 创建更复杂的数据
# data2 = {
#     '部门': ['销售', '销售', '技术', '技术', '人事', '人事', '销售', '技术'],
#     '员工': ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'],
#     '工资': [5000, 6000, 8000, 9000, 4000, 4500, 5500, 8500],
#     '奖金': [1000, 1200, 1500, 1800, 800, 900, 1100, 1700],
#     '城市': ['北京', '上海', '北京', '上海', '广州', '广州', '北京', '上海']
# }
# df2 = pd.DataFrame(data2)
#
# # 创建数据透视表
# pivot1 = pd.pivot_table(
#     df2,
#     values='工资',
#     index='部门',
#     columns='城市',
#     aggfunc='mean'
# )
# print("\n按部门和城市分组的平均工资透视表:")
# print(pivot1)
#
# # 更复杂的数据透视表
# pivot2 = pd.pivot_table(
#     df2,
#     values=['工资', '奖金'],
#     index='部门',
#     columns='城市',
#     aggfunc={'工资': 'mean', '奖金': 'max'},
#     fill_value=0,
#     margins=True,
#     margins_name='总计'
# )
# print("\n更复杂的数据透视表:")
# print(pivot2)
# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
# plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
# x = [1, 2, 3]
# y = [1, 2, 3]
# plt.title("标题")
# plt.xlabel("X轴")
# plt.ylabel("Y轴")
# 折线图
# plt.plot(x, y)
# 柱状图
# plt.bar(x, y)
# 或横向柱状图
# plt.barh(x, y)
# 散点图
# plt.scatter(x, y)
# plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
#
# # 设置中文字体
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
#
# # 创建一个2x2的子图布局
# fig, axes = plt.subplots(2, 2, figsize=(15, 12))
# fig.suptitle('数据可视化示例：折线图、柱状图、散点图', fontsize=16, fontweight='bold')
#
# # 数据准备
# 年份 = [2018, 2019, 2020, 2021, 2022, 2023]
# 销量 = [120, 135, 110, 145, 168, 185]
#
# 城市 = ['北京', '上海', '广州', '深圳', '杭州', '成都']
# 平均年龄 = [35.2, 34.8, 33.9, 32.7, 33.5, 34.1]
#
# 身高 = [160, 162, 165, 168, 170, 172, 175, 178, 180, 182,
#         161, 163, 166, 169, 171, 173, 176, 179, 181, 183]
# 体重 = [52, 54, 56, 59, 61, 63, 66, 68, 70, 72,
#         53, 55, 57, 60, 62, 64, 67, 69, 71, 73]
#
# # 1. 折线图（时间序列 - 年份-销量）
# axes[0, 0].plot(年份, 销量, marker='o', linewidth=2, markersize=8, color='#2E86AB')
# axes[0, 0].set_title('折线图：年度销量趋势（时间序列）', fontsize=12, fontweight='bold')
# axes[0, 0].set_xlabel('年份', fontsize=10)
# axes[0, 0].set_ylabel('销量（万件）', fontsize=10)
# axes[0, 0].grid(True, alpha=0.3)
# # 添加数值标签
# for i, v in enumerate(销量):
#     axes[0, 0].annotate(f'{v}', (年份[i], v), textcoords="offset points",
#                        xytext=(0,10), ha='center', fontsize=8)
#
# # 2. 柱状图（各城市平均年龄）
# bars = axes[0, 1].bar(城市, 平均年龄, color=['#A23B72', '#F18F01', '#C73E1D',
#                                            '#6A994E', '#40407A', '#CC5500'])
# axes[0, 1].set_title('柱状图：各城市平均年龄', fontsize=12, fontweight='bold')
# axes[0, 1].set_xlabel('城市', fontsize=10)
# axes[0, 1].set_ylabel('平均年龄（岁）', fontsize=10)
# axes[0, 1].tick_params(axis='x', rotation=45)
# axes[0, 1].grid(True, alpha=0.3, axis='y')
#
# # 在柱子上添加数值标签
# for bar, age in zip(bars, 平均年龄):
#     height = bar.get_height()
#     axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
#                    f'{age}岁', ha='center', va='bottom', fontsize=9)
#
# # 3. 散点图（身高-体重关系）
# scatter = axes[1, 0].scatter(身高, 体重, alpha=0.7, s=60, c=身高,
#                             cmap='viridis', edgecolors='black', linewidth=0.5)
# axes[1, 0].set_title('散点图：身高与体重的关系', fontsize=12, fontweight='bold')
# axes[1, 0].set_xlabel('身高（cm）', fontsize=10)
# axes[1, 0].set_ylabel('体重（kg）', fontsize=10)
# axes[1, 0].grid(True, alpha=0.3)
#
# # 添加颜色条
# cbar = plt.colorbar(scatter, ax=axes[1, 0])
# cbar.set_label('身高（cm）', fontsize=9)
#
# # 4. 额外添加一个更清晰的散点图（按性别分组效果）
# # 创建模拟的男女数据
# np.random.seed(42)
# 男性身高 = np.random.normal(175, 6, 20)
# 男性体重 = 0.8 * 男性身高 + np.random.normal(0, 5, 20) + 10
# 女性身高 = np.random.normal(162, 5, 20)
# 女性体重 = 0.8 * 女性身高 + np.random.normal(0, 4, 20) + 5
#
# axes[1, 1].scatter(男性身高, 男性体重, alpha=0.7, s=50, c='blue',
#                   label='男性', edgecolors='black', linewidth=0.5)
# axes[1, 1].scatter(女性身高, 女性体重, alpha=0.7, s=50, c='red',
#                   label='女性', edgecolors='black', linewidth=0.5)
# axes[1, 1].set_title('散点图：身高与体重关系（按性别）', fontsize=12, fontweight='bold')
# axes[1, 1].set_xlabel('身高（cm）', fontsize=10)
# axes[1, 1].set_ylabel('体重（kg）', fontsize=10)
# axes[1, 1].legend(fontsize=9)
# axes[1, 1].grid(True, alpha=0.3)
#
# # 调整布局
# plt.tight_layout()
# plt.show()
#
# # 如果想要单独显示每个图表，可以使用以下代码：
#
# # 创建单独的图表
# fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))
#
# # 1. 单独的折线图
# axes2[0].plot(年份, 销量, marker='o', linewidth=3, markersize=8, color='#2E86AB')
# axes2[0].set_title('📈 年度销量趋势（折线图）', fontsize=14, fontweight='bold', pad=20)
# axes2[0].set_xlabel('年份', fontsize=12)
# axes2[0].set_ylabel('销量（万件）', fontsize=12)
# axes2[0].grid(True, alpha=0.3)
# for i, v in enumerate(销量):
#     axes2[0].annotate(f'{v}', (年份[i], v), textcoords="offset points",
#                      xytext=(0,15), ha='center', fontsize=10, fontweight='bold')
#
# # 2. 单独的柱状图
# bars2 = axes2[1].bar(城市, 平均年龄, color=['#FF6B6B', '#4ECDC4', '#45B7D1',
#                                            '#96CEB4', '#FFEAA7', '#DDA0DD'])
# axes2[1].set_title('📊 各城市平均年龄（柱状图）', fontsize=14, fontweight='bold', pad=20)
# axes2[1].set_xlabel('城市', fontsize=12)
# axes2[1].set_ylabel('平均年龄（岁）', fontsize=12)
# axes2[1].tick_params(axis='x', rotation=45)
# axes2[1].grid(True, alpha=0.3, axis='y')
# for bar, age in zip(bars2, 平均年龄):
#     height = bar.get_height()
#     axes2[1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
#                  f'{age}岁', ha='center', va='bottom', fontsize=10, fontweight='bold')
#
# # 3. 单独的散点图
# scatter2 = axes2[2].scatter(身高, 体重, alpha=0.6, s=80, c=身高,
#                            cmap='plasma', edgecolors='black', linewidth=0.8)
# axes2[2].set_title('🔵 身高与体重关系（散点图）', fontsize=14, fontweight='bold', pad=20)
# axes2[2].set_xlabel('身高（cm）', fontsize=12)
# axes2[2].set_ylabel('体重（kg）', fontsize=12)
# axes2[2].grid(True, alpha=0.3)
# plt.colorbar(scatter2, ax=axes2[2], label='身高（cm）')
#
# plt.tight_layout()
# plt.show()
#
# # 打印数据摘要
# print("=== 数据摘要 ===")
# print("\n1. 年度销量数据:")
# for y, s in zip(年份, 销量):
#     print(f"  {y}年: {s}万件")
#
# print("\n2. 城市平均年龄:")
# for city, age in zip(城市, 平均年龄):
#     print(f"  {city}: {age}岁")
#
# print("\n3. 身高体重数据样本:")
# print(f"  身高范围: {min(身高)}cm - {max(身高)}cm")
# print(f"  体重范围: {min(体重)}kg - {max(体重)}kg")
# print(f"  样本数量: {len(身高)}个数据点")
# import matplotlib.pyplot as plt
# import seaborn as sns
# titanic = sns.load_dataset('titanic')
# print(titanic.head())
# plt.figure(figsize=(10, 6))
# sns.barplot(x='sex', y='survived', hue='class', data=titanic)
# plt.title('不同性别和舱位的生存率')
# plt.show()

# from sklearn.datasets import load_iris
# from sklearn.model_selection import train_test_split
#
# # 加载鸢尾花数据集
# iris = load_iris()
# X = iris.data
# y = iris.target
#
# # 将数据集划分为训练集和测试集，测试集占比 20%，随机种子为 42
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
#
# print("训练集特征数据形状:", X_train.shape)
# print("测试集特征数据形状:", X_test.shape)
# print("训练集标签数据形状:", y_train.shape)
# print("测试集标签数据形状:", y_test.shape)


import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 设置随机种子，确保结果可复现
np.random.seed(42)

# 模拟中国主要城市数据（20个城市）
cities = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉',
          '西安', '重庆', '天津', '苏州', '长沙', '郑州', '青岛', '大连',
          '宁波', '厦门', '福州', '无锡']

# 生成模拟特征数据
n_samples = len(cities)
data = {
    '城市': cities,
    '人均GDP': np.random.uniform(5, 20, n_samples),  # 万元
    '平均工资': np.random.uniform(5000, 20000, n_samples),  # 元/月
    '人口密度': np.random.uniform(500, 3000, n_samples),  # 人/平方公里
    '地铁线路数': np.random.randint(0, 20, n_samples),  # 条
    '高校数量': np.random.randint(10, 100, n_samples),  # 所
}

# 模拟房价（目标变量），基于特征线性组合 + 噪声
data['房价'] = (
    5000 * data['人均GDP'] +  # 人均GDP影响大
    100 * data['平均工资'] +   # 工资影响
    20 * data['人口密度'] +    # 人口密度影响
    800 * data['地铁线路数'] + # 地铁影响
    300 * data['高校数量'] +   # 教育资源影响
    np.random.normal(0, 5000, n_samples)  # 添加噪声
)

# 转换为DataFrame
df = pd.DataFrame(data)
print(df.head())  # 查看前5行数据
# 特征：人均GDP、平均工资、人口密度、地铁线路数、高校数量
X = df[['人均GDP', '平均工资', '人口密度', '地铁线路数', '高校数量']]

# 目标：房价
y = df['房价']
# 划分训练集和测试集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("训练集样本数:", len(X_train))  # 16
print("测试集样本数:", len(X_test))   # 4

# 创建线性回归模型
model = LinearRegression()

# 训练模型
model.fit(X_train, y_train)

# 模型验证
# # 输出模型系数（每个特征对房价的影响）
# print("模型系数（特征重要性）:", model.coef_)
# print("模型截距:", model.intercept_)
# # 测试集预测
# y_pred = model.predict(X_test)
# # 计算评估指标
# mse = mean_squared_error(y_test, y_pred)
# rmse = np.sqrt(mse)
# r2 = r2_score(y_test, y_pred)
#
# print("均方误差 (MSE):", mse)
# print("均方根误差 (RMSE):", rmse)
# print("决定系数 (R²):", r2)
# # 查看特征重要性（系数绝对值越大，影响越大）
# feature_importance = pd.DataFrame({
#     '特征': X.columns,
#     '系数': model.coef_,
#     '绝对值系数': np.abs(model.coef_)
# }).sort_values('绝对值系数', ascending=False)
#
# print(feature_importance)

# 模型使用
model.fit(X, y)

# 获取西安2024年的特征数据（模拟）
xian_2024 = {
    '人均GDP': 12.5,    # 万元
    '平均工资': 9500,   # 元/月
    '人口密度': 1200,   # 人/km²
    '地铁线路数': 9,    # 条
    '高校数量': 1000,     # 所
}

# 转换为模型输入格式
xian_features = pd.DataFrame([xian_2024])

# 预测2024年西安房价
xian_2024_price = model.predict(xian_features)[0]
print(f"预测2024年西安房价: {xian_2024_price:.0f} 元/平方米")