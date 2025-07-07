from fastapi import FastAPI, UploadFile, File, Form
import sqlite3
from resume_parser import parse_resume
from llm_utils import analyze_jd_resume
import tempfile
import os
import json

app = FastAPI()
conn = sqlite3.connect("models.db", check_same_thread=False)
conn.execute("""
CREATE TABLE IF NOT EXISTS results(
 id INTEGER PRIMARY KEY,
 resume TEXT,
 jd TEXT,
 score TEXT,
 skills_have TEXT,
 skills_missing TEXT,
 suggestions TEXT
)
""")

@app.post("/analyze/")
async def analyze(resume: UploadFile = File(...), jd_text: str = Form(...)):
    temp_dir = tempfile.gettempdir()  # Cross-platform tmp directory
    file_path = os.path.join(temp_dir, resume.filename)

    with open(file_path, "wb") as f:
        f.write(await resume.read())

    resume_text, skills = parse_resume(file_path)
    llm_out = analyze_jd_resume(resume_text, jd_text)
    print(json.dumps(llm_out, indent=2))

    # store to db (optional)

    return llm_out

@app.get("/")
def home():
    return {"msg": "POST to /analyze with form data: resume file + jd_text"}
