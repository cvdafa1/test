import requests
from langchain.llms.base import LLM
from typing import Optional, List


# 1. 定义简单的本地模型类
class SimpleLocalLLM(LLM):
    api_url: str = "http://localhost:8000/v1/chat/completions"  # 修改为你的接口地址

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # 调用本地模型API
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        try:
            response = requests.post(self.api_url, json=data, timeout=30)
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"错误: {e}"

    @property
    def _llm_type(self) -> str:
        return "simple_local"


# 2. 创建工作流
def simple_workflow():
    # 初始化本地模型
    llm = SimpleLocalLLM()

    # 示例1: 直接问答
    print("=== 简单问答 ===")
    question = "什么是人工智能？"
    answer = llm(question)
    print(f"问题: {question}")
    print(f"回答: {answer}\n")

    # 示例2: 文档分析工作流
    print("=== 文档分析工作流 ===")
    document = """
    Python是一种高级编程语言，具有简单易学的特点。
    它广泛应用于Web开发、数据分析、人工智能等领域。
    Python拥有丰富的第三方库，如NumPy、Pandas、TensorFlow等。
    """

    # 步骤1: 总结文档
    summary_prompt = f"请用一句话总结以下文本：\n{document}"
    summary = llm(summary_prompt)
    print(f"文档总结: {summary}\n")

    # 步骤2: 提取关键点
    key_points_prompt = f"从以下文本中提取3个关键点：\n{document}"
    key_points = llm(key_points_prompt)
    print(f"关键点: {key_points}\n")

    # 步骤3: 回答问题
    qa_prompt = f"基于以下文本回答问题：'{document}'\n\n问题：Python主要用于哪些领域？"
    answer = llm(qa_prompt)
    print(f"问题回答: {answer}")


# 运行示例
if __name__ == "__main__":
    simple_workflow()