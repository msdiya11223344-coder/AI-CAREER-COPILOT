# AI Career Copilot

A full-stack Flask web application that analyzes a user's resume against their career goal using the Google Gemini API. It identifies existing skills, skill gaps, a personalized learning roadmap, likely interview questions, recommended certifications, platforms to apply on, and project ideas to strengthen the resume.

## Features

- **User Authentication** — Signup/login with password hashing (Werkzeug) and session-based auth
- **Resume Analysis** — Paste resume text or upload a file, along with a career goal
- **AI-Powered Insights** (Google Gemini API):
  - Skills already present
  - Missing skills for the target role
  - Recommended certifications
  - Step-by-step learning roadmap
  - Likely interview questions
  - Platforms to apply on (e.g. Wellfound, Internshala, LinkedIn)
  - Project ideas to add to the resume
- **Report History** — Save analysis reports and revisit them later
- **Cloud Database** — Persistent storage using TiDB (MySQL-compatible, serverless)

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLAlchemy ORM + TiDB Cloud (MySQL-compatible)
- **AI:** Google Gemini API (`google-generativeai`)
- **Frontend:** HTML, Jinja2 templates, CSS
- **Auth:** Werkzeug password hashing, Flask sessions

## Project Structure
AI_CAREER_COPILOT/
├── app.py # Flask routes (auth, dashboard, save, history)
├── ai.py # Gemini API integration and prompt logic
├── db.py # Database engine/session setup
├── models.py # SQLAlchemy models (User, Reports)
├── templates/ # Jinja2 HTML templates
│ ├── base.html
│ ├── login.html
│ ├── signup.html
│ ├── dashboard.html
│ └── history.html
├── static/
│ └── style.css
└── .env # Environment variables (not committed)


## Setup

1. Clone the repo:
```bash
   git clone https://github.com/msdiya11223344-coder/AI-CAREER-COPILOT.git
   cd AI-CAREER-COPILOT
```

2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
   pip install flask sqlalchemy pymysql google-generativeai python-dotenv werkzeug
```

4. Create a `.env` file in the project root:

GEMINI_API_KEY=your_gemini_api_key


5. Update `db.py` with your own database connection string (TiDB Cloud or any MySQL-compatible database).

6. Run the app:
```bash
   python app.py
```

7. Visit `http://127.0.0.1:5000/login` in your browser.

## Roadmap / Future Improvements

- PDF/DOCX resume parsing (currently plain text)
- Switch to the newer `google-genai` SDK (the `google-generativeai` package is deprecated)
- Deploy to a cloud platform (Render/Railway)
- Add unit tests

## Author

Diya — BTech CSE student, building toward an AI/Python Engineer role.
GitHub: [msdiya11223344-coder](https://github.com/msdiya11223344-coder)