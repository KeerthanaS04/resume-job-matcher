# Resume–Job Matcher

A smart Python-based application that compares a candidate’s resume with a job description and returns:
- Match Score (0–100)
- Skills Present
- Skills Missing
- Suggestions for improvement

This project uses the **Groq API** (Mixtral / LLaMA) for ultra-fast and accurate LLM-based comparison.

---

## Features

- Extracts and cleans text from resumes and job descriptions.
- Sends prompt to Groq’s LLaMA model (`llama-4-scout-17b-16e-instruct`) via API.
- Parses structured output into JSON.
- Identifies strengths, weaknesses, and improvement tips.
- Works with `.env` for secure API key management.

---

## Tech Stack

- Python 3.9+
- [Groq API](https://console.groq.com/)
- `requests`, `dotenv`, `re`
- FastAPI (optional for API usage)

---

## How to Use

### 1. Set Your API Key

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here

2. Install Dependencies
pip install -r requirements.txt
<details>
  <summary><code>
requests
python-dotenv
fastapi
uvicorn
</code></summary>
</details>

3. Run the Main Script
uvicorn main:app --reload

4. Folder Structure
resume_job_matcher/
├── main.py
├── llm_utils.py
├── .env
├── .env.example
├── requirements.txt
└── README.md

5. Todo / Improvements
- Add PDF resume text extraction
- Streamlit or Gradio UI
- Auto-upload and preview JSON results
