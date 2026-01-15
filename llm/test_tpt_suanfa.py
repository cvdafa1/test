# 预测automl推理算法(预处理与推理)
import json

import requests
# session_id = "019a2e93-35c0-78e2-9aa9-77e85f643bff"
# tenant_id = '0'
# csv_path = 's3://recommend/0/0/1772cd2d15c549868f3239d85fd6535d_output.csv'
# # 模型在线推理前的数据处理
# # 离线
# # alg_data_eval_params= {"id": "019a2f8f-9db9-7c93-89c3-434a938e6457", "task_type": 2, "online_data": False, "csv_path": "s3://recommend/0/0/97e2e19672bb44e9ab5de53041a7b682_output.csv", "prediction_length": "", "frequency": 0, "target_variables": ["CokeRate", "yield"], "input_variables": ["XC1137Y", "XC1237Y", "average_furnace_temp", "XX1106Y", "XX1306Y", "TSBV"]}
# # 在线
# alg_data_eval_params= {"id": "019a2f8f-9db9-7c93-89c3-434a938e6457", "task_type": 2, "online_data": True, "csv_path": "", "prediction_length": "", "frequency": 0, "target_variables": ["CokeRate", "yield"], "input_variables": ["XC1137Y", "XC1237Y", "average_furnace_temp", "XX1106Y", "XX1306Y", "TSBV"]}
# q_url= "http://10.30.73.42:31668/call/app?name=tptmoe_create_data_sample_py&built_in=1&time_out=600"
# response = requests.post(
#     url = q_url,
#     data= json.dumps(alg_data_eval_params, ensure_ascii=False),
#     headers={
#         'Content-Type': 'application/json',
#         'tenant-id' : tenant_id,
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
# })
# json_obj_data_eval = {}
# if response.status_code == 200:
#     try:
#         json_obj = json.loads(response.text)
#         json_obj_data_eval = json.loads(json_obj["data"]["result"])
#     except Exception as e:
#         print("执行推理数据处理结果失败，返回结果：" + response.text)
# else:
#     print("执行推理数据处理出现异常，返回结果：" + response.text)
# print(json_obj_data_eval)



# url = 'http://10.30.73.42:31668/call/app?name=AutoMLRegressionInferenceOnline_py&built_in=1&time_out=600'
# alg_exec_params = {
#             "id": session_id,
#             "task_type" : 2,
#             "model_file": "data/finetune/0/best_automl_DummyRegressor_regressor_202510291413.joblib",
#             "data": json_obj_data_eval
#         }
# response = requests.post(
#         url = url,
#         data=json.dumps(alg_exec_params, ensure_ascii=False),
#         headers={
#             'Content-Type': 'application/json',
#             'tenant-id' : tenant_id,
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
#     })
# if response.status_code == 200:
#     try:
#         json_obj = json.loads(response.text)
#         json_obj = json.loads(json_obj["data"]["result"])
#         past_values = json_obj["pastValue"]
#         pre_values = json_obj["preValue"]
#         print(json_obj)
#     except Exception as e:
#         print("解析推理结果失败，返回结果：" + response.text)
# else:
#     print("调用推理API出现异常，返回结果：" + response.text)


# # 模型在线推理前的数据处理
# alg_data_eval_params = {
#     "id": "019a58c3-f2e8-78a1-ba4b-7b01ac0cda72",
#     "task_type" : 2,
#     "online_data": False,
#     "csv_path": "s3://agent-runner.public/0/0/ab92b40217fe4e18aff6d79d7409f357_output.csv",
#     "prediction_length": "",
#     "frequency": 0,
#     "target_variables": ["CokeRate", "yield"],
#     "input_variables": ["average_furnace_temp"]
# }
#
# url='http://10.30.73.42:31668/call/app?name=tptmoe_create_data_sample_py&built_in=1&time_out=600'
# response = requests.post(
#     url = url,
#     data= json.dumps(alg_data_eval_params, ensure_ascii=False),
#     headers={
#         'Content-Type': 'application/json',
#         'tenant-id' : tenant_id,
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
# })
# if response.status_code == 200:
#     try:
#         json_obj = json.loads(response.text)
#         json_obj_data_eval = json.loads(json_obj["data"]["result"])
#     except Exception as e:
#         print("执行推理数据处理结果失败，返回结果：" + response.text)
# else:
#     print("执行推理数据处理出现异常，返回结果：" + response.text)

# tolerance_info = [
#     {
#       "tag": "XX.LJS.FIC_2A221A.PV",
#       "description": "FV_2A221A（进电解槽纯水流量调节）测量值",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 2.89,
#       "pointToleranceValue": 2.89,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.FIC_2A221A.PV",
#       "tagsDescription": "FV_2A221A（进电解槽纯水流量调节）测量值",
#       "unit": "m3/h"
#     },
#     {
#       "tag": "XX.LJS.TT_2A234A.PV",
#       "description": "A线.电槽A单槽槽温显示",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 2.81,
#       "pointToleranceValue": 2.81,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.TT_2A234A.PV",
#       "tagsDescription": "三线电解电槽A单槽槽温",
#       "unit": "℃"
#     },
#     {
#       "tag": "XX.LJS.TT_2A234B.PV",
#       "description": "A线.电槽B单槽槽温显示",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 1.76,
#       "pointToleranceValue": 1.76,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.TT_2A234B.PV",
#       "tagsDescription": "三线电解电槽B单槽槽温",
#       "unit": "℃"
#     },
#     {
#       "tag": "XX.LJS.TT_2A234C.PV",
#       "description": "A线.电槽C单槽槽温显示",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 1.7,
#       "pointToleranceValue": 1.7,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.TT_2A234C.PV",
#       "tagsDescription": "三线电解电槽C单槽槽温\t",
#       "unit": "℃"
#     },
#     {
#       "tag": "XX.LJS.TT_2A234D.PV",
#       "description": "A线.电槽D单槽槽温显示",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 4.86,
#       "pointToleranceValue": 4.86,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.TT_2A234D.PV",
#       "tagsDescription": "三线电解电槽D单槽槽温\t",
#       "unit": "℃"
#     },
#     {
#       "tag": "XX.LJS.TT_2A234E.PV",
#       "description": "A线.电槽E单槽槽温显示",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 2.19,
#       "pointToleranceValue": 2.19,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.TT_2A234E.PV",
#       "tagsDescription": "三线电解电槽E单槽槽温\t",
#       "unit": "℃"
#     },
#     {
#       "tag": "XX.LJS.TT_2A234F.PV",
#       "description": "A线.电槽F单槽槽温显示",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 1.72,
#       "pointToleranceValue": 1.72,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.TT_2A234F.PV",
#       "tagsDescription": "三线电解电槽F单槽槽温\t",
#       "unit": "℃"
#     },
#     {
#       "tag": "XX.LJS.TT_2A234G.PV",
#       "description": "A线.电槽G单槽槽温显示",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 1.69,
#       "pointToleranceValue": 1.69,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.TT_2A234G.PV",
#       "tagsDescription": "三线电解电槽G单槽槽温\t",
#       "unit": "℃"
#     },
#     {
#       "tag": "XX.LJS.TT_2A234H.PV",
#       "description": "A线.电槽H单槽槽温显示",
#       "highFilteringFactor": 0.8,
#       "lowFilteringFactor": 0.2,
#       "trendToleranceValue": 1.76,
#       "pointToleranceValue": 1.76,
#       "X_H0": "",
#       "X_L0": "",
#       "isStart": True,
#       "tags": "XX.LJS.TT_2A234H.PV",
#       "tagsDescription": "三线电解电槽H单槽槽温\t",
#       "unit": "℃"
#     }
#   ]
# ssd_info_param = {
#         "online_data": True,    #是否读取在线数据,True为读在线数据，False为读离线数据
#         "csv_path": "",
#         "tolerance_info": tolerance_info
#     }
#
# url='http://10.30.73.42:31668/call/app?name=TPT-SSD2_py&built_in=1&time_out=600'
# response = requests.post(
#     url=url,
#     data=json.dumps(ssd_info_param, ensure_ascii=False).encode('utf-8'),
#     headers={
#         'Content-Type': 'application/json',
#         'tenant-id' : tenant_id,
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
#     })
# json_obj = json.loads(response.text)
# print(f'请求参数为:{ssd_info_param},返回结果为:{response.text}')
# read_tolerance_data = json.loads(json_obj["data"])
# print(read_tolerance_data["tolerance_info"])





ssd_info_param = {"csv_path": "", "tolerance": [{"tag": "XX.LJS.FIC_2A221A.PV", "description": "FV_2A221A（进电解槽纯水流量调节）测量值", "upper": 24, "lower": 18, "step": 6, "unit": "m3/h"}, {"tag": "XX.LJS.TT_2A234A.PV", "description": "A线.电槽A单槽槽温显示", "upper": 88, "lower": 80, "step": 8, "unit": "℃"}, {"tag": "XX.LJS.TT_2A234B.PV", "description": "A线.电槽B单槽槽温显示", "upper": 88, "lower": 80, "step": 8, "unit": "℃"}, {"tag": "XX.LJS.TT_2A234C.PV", "description": "A线.电槽C单槽槽温显示", "upper": 88, "lower": 80, "step": 8, "unit": "℃"}, {"tag": "XX.LJS.TT_2A234D.PV", "description": "A线.电槽D单槽槽温显示", "upper": 88, "lower": 80, "step": 8, "unit": "℃"}, {"tag": "XX.LJS.TT_2A234E.PV", "description": "A线.电槽E单槽槽温显示", "upper": 88, "lower": 80, "step": 8, "unit": "℃"}, {"tag": "XX.LJS.TT_2A234F.PV", "description": "A线.电槽F单槽槽温显示", "upper": 88, "lower": 80, "step": 8, "unit": "℃"}, {"tag": "XX.LJS.TT_2A234G.PV", "description": "A线.电槽G单槽槽温显示", "upper": 88, "lower": 80, "step": 8, "unit": "℃"}, {"tag": "XX.LJS.TT_2A234H.PV", "description": "A线.电槽H单槽槽温显示", "upper": 88, "lower": 80, "step": 1, "unit": "℃"}]}

url='http://10.30.73.42:31668/call/app?name=TPT-SSD1_py&built_in=1&time_out=600'
response = requests.post(
    url=url,
    data=json.dumps(ssd_info_param, ensure_ascii=False).encode('utf-8'),
    headers={
        'Content-Type': 'application/json',
        'tenant-id' : "0",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    })
print(response.text)
json_obj = json.loads(response.text)
read_data = json.loads(json_obj["data"]["result"])










