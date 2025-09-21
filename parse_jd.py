import re
from typing import List, Dict

COMMON_SKILLS = [
    "python","sql","java","c++","javascript","react","node","docker","kubernetes",
    "aws","gcp","azure","fastapi","flask","django","nlp","tensorflow","pytorch",
    "pandas","numpy","spark","hadoop","excel","r","machine learning","data science"
]

def parse_jd_text(text: str, skills_master_list: List[str] = None) -> Dict:
    if skills_master_list is None:
        skills_master_list = COMMON_SKILLS

    t = text.lower()
    must_have = []
    good_to_have = []

    for line in t.splitlines():
        line = line.strip()
        if not line:
            continue
        for s in skills_master_list:
            if re.search(rf"\b{s}\b", line):
                if any(k in line for k in [
                    "must", "required", "minimum", "requires",
                    "experience in", "proficient in", "should have", "need"
                ]):
                    must_have.append(s)
                elif any(k in line for k in [
                    "nice to have", "preferred", "good to have", "desirable",
                    "preferred skills", "bonus"
                ]):
                    good_to_have.append(s)
                else:
                    good_to_have.append(s)  # fallback if no keyword

    # Final fallback: scan entire text if nothing found
    if not must_have and not good_to_have:
        for s in skills_master_list:
            if re.search(rf"\b{s}\b", t):
                good_to_have.append(s)

    return {
        "raw_text": text,
        "must_have": sorted(set(must_have)),
        "good_to_have": sorted(set(good_to_have))
    }