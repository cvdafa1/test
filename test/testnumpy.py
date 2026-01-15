"""
使用 np.arange创建一个包含 0 到 9 的一维数组。
[1 2 3 4 5 6 7 8 9]
使用 np.zeros创建一个 3×3 的全零矩阵。
[[0. 0. 0.]
 [0. 0. 0.]
 [0. 0. 0.]]
使用 np.ones创建一个 2×3 的全 1 矩阵。
[[1. 1. 1.]
 [1. 1. 1.]]
使用 np.eye创建一个 3×3 的单位矩阵。
[[1. 0. 0. ]
 [0. 1. 0. ]
 [0. 0. 1. ]
]
如何创建一个从 1 到 10（不包括 10），步长为 2 的数组？
"""
import numpy as np

# np1 = np.arange(1, 10)
# np2 = np.zeros((3,3))
# np3 = np.ones((2,3))
# print(np3)
# np4 = np.eye(4)
# print(np4)
# np5 = np.arange(1, 10, step=2)
# print(np5)
#在 0 到 1 之间生成 5 个等间隔数
# arr = np.linspace(0, 1, 5)
"""
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
提取第 3 行第 2 列的元素（索引从 0 开始）。
8
提取第 2 行到第 3 行，第 2 列到第 3 列的子数组。
[[5 6]
 [8 9]]
"""
# arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# arr1 = arr[2,1]
# print(arr1)
# arr2 = arr[1:3,1:3]
# print(arr2)
"""
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
计算 a 和 b 的逐元素相加、相减、相乘。
计算 a 和 b 的逐元素相除（注意避免除零）。
计算 a 和 b 的点积（内积）。
"""
# a = np.array([1, 2, 3])
# b = np.array([4, 5, 6])
# c_add=a+b
# print(c_add)
# c_sub=a-b
# print(c_sub)
# c_mul=a*b
# print(c_mul)
# c_div=a//b
# print(c_div)
# c_truediv=a%b
# print(c_truediv)
# 使用 shape、ndim 和 dtype 属性分别查看数组的形状、维度和数据类型
# arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# print(arr.shape)
# print(arr.ndim)
# print(arr.dtype)
# 使用 reshape 方法可以改变数组形状，不改变数据
# arr = np.array([[4, 5, 6], [7, 8, 9]])
# print(arr)
# print(arr.reshape(3,2))

# arr = np.array([[4, 5, 6], [7, 8, 9], [10, 11, 12]])
# print(arr[0]) # 第一个元素
# print(arr[0:2]) # 1-2的元素
# print(arr[arr>2]) # 大于2的值
# print(arr[0,2]) # 第1行第2列的值   第一个元素的第3个值
# print(arr[[0,2]]) # 第1第3个元素
# print(arr[[0,2]])
a = np.array([1, 2])
b = np.array([3, 4])
# 连接
c = np.concatenate((a, b))
print(c)
# 垂直堆叠
a = np.array([1, 2])
b = np.array([3, 4])
c = np.vstack((a, b))
print(c)
# 水平堆叠
a = np.array([1, 2])
b = np.array([3, 4])
c = np.hstack((a, b))
print(c)
# 生成3*3的0-1的随机数
random_arr = np.random.rand(3, 3)
print(random_arr)
# 正太分布随机数组
normal_arr = np.random.randn(3, 3)
print(normal_arr)
# 生成 0 到 9 的 5 个随机整数
random_ints = np.random.randint(0, 10, 5)
print(random_ints)
# 数组的唯一值
arr = np.array([1, 2, 2, 3])
unique_arr = np.unique(arr)
print(unique_arr)
# 筛选大于 2 的元素
arr = np.array([1, 2, 3, 4])
filtered = arr[arr > 2]
print(filtered)
# 数组进行四舍五入
arr = np.array([1.234, 2.567])
rounded = np.round(arr, 2)
print(rounded)
# NumPy 数组的点积
a = np.array([1, 2])
b = np.array([3, 4])
dot_product = np.dot(a, b)
print(dot_product)
# NumPy 数组的矩阵乘法
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
result = a @ b
print(result)
