# server.py - FastAPI + WebSocket
import json
from fastapi import WebSocket, APIRouter, Request
from message.msg_sql import create_message, SessionLocal, get_all_messages

router = APIRouter()


# 存储连接的客户端
connections = []

# 创建数据库会话
db = SessionLocal()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # 1. 接受连接
    connections.append(websocket)

    try:
        # 2. 监听前端消息
        while True:
            data = await websocket.receive_text()
            print(f"收到前端消息: {data}")
            msg1 = create_message(db, str(data))
            # 3. 后端主动推送
            response = f"后端回复: 你发了 '{data}'"
            await websocket.send_text(response)

    except Exception as e:
        connections.remove(websocket)
        print(f"连接关闭: {e}")


@router.post("/msg")
async def msg_func(request: Request):
    # 获取所有 Header
    headers = dict(request.headers)

    # 获取所有 Cookie
    cookies = dict(request.cookies)

    # 获取查询参数
    query_params = dict(request.query_params)

    # 获取请求体
    try:
        body = await request.json()
    except:
        body = await request.body()
        try:
            body = json.loads(body)
        except:
            body = str(body)

    # 获取请求方法
    method = request.method

    # 获取客户端信息
    client = request.client
    client_host = client.host if client else None
    client_port = client.port if client else None

    return {
        "method": method,
        "url": str(request.url),
        "client": {
            "host": client_host,
            "port": client_port
        },
        "headers": headers,
        "cookies": cookies,
        "query_params": query_params,
        "body": body
    }


@router.post("/get_msg")
async def get_msg(request: Request):
    # 获取请求体
    try:
        body = await request.json()
    except:
        body = await request.body()
        try:
            body = json.loads(body)
        except:
            body = str(body)

    print(f"body: {body}")
    msg = get_all_messages(db)
    msg = list(msg)
    print(f"msg: {msg}")
    return {
        "data": msg
    }

# 后端定时主动推送任务
# @app.on_event("startup")
# async def startup_event():
#     """启动后台推送任务"""
#
#     async def broadcast_updates():
#         count = 0
#         while True:
#             await asyncio.sleep(3)  # 每3秒推送
#             count += 1
#             message = f"系统消息 {count}"
#
#             # 向所有客户端推送
#             for connection in connections.copy():
#                 try:
#                     await connection.send_text(message)
#                 except:
#                     connections.remove(connection)
#
#     asyncio.create_task(broadcast_updates())


