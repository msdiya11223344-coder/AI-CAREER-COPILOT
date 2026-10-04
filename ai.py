import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.8-flash")

def analyze_resume(resume_text, career_goal):
    prompt = f"""
You are a career advisor AI. Analyze the resume below against the career goal.

Career Goal: {career_goal}

Resume:
{resume_text}

Return ONLY valid JSON, no extra text, no markdown, in exactly this structure:
{{
  "skills": ["skills the candidate already has"],
  "missing_skills": ["important skills missing for this goal"],
  "certifications": ["recommended certifications to add"],
  "roadmap": ["step by step learning roadmap, ordered"],
  "interview_questions": ["likely interview questions for this role"],
  "platforms_to_apply": ["job platforms relevant for this role, e.g. Wellfound, Internshala, LinkedIn"],
  "projects_to_add": ["specific project ideas that would strengthen this resume for this goal"]
}}
"""
    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # Gemini sometimes wraps JSON in ```json ... ``` - clean it
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        result = {
            "skills": [], "missing_skills": [], "certifications": [],
            "roadmap": [], "interview_questions": [],
            "platforms_to_apply": [], "projects_to_add": [],
            "error": "AI response could not be parsed. Try again."
        }
    return result