from sentence_transformers import SentenceTransformer, util

v_text = 'The cat jumped over the fence'
u_text = 'This is a great presentation'

model = SentenceTransformer('all-MiniLM-L6-v2')
v = model.encode(v_text)
u = model.encode(u_text)
sim = util.cos_sim(v, u)

print(f"{v_text} -> {v[0:5]}")
print(f"{u_text} -> {u[0:5]}")
print(f"Cosine similarity -> {sim.item()}")