import requests
import json
import time

def test_sse_services():
    # 可用的测试地址列表
    url  = "http://localhost:5000/sse"

    print(f"\n🔗 测试: {url}")
    try:
        with requests.get(url, stream=True, timeout=(10,10)) as response:
            print(f"✅ 连接成功: HTTP {response.status_code}")
            if response.status_code == 200:
                start = time.time()
            # 读取前3条消息测试
            count = 0
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data:'):
                        data = decoded[5:].strip()
                        print(f"📨 收到: {data}")
                        count += 1
                print(time.time() - start)
                if time.time() - start > 60:
                    break
            print("✅ 测试通过")

    except Exception as e:
        print(f"❌ 错误: {e}")


# 运行测试
if __name__ == "__main__":
    test_sse_services()