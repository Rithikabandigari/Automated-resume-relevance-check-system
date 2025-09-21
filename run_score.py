from parse_resume import parse_resume
from parse_resume import extract_text
from parse_jd import parse_jd_text
from score_match import score_resume_to_jd

resume = parse_resume("../../resume-1.pdf")
jd_text = extract_text("../../sample_jd_1.pdf")
jd = parse_jd_text(jd_text)

score = score_resume_to_jd(resume["skills"], jd)
print("==== SCORE ====")
print(score)