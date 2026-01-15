#!/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
import multiprocessing
import os
import time
import json
from idlelib.window import add_windows_to_menu

import redis
import requests
from datetime import datetime
from redis.cluster import RedisCluster, ClusterNode
import ast

class Config:
    #dev
    # REDIS_HOST = "seak8sm1.supcon5t.com"  # redis地址/stream_train_logs/
    # REDIS_PORT = 26379  # redis端口
    # RUNTIME_URL = "http://10.30.73.42:31668/stream_train_logs/"  # 运行时sse调用接口
    # TPT_MOE_TRAIN_TOPIC = "single_python_tpt_tptmoe_alg"  # 发送训练算法参数执行topic
    # # local
    REDIS_HOST = "10.51.1.117"
    REDIS_PORT = 30379
    RUNTIME_URL = "http://10.30.75.34:8080/stream_train_logs/"  # 运行时sse调用接口
    TPT_MOE_TRAIN_TOPIC = "single_python_train_alg_h"  # 发送训练算法参数执行topic

    # test
    # REDIS_HOST = "gateway.supcon5t.com"
    # REDIS_PORT = 16379
    # RUNTIME_URL = "http://10.30.73.42:31667/stream_train_logs/"  # 运行时sse调用接口
    # TPT_MOE_TRAIN_TOPIC = "single_python_tpt_tptmoe_alg"  # 发送训练算法参数执行topic


    REDIS_DB = 2  # redis数据库
    REDIS_CLUSTER_NODES = ""  # redis集群




    TIME_OUT = 7200  # 算法执行超时时间
    SSE_TIME_OUT = 600   # sse连接超时时间


    #tpt-moe相关新的配置
    TPT_MOE_ALG_NAME = "tptmoe"
    TPT_MOE_ALG_FULL_NAME = "tptmoe.zip"

    # TPT_MOE_ALG_NAME = "AutoMLTransformerTrain"
    # TPT_MOE_ALG_FULL_NAME = "AutoMLTransformerTrain.zip"
    TPT_MOE_TRAIN_REDIS_END_PRE = "TRAIN:TPTMOE:"  # 算法管理监听redis存储算法执行结果前缀
    TPT_MOE_TRAIN_REDIS_RESULT_PRE = "tptmoe_"  # 训练算法自己发送redis结果key前缀
    TPT_MOE_TRAIN_LOSS_KEYWORD = "#SEPERATE#" #训练过程中发送的loss数据关键字



# 执行tpt-moe模型训练算法
async def execute_tpt_moe_train(params: any):
    tenant_id = params["tenant_id"]
    clientId = params["clientId"]
    target_variables = params["target_variables"]
    input_variables= params["input_variables"]
    task_type =  params["task_type"]
    model_full_name = params["model_full_name"]
    prediction_length = params["prediction_length"] #预测时的预测时长
    csv_path = params["csv_path"] 
    alg_name = Config.TPT_MOE_ALG_NAME
    alg_full_name = Config.TPT_MOE_ALG_FULL_NAME
    topic = Config.TPT_MOE_TRAIN_TOPIC
    redis_end_pre = Config.TPT_MOE_TRAIN_REDIS_END_PRE
    redis_result_pre = Config.TPT_MOE_TRAIN_REDIS_RESULT_PRE

    r = None
    message = ""
    execute_status = 1
    result = None
    cur_time = str(int(time.time() * 1000))
    input_params = [
        {
            "defaultValue": "",
            "name": "id",
            "type": 1,
            "typeName": "str",
            "userInput": 1,
            "value": clientId
        },
        {
            "defaultValue": "",
            "name": "target_variables",
            "type": 9,
            "typeName": "list",
            "userInput": 1,
            "value": json.dumps(target_variables)
        },
        {
            "defaultValue": "",
            "name": "input_variables",
            "type": 9,
            "typeName": "list",
            "userInput": 1,
            "value": json.dumps(input_variables)
        },
        {
            "defaultValue": "",
            "name": "task_type",
            "type": 4,
            "typeName": "int",
            "userInput": 1,
            "value": str(task_type)
        },
         {
            "defaultValue": "",
            "name": "prediction_length",
            "type": 4,
            "typeName": "int",
            "userInput": 1,
            "value": str(prediction_length)
        },
        {
            "defaultValue": "",
            "name": "model_full_name",
            "type": 1,
            "typeName": "str",
            "userInput": 1,
            "value": model_full_name
        },
        {
            "defaultValue": "",
            "name": "csv_path",
            "type": 1,
            "typeName": "str",
            "userInput": 1,
            "value": csv_path
        },
        {
            "defaultValue": "",
            "name": "microContent",
            "type": 13,
            "typeName": "json",
            "userInput": 1,
            "value": f'{{"deviceTypeName": "gpu", "gpuNo": 1}}' # 确认算法走cpu还是npu
        }
    ]
    print(json.dumps(input_params, ensure_ascii=False))
    output_params = [
        {
            "name": "res",
            "type": 1,
            "typeName": "str"
        }
    ]
    algorithm = {
        "algorithm": {
            "builtIn": 1,
            "input": input_params,
            "name": alg_name,
            "sourcePath": alg_full_name,
            "output": output_params
        },
        "id": clientId,
        "tableName": "",
        "type": "redis",
        "curTime": cur_time
    }
    try:
        r = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)
        # if(context.config["redis_cluster"] == 1):
        #    Config.REDIS_CLUSTER_NODES = [ClusterNode(host=context.config["redis_host"], port=context.config["redis_port"])]  # redis集群
        #    r = RedisCluster(startup_nodes=Config.REDIS_CLUSTER_NODES, decode_responses=True)
        # else :
        #     r = redis.Redis(host=context.config["redis_host"], port=context.config["redis_port"], db=Config.REDIS_DB)
        # r = redis.Redis(host="10.51.1.117", port=30379, db=Config.REDIS_DB)
        r = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)
        r.xadd(
            "runtime_python_stream:" + topic,
            {"tenant_id": tenant_id, "value": json.dumps(algorithm, ensure_ascii=False)},
            id='*'
        )

        await tptmoe_sse_client(clientId,tenant_id, alg_full_name, cur_time ,r)

        # start = time.time()
        # while True:
        #     time.sleep(2)
        #     execute_res = r.get(tenant_id + ":" + redis_end_pre + clientId)
        #     # redis_implementation_key = Config.TENANT_ID + ":" + redis_end_pre + clientId
        #     # await context.log_info(f"redis_implementation_key = {redis_implementation_key}")
        #     if execute_res is not None:
        #         json_array = json.loads(execute_res)
        #         if json_array[0].get("implementation") == 1:
        #             message = json_array[0].get("logInfo")
        #             result = r.get(tenant_id +":"+ redis_result_pre + clientId)
        #             # redis_result_key = redis_pre + clientId
        #             # await context.log_info(f"redis_result_key = {redis_result_key}")
        #             result = None if result is None else json.loads(result)
        #             break
        #         if json_array[0].get("implementation") == 2:
        #             message = json_array[0].get("errorInfo")
        #             if(message == ""):
        #                 message = json_array[0].get("logInfo")
        #             execute_status = 2
        #             break
        #     if time.time() - start > Config.TIME_OUT:
        #         execute_status = 2
        #         message = "Executing timeout"
        #         break
    finally:
        if r is not None:
            r.close()
    res = {
        "message": message,
        "executeStatus": execute_status,  # 1成功, 2失败
        "result": result
    }
    # await context.log_info(f"res = {res}")
    return res





async def tptmoe_sse_client(client_id: str,tenant_id: str, sourcePath: str, cur_time: str,r: any):
    #print("调用sse_client方法")
    params = {
        "sourcePath": sourcePath,
        "client_id": client_id,
        "cur_time": cur_time
    }
    headers = {
        "Accept": "text/event-stream",
        "tenant-id": tenant_id
    }
    #response = requests.get(Config.RUNTIME_URL + client_id, params=params, headers=headers, stream=True)
    line = ''
    try:
        key = f'train_logs:{tenant_id}:{os.path.splitext(sourcePath)[0]}_{client_id}_{cur_time}'
        print(f'需要获取的key为{key}')
        sse_start = time.time()
        while True:
            try:
                if r.xinfo_stream(key):
                    break
            except Exception as e:
                pass
            if time.time() - sse_start > Config.SSE_TIME_OUT:
                break
            print(f'未获取到{key}')
            time.sleep(1)
        print(f"获取到了{key}开始调用")
        # with requests.get(context.config["sse_model_train_log_url"] + client_id, params=params, headers=headers, stream=True) as response:
        with requests.get(Config.RUNTIME_URL + client_id, params=params, headers=headers, stream=True) as response:
            print(response.status_code)
            if response.status_code == 200:
                start = time.time()
                log_str = ""
                for line in response.iter_lines(decode_unicode=True):
                    print(f"读取到的行信息:{line}-{time.time()}")
                    if Config.TPT_MOE_TRAIN_LOSS_KEYWORD in line:
                        # time.sleep(1)  #显示曲线,小于1秒的按1秒
                        field, value = line.split(Config.TPT_MOE_TRAIN_LOSS_KEYWORD, 1)
                        value = value.lstrip()
                        log_str += value
                        print(f'读取到的key信息:{value}')
                        # loss_data = json.loads(r.get(value))["train_loss"] #通过print的key读redis中的中间loss结果,需要转utf-8
                        # print(f'读取到的loss数据{loss_data}')
                    if "event" in line:
                        log_str += "---   " + line
                        #print("关闭连接")
                        if "ended" in line:
                            break
                    if time.time() - start > Config.TIME_OUT:
                        break
            else:
                raise ValueError(f"连接失败：{response.status_code}")
            #print("连接失败")
    except Exception as e:
        raise ValueError(f"连接失败:{str(e)}") from e





if __name__ == '__main__':
    # 调用异步函数
    async def main():
        print("开始调用异步函数...")
        params = {"tenant_id":"0","clientId":"01990968-a4a2-77895-843c-697t66779d1","task_type":"1","model_full_name":"finetune/0/yxlmodel_20251020140857","target_variables":
        ["18PDT_1001B.PV","P_1806C_II.PV","17FIC1016.PV"],"input_variables":["18TT_1013.PV","17LT_1006A.PV"],"prediction_length":"12","csv_path":"s3://data/moe/0/f86bf3f87b7a4a38b8568ffb1fa9eb6a/5d23a4c4f5a44beea3e53dd11d98843c_数据 -5k - 空行空列.csv"

        }
        result = await execute_tpt_moe_train(params=params)
        print(result)


    # 运行异步主函数
    asyncio.run(main())

