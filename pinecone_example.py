import pinecone
import os
from sentence_transformers import SentenceTransformer

api_key = os.environ.get("PINECONE_API_KEY")
env = os.environ.get("PINECODE_ENV")
pinecone.init(api_key=api_key, environment=env)
index = pinecone.Index("sermons")

query = "What is the fruit of the spirit?"
model = SentenceTransformer('all-MiniLM-L6-v2')
query_vector = model.encode(query)

results = index.query(query_vector.tolist(), top_k=10, include_metadata=True)

print(results)