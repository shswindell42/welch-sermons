import pinecone
import os

api_key = os.environ.get("PINECONE_API_KEY")
env = os.environ.get("PINECODE_ENV")
pinecone.init(api_key=api_key, environment=env)
print(pinecone.list_indexes())