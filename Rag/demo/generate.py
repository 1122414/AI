from dotenv import load_dotenv
from google import genai
from call import query
from call import retrive
from resort import rerank

load_dotenv()
google_client = genai.Client()

def generate (query,chunks) -> str:
  promt = f'''
  你是一个知识助手，请根据用户的问题和下列片段生成准确回答。
  用户问题：{query}
  相关片段：{"\n\n".join(chunks)}
  请基于以上信息作答，不要编造信息
  '''
  print(f"{promt}\n\n---\n")
  response = google_client.models.generate_content(
    model="gemini-2.5-flash",
    contents=promt
  )
  return response.text

temp_chunks = retrive(query=query,top_k=5)
chunks = rerank(query=query,retrived_chunks=temp_chunks,top_k=5)
answer = generate(query=query,chunks=chunks)

print(answer)