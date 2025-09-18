from sentence_transformers import CrossEncoder
from call import query
from call import retrived_chunks
from transformers import AutoTokenizer, AutoModelForCausalLM
# 不准确
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-Reranker-8B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-Reranker-8B")

def rerank(query,retrived_chunks,top_k)->list[str]:
  cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')
  # cross_encoder = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L2-v2')
  pairs = [(query,chunk) for chunk in retrived_chunks]
  scores = cross_encoder.predict(pairs)
  
  chunk_with_score_list = [
    (chunk,score) for chunk,score in zip(retrived_chunks,scores)
  ]
  chunk_with_score_list.sort(key=lambda pair:pair[1], reverse=True)
  return [chunk for chunk, _ in chunk_with_score_list][:top_k]

chunk_with_score_list = rerank(query=query,retrived_chunks=retrived_chunks,top_k=5)

for i, chunk in enumerate(chunk_with_score_list):
  print(f"排序后的chunksL：[{i}]{chunk}")


# region 网络走不通
# from google.cloud import discoveryengine_v1 as discoveryengine

# client = discoveryengine.RankServiceClient()
# request = discoveryengine.RankRequest(
#     model="semantic-ranker-512@latest",
#     top_n=3,  # 返回前3个排序结果
#     query=query,
#     records=[
#       discoveryengine.RankingRecord(id=str(i),content=chunk) for i,chunk in enumerate(retrived_chunks)
#     ]
# )
# response = client.rank(request=request)
# for rec in response.records:
#   print(f"ID: {rec.id}, Score: {rec.score}")
# endregion

# from google.cloud import discoveryengine_v1 as discoveryengine
# from google.oauth2 import service_account

# JSON_KEY = r"E:/GitHub/ornate-charter-455414-p0-cccf298e07cf.json"
# creds = service_account.Credentials.from_service_account_file(JSON_KEY)

# client = discoveryengine.RankServiceClient(credentials=creds)

# # 确保 retrived_chunks 每项是可转成字符串的
# records = []
# for i, chunk in enumerate(retrived_chunks):
#     # debug: 打印类型，方便定位非字符串问题
#     # print(i, type(chunk), repr(chunk)[:200])
#     records.append(
#         discoveryengine.RankingRecord(
#             id=str(i),          # ✅ 强制转成 str
#             content=str(chunk)  # ✅ 强制转成 str（如果 chunk 里是 dict, 请取具体字段）
#         )
#     )

# request = discoveryengine.RankRequest(
#     model="projects/ornate-charter-455414-p0/locations/global/dataStores/resort-data/servingConfigs/semantic-ranker-512@latest",
#     top_n=3,          # gRPC 字段名是 top_n
#     query=query,
#     records=records
# )

# response = client.rank(request=request)
# for rec in response.records:
#     print(f"ID: {rec.id}, Score: {rec.score}")
