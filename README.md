# Automated-resume-relevance-check-system
This project is my take on solving a real-world hiring challenge: figuring out how well a candidate’s resume matches a job description—without manually scanning through piles of documents. It’s a lightweight, fast, and modular system that scores resumes based on skills, semantic similarity, and even offers suggestions for improvement.
Whether you're a recruiter, a job seeker, or just curious about NLP-powered matching, this tool gives you instant, structured feedback.
Tech Stack
- Backend: Python + FastAPI
- Frontend: HTML + vanilla JavaScript
- Database: SQLAlchemy (SQLite or MySQL)
- NLP: Sentence-transformers, skill extraction, optional GPT-based suggestions
What It Can Do
- Upload and parse job descriptions and resumes
- Auto-fill evaluation fields for quick testing
- Score resumes based on:
- Hard skill match
-  Soft skill similarity
-  Optional LLM-based suggestions
- Return a final verdict with breakdowns and missing skills

🗂️ Project Structure
backend/
├── apps/
│   ├── main.py               - FastAPI app
│   ├── scoring.py            - Evaluation logic
│   ├── parse_resume.py       -Resume parsing
│   ├── parse_jd.py           - JD parsing
│   ├── db.py                 - SQLAlchemy models
│   ├── llm.py                - GPT-based suggestions (optional)
│   └── uploaded_files/       - Uploaded documents
frontend/
└── index.html                - Simple UI for testing

How to Run It
---Backend
cd backend/apps
uvicorn main:app --reload --port 8000


---Frontend
Just open index.html in your browser.
Or use Live Server in VS Code for auto-refresh.

 What’s Next
- Role-based access (admin vs candidate)
- Export results as PDF or CSV
- Score breakdown visualizations
- Resume rewriting suggestions via GPT
- React or Streamlit frontend upgrade
