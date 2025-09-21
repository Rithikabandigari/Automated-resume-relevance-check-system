# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pathlib import Path
import uuid
from parse_resume import parse_resume, extract_text
from parse_jd import parse_jd_text
from scoring import compute_hard_score, compute_soft_score, combine_scores
from llm import get_llm_suggestions
from db import SessionLocal, init_db, JobDescription, Resume, Evaluation

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
init_db()
app = FastAPI(title="Resume Relevance MVP")

@app.post("/upload_jd")
async def upload_jd(file: UploadFile = File(...), title: str = Form(None)):
    ext = Path(file.filename).suffix
    fname = UPLOAD_DIR / f"jd_{uuid.uuid4().hex}{ext}"
    content = await file.read()
    fname.write_bytes(content)
    raw = extract_text(str(fname))
    parsed = parse_jd_text(raw)
    db = SessionLocal()
    jd = JobDescription(title=title or file.filename, raw_text=raw)
    db.add(jd); db.commit(); db.refresh(jd); db.close()
    return {"jd_id": jd.id, "must_have": parsed["must_have"], "good_to_have": parsed["good_to_have"]}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...), name: str = Form(None)):
    ext = Path(file.filename).suffix
    fname = UPLOAD_DIR / f"resume_{uuid.uuid4().hex}{ext}"
    content = await file.read()
    fname.write_bytes(content)
    parsed = parse_resume(str(fname))
    raw = parsed["raw_text"]
    db = SessionLocal()
    r = Resume(name=name or file.filename, raw_text=raw)
    db.add(r); db.commit(); db.refresh(r); db.close()
    return {"resume_id": r.id, "skills": parsed["skills"]}

@app.post("/evaluate")
async def evaluate(jd_id: int = Form(...), resume_id: int = Form(...)):
    db = SessionLocal()
    jd = db.query(JobDescription).filter(JobDescription.id==jd_id).first()
    res = db.query(Resume).filter(Resume.id==resume_id).first()
    if not jd or not res:
        db.close()
        raise HTTPException(status_code=404, detail="JD or Resume not found")
    jd_parsed = parse_jd_text(jd.raw_text)
    from parse_resume import split_sections, extract_skills_from_text
    resume_skills = extract_skills_from_text(res.raw_text)
    hard = compute_hard_score(jd_parsed["must_have"], jd_parsed["good_to_have"], resume_skills)
    soft = compute_soft_score(jd.raw_text, res.raw_text)
    llm_resp = get_llm_suggestions(jd.raw_text, res.raw_text)
    llm_score = llm_resp.get("score", 50)
    suggestions = llm_resp.get("suggestions", [])
    combined = combine_scores(hard, soft, llm_score)
    missing = [s for s in jd_parsed["must_have"] if s not in resume_skills]
    ev = Evaluation(jd_id=jd.id, resume_id=res.id, hard=hard, soft=soft, llm=llm_score,
                    final_score=combined["final_score"], verdict=combined["verdict"])
    db.add(ev); db.commit(); db.refresh(ev); db.close()
    return {"hard": hard, "soft": soft, "llm": llm_score,
            "final_score": combined["final_score"], "verdict": combined["verdict"],
            "missing": missing, "suggestions": suggestions}
