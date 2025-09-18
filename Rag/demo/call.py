from save_db import chromadb_collection
from embed import embeded_chunks
def retrive(query,top_k) -> list[str]:
  query_embedding = [embedding.values for embedding in embeded_chunks(query)]
  result = chromadb_collection.query(
    query_embeddings=query_embedding,
    n_results=top_k
  )
  return result['documents'][0]

# query = '令狐冲领悟了什么魔法'

# 召回有问题
query = '令狐冲逝世前最后的念头是什么'
retrived_chunks = retrive(query=query,top_k=5)
for i,chunk in enumerate(retrived_chunks):
  print(f"[{i}]{chunk}\n")