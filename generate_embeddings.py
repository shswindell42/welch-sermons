import os
from sentence_transformers import SentenceTransformer
import pinecone

# read files from data/lessons
path = "./data/lessons"
files = os.listdir(path)

model = SentenceTransformer('all-MiniLM-L6-v2')


api_key = os.environ.get("PINECONE_API_KEY")
env = os.environ.get("PINECONE_ENV")
pinecone.init(api_key=api_key, environment=env)
pinecone_index = pinecone.Index("sermons")

for f in files:
    filepath = os.path.join(path, f)

    with open(filepath, 'r') as fp:
        lines = fp.readlines()

    # remove empty lines
    lines = [l.strip() for l in lines if l != ""]

    # split into 3 lines
    next = ""
    prev = ""
    document_embedding = []
    for i, l in enumerate(lines):
        prev = lines[i-1] if i - 1 >= 0 else ""
        next = lines[i+1] if i + 1 < len(lines) else ""

        text = " ".join([prev, l, next])
        meta = {
            "text": text,
            "file": f
        }
        key = f"{f}-{i}"

        # embed 
        embedding = model.encode(text)

        # build the object to send to pinecone
        document_embedding.append({
            "id": key,
            "values": embedding,
            "metadata": meta
        })

    # upsert to pinecone
    doc_length = len(document_embedding)
    print(f"Uploading {doc_length} vectors to pinecone")

    chunk_size = 100
    chunks = (doc_length // chunk_size) + 1
    for c in range(chunks):
        start = c * chunk_size
        end = min(start + chunk_size, doc_length) - 1

        chunk = document_embedding[start:end] if start != end else document_embedding[start]

        pinecone_index.upsert(chunk)
