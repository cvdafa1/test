# app/main.py
from fastapi import FastAPI
import uvicorn
from message import msg

app = FastAPI()

# 导入并包含所有路由器
app.include_router(msg.router, prefix="/api/v1", tags=["msg"])


# 启动: uvicorn server:app --reload
if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发时开启热重载
        workers=1  # 生产环境可增加worker数量
    )