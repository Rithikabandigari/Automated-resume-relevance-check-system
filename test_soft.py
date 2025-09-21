from embeddings import embed_text, cosine_sim
jd_text = "Required: Python, FastAPI, SQL. Preferred: Docker, AWS."
resume_text = "Worked on FastAPI REST services in Python, used SQL and Docker."
v1 = embed_text(jd_text)
v2 = embed_text(resume_text)
sim = cosine_sim(v1, v2)  # since normalized dot product returns cosine in [-1,1]
scaled = (sim + 1) / 2 * 100
print("cosine:", sim, "soft_score_0_100:", round(scaled,2))
