from sentence_transformers import SentenceTransformer, util

original_text = 'The cat jumped over the fence'
different_text = 'This is a great presentation'
similar_text = 'The cat jumped over the wall'

model = SentenceTransformer('all-MiniLM-L6-v2')
v = model.encode(original_text)
u = model.encode(different_text)
z = model.encode(similar_text)
sim = util.cos_sim(v, u)
dif = util.cos_sim(v, z)

print(f"{original_text} -> {v[0:5]}")
print(f"{different_text} -> {u[0:5]}")
print(f"Cosine similarity -> {sim.item()}")

print(f"{similar_text} -> {z[0:5]}")
print(f"Cosine similarity -> {dif.item()}")