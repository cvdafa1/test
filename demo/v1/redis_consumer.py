import json

import redis
import time
import threading

# 连接Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 定义Stream名称和消费者组名称
STREAM_NAME = 'order_events'
GROUP_NAME = 'order_processors'


def consumer(consumer_name):
    """消费者函数"""
    print(f"Consumer {consumer_name} started")
    while True:
        try:
            # 从消费者组读取消息
            messages = r.xreadgroup(
                GROUP_NAME, consumer_name,
                {STREAM_NAME: '>'},
                count=1,
                block=5000
            )

            if not messages:
                continue
            for stream, message_list in messages:
                for message_id, message_data in message_list:
                    print(message_data)
                    if  b'data' in message_data.keys():
                        message_data = message_data[b'data'].decode('utf-8')  # This gives you the JSON string
                        message_data = json.loads(message_data)
                        order_id = message_data['order_id']
                        print(f"{consumer_name} processing order {order_id}")

                        # 模拟处理时间
                        time.sleep(2)

                        # # 更新订单状态
                        # r.xadd(STREAM_NAME, {
                        #     'order_id': order_id,
                        #     'status': 'processed',
                        #     'consumer': consumer_name,
                        #     'timestamp': str(time.time())
                        # })
                        #
                        # # 确认消息已处理
                        r.xack(STREAM_NAME, GROUP_NAME, message_id)
                        print(f"{consumer_name} completed order {order_id}")
                    else:
                        print("未产生新消息")

        except Exception as e:
            print(f"Error in consumer {consumer_name}: {e}")
            time.sleep(5)





if __name__ == '__main__':
    # 启动多个消费者
    consumers = ['consumer1']
    for name in consumers:
        threading.Thread(target=consumer, args=(name,), daemon=True).start()

    # 主线程等待
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")