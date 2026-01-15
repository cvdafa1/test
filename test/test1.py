tar_vars1 = [{'tag': 'CokeRate', 'description': '结焦速率'}, {'tag': 'yield', 'description': '裂解炉乙烯收率'}]
input_vars1 = [{'tag': 'XC1137Y', 'description': 'A炉膛温度'}, {'tag': 'XC1237Y', 'description': 'B炉膛温度'}, {'tag': 'average_furnace_temp', 'description': '所有炉管COT平均温度'}, {'tag': 'XX1106Y', 'description': '裂解炉A炉膛进料量'}, {'tag': 'XX1306Y', 'description': '裂解炉B炉膛进料量'}, {'tag': 'TSBV', 'description': '烃水比'}]

rx_data= {"X_test": [[850, 841.875, 842.4707961309523, 27.435416816666663, 27.219075616666668, 0.179993]], "n_targets": 2}
ry_data = {"preValue": [[0.2653083442, 49.590727894000004]]}
X=[842.0, 841.875, 842.4707961309523, 27.435416816666663, 27.219075616666668, 0.179993]
Y=[0.1253627450168185, 49.94744333094091]

# 第一行, 第二行
all_tar = input_vars1+tar_vars1
print(all_tar)

# 原始数据
o = X+Y



# 修改后的数据
result = [a + b for a, b in zip(rx_data['X_test'], ry_data['preValue'])]

result.insert(0, o)
print(result)

