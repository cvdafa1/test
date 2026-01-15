import requests
import socket
from flask import Flask, Response

# server.py
from flask import Flask, Response
import time
import json

app = Flask(__name__)


@app.route('/sse')
def sse_stream():
    def generate():
        # 模拟训练日志数据
        messages = [
            {"event": "start", "message": "训练开始", "progress": 0},
            {"event": "epoch", "message": "第1轮训练", "loss": 0.85, "progress": 10},
            {"event": "epoch", "message": "第2轮训练", "loss": 0.72, "progress": 20},
            {"event": "epoch", "message": "第3轮训练", "loss": 0.61, "progress": 30},
            {"event": "epoch", "message": "第4轮训练", "loss": 0.53, "progress": 40},
            {"event": "epoch", "message": "第5轮训练", "loss": 0.46, "progress": 50},
            {"event": "complete", "message": "训练完成", "accuracy": 0.92, "progress": 100}
        ]

        for msg in messages:
            yield f"data: {json.dumps(msg)}\n\n"
            time.sleep(1)  # 每秒发送一条

        # 发送完数据保持连接
        while True:
            time.sleep(1)  # 防止 CPU 占用过高
    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(port=5000, debug=True)