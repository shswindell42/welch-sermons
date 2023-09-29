import os
from sentence_transformers import SentenceTransformer
import pinecone
import requests
import urllib.parse

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


def query_solr(query):
    # format the request
    url_query = urllib.parse.quote_plus(f"content:{query}")
    url = f"http://localhost:8983/solr/sermons/select?q={url_query}"

    results = requests.get(url=url)

    if results.status_code == 200:
        docs = results.json()["response"]["docs"]
    else:
        docs = [{"title": "", "content": results.text}]

    return [
        {
            "title": d["title"],
            "meta": d["content"][0:100]
        }
        for d in docs
    ]