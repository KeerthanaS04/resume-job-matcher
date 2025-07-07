import os
import requests
import re
from dotenv import load_dotenv

# Load .env variables if present
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def clean_raw_output(raw_text: str) -> str:
    # Remove HuggingFace/Anthropic-style tokens and duplicates
    lines = raw_text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("<|") or "assistant" in line.lower():
            continue
        if line.count("*") > 10:  # malformed header lines
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def parse_llm_response(raw_text: str) -> dict:
    output = clean_raw_output(raw_text)
    parsed = {"raw": output}
    section = None

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue

        # Match Score (numeric only)
        if re.match(r"(#+\s*)?Match Score\s*:?\s*\d+", line, re.IGNORECASE):
            section = "Match Score"
            match = re.search(r'(\d+)', line)
            if match:
                parsed[section] = int(match.group(1))  # Convert to numeric
            else:
                parsed[section] = None
            section = None
            continue

        elif "Skills Present" in line:
            section = "Skills Present"
            parsed[section] = []

        elif "Skills Missing" in line:
            section = "Skills Missing"
            parsed[section] = []

        elif "Suggestions" in line:
            section = "Suggestions"
            parsed[section] = []

        elif "Additional Observations" in line:
            section = "Suggestions"
            continue

        elif section and section in parsed:
            if isinstance(parsed[section], list):
                cleaned_line = re.sub(r"^[-*•\d. ]+", "", line).strip()
                if cleaned_line:
                    parsed[section].append(cleaned_line)

    return parsed

def analyze_jd_resume(resume_text: str, jd_text: str) -> dict:
    if not GROQ_API_KEY:
        return {"error": "GROQ API key not set in environment."}

    resume_text = resume_text[:2000]
    jd_text = jd_text[:1500]

    prompt = (
        f"Compare the following resume and job description.\n\n"
        f"Resume:\n{resume_text}\n\n"
        f"Job Description:\n{jd_text}\n\n"
        f"Return this as Markdown:\n"
        f"- Match Score (0-100)\n"
        f"- Skills Present\n"
        f"- Skills Missing\n"
        f"- Suggestions"
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional job-matching assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        output = result["choices"][0]["message"]["content"]

        print("[DEBUG] Raw output:\n", output)  # optional debug

        return parse_llm_response(output)

    except requests.exceptions.RequestException as e:
        return {"error": str(e), "response": response.text}
