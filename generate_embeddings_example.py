from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

# read the file
with open('./data/lessons/memorials.txt', 'r') as f:
    sentences = f.readlines()

query_embedding = model.encode('What is the Lord''s supper')
passage_embedding = model.encode(sentences)

scores = util.dot_score(query_embedding, passage_embedding)

sentence_scores = list(zip(sentences, scores[0].numpy()))
sentence_scores.sort(key=lambda x: x[1], reverse=True)

for line, score in sentence_scores[:5]:
    print(f"{line} -> {score}")