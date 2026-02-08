# OpenAI接口
# from openai import OpenAI
# client = OpenAI(
#     base_url="http://172.23.216.104:5000/v1/",  # 注意末尾 /
#     api_key="sk-xxx",
# )

# completion = client.chat.completions.create(
#     model="Qwen1.5-7B-Chat",
#     messages=[{"role": "user", "content": "你是谁"}]
# )

# print(completion.choices[0].message)


# request请求
# import requests
# url = "http://172.23.216.104:5000/generate"
# data = {"prompt": '你是谁'}

# resp = requests.post(url, json=data)
# print(resp.text)

# LangChain框架
from langchain_openai import ChatOpenAI
import os
import dotenv

# 前提：加载配置文件
dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# 1、获取对话模型
chat_model = ChatOpenAI(
    model="Qwen2.5-14B-Instruct",
)

# 2、调用对话模型
response = chat_model.invoke("大模型中的LlamaIndex是什么")
# response = chat_model.invoke("你是谁")

# 3、处理响应数据
# print(response)
print(response.content)
print(type(response))  #<class 'langchain_core.messages.ai.AIMessage'>
