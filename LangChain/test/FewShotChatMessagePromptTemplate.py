import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import FewShotChatMessagePromptTemplate,ChatPromptTemplate

dotenv.load_dotenv()

os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

chat_model = ChatOpenAI(
  model="Qwen2.5-14B-Instruct"
)

examples = [
  {"input": "2🦜2", "output": "4"},
  {"input": "2🦜3", "output": "6"},
  {"input": "2🦜4", "output": "8"},
  {"input": "2🦜5", "output": "10"},
]

example_prompt = ChatPromptTemplate.from_messages(
  [
    ('human', '{input} 是多少?'),
    ('ai', '{output}')
  ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
  examples=examples,
  example_prompt=example_prompt
)

final_prompt = ChatPromptTemplate.from_messages(
  [
    ('system', '你是一个中国的数学奇才'),
    few_shot_prompt,
    ('human', '{input}'),
  ]
)

print(chat_model.invoke(final_prompt.invoke(input="请输出并只输出这个式子的答案：3🦜15=？不要带有其他任何信息")).content)