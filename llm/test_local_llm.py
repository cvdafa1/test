from openai import OpenAI

# 关键：将客户端指向你本地的Ollama服务
client = OpenAI(
    base_url="http://localhost:11434/v1", # Ollama的固定本地地址
    api_key="none" # 不需要密钥，但必须提供，可以任意填写
)

# 你的提问
stream_mode = True

# 发送请求，格式与OpenAI完全相同！
response = client.chat.completions.create(
    model="llama3.2:1b", # 必须与你pull的模型名一致
    messages=[
        {"role": "user", "content": '请用 Python 写一个快速排序算法'}
    ],
    stream=stream_mode, # 是否使用流式输出
    temperature=0.7 # 控制创造性
)

if stream_mode:
    # 流式输出处理
    full_response = ""
    for chunk in response:
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
    print()  # 换行

else:
    # 非流式输出处理
    content = response.choices[0].message.content
    print(content)
