from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
from google import genai
load_dotenv()

google_client = genai.Client()
EMDEDDING_MODEL = 'gemini-embedding-exp-03-07'

def embeded_chunks(text) -> list[float]:
  result = google_client.models.embed_content(
    model=EMDEDDING_MODEL,
    contents=text
  )
  return result.embeddings

# embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
# def embeded_chunks(chunk)->list[float]:
#   embedding = embedding_model.encode(chunk)
#   return embedding.tolist()

# chunks = get_chunks()
# for c in chunks:
#   print(len(embeded_chunks(c)))
