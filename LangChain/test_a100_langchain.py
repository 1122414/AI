# # LangChain框架
# import os
# import dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage,HumanMessage

# # 前提：加载配置文件
# dotenv.load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# # 1、获取对话模型
# chat_model = ChatOpenAI(
#     model="Qwen2.5-14B-Instruct",
# )

# system_message = SystemMessage(content="你是一个AI调教专家,你叫小智")
# human_message = HumanMessage(content="大模型中的LlamaIndex是什么")

# messages = [system_message, human_message]

# # 2、调用对话模型
# response = chat_model.invoke(messages)

# response = chat_model.invoke("你叫什么名字，请只回答一句话，不要解释。")

# # 3、处理响应数据
# # print(response)
# print(response.content)
# print(type(response))  #<class 'langchain_core.messages.ai.AIMessage'>

import asyncio
import os
import time

import dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

# 初始化大模型
chat_model = ChatOpenAI(model="Qwen2.5-1.5B-Instruct")

example_prompt = PromptTemplate.from_template(
  "input:{input}\noutput:{output}"
)

examples = [
  {"input": "北京天气怎么样", "output": "北京市"},
  {"input": "南京下雨吗", "output": "南京市"},
  {"input": "武汉热吗", "output": "武汉市"}
]

few_shot_template = FewShotPromptTemplate(
  example_prompt = example_prompt,
  examples = examples,
  suffix = "input:{input}\noutput:",
  input_variables=["input"]
)

response = chat_model.invoke(few_shot_template.invoke({"input":"天津会下雨吗？只给出一个城市名，不要多输出"}))
print(response.content)