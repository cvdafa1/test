import ast
import asyncio
import json
import random

import requests

prompt_str = f"""
        #角色
        你是一个专业的问题分析师，能够对输入的数据进行精确解读与分析。
        ###技能
        1. 接收用户输入的问题，问题内容如下：
        一次盐水折流槽pH无法通过PID、APC控制，请用AI实现pH控制。
        2. 根据问题的描述，生成该工业场景下可能会出现的参数。如操作变量MV、被控变量PV、压力、液位、酸碱度、温度、湿度、流量、阀门开度、浓度等。其中必须包含操作变量MV和被控变量PV。
        3. 返回时以列表的格式返回，例如["操作变量MV","被控变量PV","浓度","压力","液位","温度","湿度"]。
        4. 尽量更多的可能出现的工业参数。
        ##限制
        - 只返回列表格式，不需要任何字符串文字。
        - 返回的工业参数不少于10个。
        - 返回的工业参数要契合用户输入的问题。
        /no_think
        """

llm_params = {
            "model": "qwen3",
            "messages": [{
                "role": "user",
                "content": prompt_str
            }]
        }
response = requests.post(
    url= "http://nlb-2weu6cb4a97uoz9cqu39kvmj.nlb.cn-beijing.volces.com:32004/v1/chat/completions",
    data=json.dumps(llm_params, ensure_ascii=False),
    headers={
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
})
if response.status_code == 200:
    llm_resp = response.json().get("choices")[0].get("message").get("content")
else:
    success = -1
    llm_resp = response.text
print(llm_resp)
llm_resp_list = ast.literal_eval(llm_resp)
print(llm_resp_list)
tag_list = [f'tag{i+1}' for i in range(len(llm_resp_list))]
random_numbers = [random.randint(1, 100) for _ in range(len(llm_resp_list))]
rows = [
    ['Timestamp'] + tag_list,
    ['时间戳'] + llm_resp_list,
    ['2024/5/31 1:55:00'] + random_numbers,
    ['tips:'],
    ['1、前两行固定不变，第一行是位号名称，第二行是位号描述，第三行是位号数据；'],
    ['2、时间戳固定为‘Timestamp’；'],
    ['3、tag1、tag2...为示例位号，应用时修改为实际位号，实际位号中必须包含：操作变量MV和被控变量PV；'],
    ['4、推荐采样周期为10s，时间戳可参考左边格式：时间戳格式YYYY/MM/DD HH:MM:SS；'],
    ['5、建议行数不少于50000行。']
]
csv_string = '\n'.join([','.join(map(str, row)) for row in rows])
bom = b"\xef\xbb\xbf"
report_file_path = "数据上传模板.csv"
with open(report_file_path, 'w', encoding='utf-8') as f:
    f.write(csv_string)