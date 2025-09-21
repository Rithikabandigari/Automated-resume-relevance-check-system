# scoring.py  (append)
def combine_scores(hard: float, soft: float, llm: float=None) -> dict:
    if llm is None:
        llm = 50.0
    # weights: hard 60%, soft 30%, llm 10%
    final = hard * 0.60 + soft * 0.30 + llm * 0.10
    final_rounded = int(round(final))
    verdict = "Low"
    if final_rounded >= 75:
        verdict = "High"
    elif final_rounded >= 50:
        verdict = "Medium"
    return {"hard": hard, "soft": soft, "llm": llm, "final_score": final_rounded, "verdict": verdict}
def compute_hard_score(must_have, good_to_have, resume_skills):
    score = 0
    matched_must = [s for s in must_have if s in resume_skills]
    matched_good = [s for s in good_to_have if s in resume_skills]
    score += len(matched_must) * 10
    score += len(matched_good) * 5
    return min(score, 100)

def compute_soft_score(jd_text, resume_text):
    from embeddings import embed_text, cosine_sim
    v1 = embed_text(jd_text)
    v2 = embed_text(resume_text)
    return (cosine_sim(v1, v2) + 1) / 2 * 100

def combine_scores(hard: float, soft: float, llm: float = None) -> dict:
    if llm is None:
        llm = 50.0
    final = hard * 0.60 + soft * 0.30 + llm * 0.10
    final_rounded = int(round(final))
    verdict = "Low"
    if final_rounded >= 75:
        verdict = "High"
    elif final_rounded >= 50:
        verdict = "Medium"
    return {
        "hard": hard,
        "soft": soft,
        "llm": llm,
        "final_score": final_rounded,
        "verdict": verdict
    }