import json
import random

import redis
import time
import threading

# 连接Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 定义Stream名称和消费者组名称
STREAM_NAME = 'order_events'
GROUP_NAME = 'order_processors'


def producer():
    """生产者函数"""
    order_id = 1000
    while True:
        try:
            order_id += 1
            message = {
                'order_id': str(order_id),
                'status': 'created',
                'timestamp': str(time.time())
            }
            r.xadd(STREAM_NAME, {'data': json.dumps(message)})
            print(f"Produced order {order_id}")
            time.sleep(random.uniform(0.5, 2))
        except Exception as e:
            print(f"Producer error: {e}")
            time.sleep(5)

def monitor_pending_messages():
    """监控未确认消息"""
    while True:
        pending = r.xpending(STREAM_NAME, GROUP_NAME)
        print(f"Pending messages: {pending}")
        time.sleep(10)

if __name__ == '__main__':
    # 初始化消费者组
    try:
        r.xgroup_create(STREAM_NAME, GROUP_NAME, id='0', mkstream=True)
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise

    # 启动监控线程
    threading.Thread(target=monitor_pending_messages, daemon=True).start()

    # 启动生产者
    threading.Thread(target=producer, daemon=True).start()
    # 主线程等待
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")