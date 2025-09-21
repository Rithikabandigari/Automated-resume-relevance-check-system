# parse_resume.py
import fitz          # PyMuPDF
import docx
import re
from typing import Dict, List

# === Skill List ===
DEFAULT_SKILL_LIST = [
    "python","sql","java","c++","c#","javascript","react","node","docker",
    "kubernetes","aws","gcp","azure","fastapi","flask","django","nlp",
    "tensorflow","pytorch","pandas","numpy","spark","hadoop","rest","graphql"
]

# === Text Extraction ===
def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    pages = []
    for p in doc:
        pages.append(p.get_text())
    return "\n".join(pages)

def extract_text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(paragraphs)

def extract_text(path: str) -> str:
    path = str(path)
    if path.lower().endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.lower().endswith(".docx"):
        return extract_text_from_docx(path)
    elif path.lower().endswith(".txt"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type: " + path)

# === Section Splitting ===
_SECTION_HEADERS = r"(education|experience|projects|skills|certifications|summary|objective|work experience|achievements|technical skills)"

def split_sections(text: str) -> Dict[str, str]:
    t = re.sub(r'\r', '', text)
    lines = t.splitlines()
    sections = {}
    current = "other"
    buffer = []
    for ln in lines:
        l = ln.strip()
        if not l:
            continue
        m = re.match(rf"^\s*({_SECTION_HEADERS})\b[:\-]?\s*$", l, re.I)
        if m:
            if buffer:
                sections[current] = "\n".join(buffer).strip()
            header = m.group(1).lower()
            current = header
            buffer = []
        else:
            buffer.append(l)
    if buffer:
        sections[current] = "\n".join(buffer).strip()
    return sections

# === Skill Extraction ===
def extract_skills_from_text(text: str, skill_list: List[str] = None) -> List[str]:
    if skill_list is None:
        skill_list = DEFAULT_SKILL_LIST
    found = set()
    text_low = text.lower()
    for s in skill_list:
        if re.search(rf"\b{re.escape(s.lower())}\b", text_low):
            found.add(s.lower())
    for part in re.split(r'[,;/\n]', text):
        p = part.strip().lower()
        if p and p in skill_list:
            found.add(p)
    return sorted(found)

# === Unified Resume Parser ===
def parse_resume(path: str) -> Dict[str, any]:
    txt = extract_text(path)
    sections = split_sections(txt)
    skills_text = sections.get("skills", "") + "\n" + sections.get("technical skills", "") + "\n" + txt
    skills = extract_skills_from_text(skills_text)
    return {
        "raw_text": txt,
        "sections": sections,
        "skills": skills
    }