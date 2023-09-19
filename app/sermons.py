import os
from sentence_transformers import SentenceTransformer
import pinecone

path = "data/lessons"

_model = SentenceTransformer("all-MiniLM-L6-v2")

_api_key = os.environ.get("PINECONE_API_KEY")
_env = os.environ.get("PINECODE_ENV")
pinecone.init(api_key=_api_key, environment=_env)
search_index = pinecone.Index("sermons")

def get_sermon(title):
    file_path = f"{path}/{title}"
    with open(file_path, 'r') as fp:
        content = fp.read()

    return {
        "title": title,
        "content": content
    }

def query(query):
    # need to encode the query
    query_vector = _model.encode(query)
    results = search_index.query(query_vector.tolist(), top_k=10, include_metadata=True)

    return [
        {
            "title": m["metadata"]["file"],
            "meta": m["metadata"]["text"]
        }
        for m in results["matches"]
    ]