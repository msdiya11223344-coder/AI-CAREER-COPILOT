from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

from db import engine, Base
from models import User, Reports
from ai import analyze_resume


app = Flask(__name__)

# Session secret key
app.secret_key = os.getenv("SECRET_KEY", "ai-career-copilot-secret")

# Create database tables
Base.metadata.create_all(engine)

# Database session
SessionLocal = sessionmaker(bind=engine)


# =========================
# HOME
# =========================

@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return redirect(url_for("dashboard"))


# =========================
# SIGNUP
# =========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        db = SessionLocal()

        try:

            existing_user = db.query(User).filter(
                User.email == email
            ).first()

            if existing_user:
                return render_template(
                    "signup.html",
                    error="Email already registered"
                )

            hashed_password = generate_password_hash(password)

            user = User(
                email=email,
                password=hashed_password
            )

            db.add(user)
            db.commit()

            return redirect(url_for("login"))

        finally:
            db.close()

    return render_template("signup.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        db = SessionLocal()

        try:

            user = db.query(User).filter(
                User.email == email
            ).first()

            if not user:
                return render_template(
                    "login.html",
                    error="Invalid email or password"
                )

            if not check_password_hash(user.password, password):
                return render_template(
                    "login.html",
                    error="Invalid email or password"
                )

            session["user_id"] = user.id
            session["email"] = user.email

            return redirect(url_for("dashboard"))

        finally:
            db.close()

    return render_template("login.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":

        resume_text = request.form.get("resume", "")
        user_goal = request.form.get("role", "")

        # File upload
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename:

            try:
                file_content = uploaded_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                resume_text = file_content

            except Exception:
                pass

        if not resume_text.strip():

            result = {
                "error": "Please enter your resume or upload a file."
            }

        elif not user_goal.strip():

            result = {
                "error": "Please enter your career goal."
            }

        else:

            result = analyze_resume(
                resume_text,
                user_goal
            )

            # Keep latest result in session
            session["last_result"] = result
            session["last_resume"] = resume_text
            session["last_goal"] = user_goal

    return render_template(
        "dashboard.html",
        user=session.get("email"),
        result=result
    )


# =========================
# SAVE DATA
# =========================

@app.route("/save", methods=["POST"])
def save_data():

    if "user_id" not in session:
        return redirect(url_for("login"))

    result = session.get("last_result")

    if not result:
        return redirect(url_for("dashboard"))

    db = SessionLocal()

    try:

        report = Reports(
            user_id=session["user_id"],
            resume_text=session.get("last_resume", ""),
            result=json.dumps(result)
        )

        db.add(report)
        db.commit()

    finally:
        db.close()

    return redirect(url_for("history"))


# =========================
# HISTORY
# =========================

@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = SessionLocal()

    try:

        reports = db.query(Reports).filter(
            Reports.user_id == session["user_id"]
        ).order_by(
            Reports.id.desc()
        ).all()

        history_data = []

        for report in reports:

            try:
                result = json.loads(report.result)
            except:
                result = {}

            history_data.append({
                "id": report.id,
                "resume": report.resume_text,
                "result": result
            })

        return render_template(
            "history.html",
            reports=history_data
        )

    finally:
        db.close()


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)