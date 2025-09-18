import chromadb
from chunks import get_chunks
from embed import embeded_chunks
chromadb_client = chromadb.EphemeralClient()
chromadb_collection = chromadb_client.get_or_create_collection(name="rag_demo")

def save_embeddings(chunks,embddings) -> None:
  ids = [str(i) for i in range(len(chunks))]
  chromadb_collection.add(
    documents=chunks,
    embeddings=embddings,
    ids=ids
  )

chunks = get_chunks()
embeddings = [embedding.values for embedding in embeded_chunks(chunks)]
save_embeddings(chunks=chunks, embddings=embeddings)