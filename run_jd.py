from parse_resume import extract_text  # Reuse your PDF/text extractor
from parse_jd import parse_jd_text     # Your improved JD parser
jd_text = extract_text("../../sample_jd_1.pdf")  # Adjust path if needed
print("==== RAW TEXT ====")
print(jd_text)
parsed_jd = parse_jd_text(jd_text)
print("\n==== PARSED JD ====")
print(parsed_jd)