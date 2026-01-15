from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
prompt_template = PromptTemplate.from_template("告诉我关于 {topic} 的有趣事实。")
chain = LLMChain(llm=Ollama(
    model="llama3.2:1b",                        # ⚠️ 你指定的模型名称
), prompt=prompt_template)

result = chain.run({"topic": "太空"})
print(result)






