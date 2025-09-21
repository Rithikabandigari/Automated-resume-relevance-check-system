from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL = None

def get_model(name="all-MiniLM-L6-v2"):
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(name)
    return _MODEL

def embed_text(text: str):
    model = get_model()
    vec = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return vec

def cosine_sim(a, b):
    if a is None or b is None:
        return 0.0
    return float(np.dot(a, b))
