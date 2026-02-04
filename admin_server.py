from flask import Flask, render_template, request, redirect, url_for, flash
import os
import logging
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DATA_DIR = "data"
QUESTIONS_FILE = os.path.join(DATA_DIR, "chat_questions.json")
USERS_FILE = os.path.join("data", "user.json")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)  # dict: {question: [answers]}
            except json.JSONDecodeError:
                return {}
    return {}

def save_questions(questions):
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)

@app.route("/list-qa")
def list_qa():
    q_dict = load_questions()
    search_query = request.args.get("q", "").lower().strip()
    filtered = {}

    if search_query:
        for q, answers in q_dict.items():
            if search_query in q.lower() or any(search_query in ans.lower() for ans in answers):
                filtered[q] = answers
    else:
        filtered = q_dict

    # Convert dict to list of dicts for template compatibility
    qa_list = [{"question": q, "answer": answers} for q, answers in filtered.items()]
    return render_template("list_qa.html", qa_list=qa_list, search_query=search_query)


@app.route("/logs")
def logs():
    try:
        with open(LOG_FILE, "r") as f:
            log_lines = f.readlines()
    except FileNotFoundError:
        log_lines = ["No logs found"]
    return render_template("logs.html", logs=log_lines)

@app.route("/clear-logs")
def clear_logs():
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
        flash("Log file cleared successfully!", "success")
    else:
        flash("Log file does not exist.", "error")
    return redirect(url_for("logs"))


@app.route("/users")
def users():
    users_list = load_users()
    return render_template("list_users.html", users=users_list)

@app.route("/edit-qa", methods=["GET", "POST"])
def edit_qa():
    questions = load_questions()

    if request.method == "POST":
        action = request.form.get("action")
        question = request.form.get("question", "").strip()
        answer = request.form.get("answer", "").strip()

        if action == "add":
            if question and answer:
                if question in questions:
                    if answer not in questions[question]:
                        questions[question].append(answer)
                        flash(f"Added new answer to existing question.", "success")
                    else:
                        flash("This answer already exists for the question.", "error")
                else:
                    questions[question] = [answer]
                    flash("Added new question and answer.", "success")
                save_questions(questions)
            else:
                flash("Please provide both question and answer to add.", "error")

        elif action == "delete_question":
            if question in questions:
                del questions[question]
                save_questions(questions)
                flash(f"Deleted question '{question}' and its answers.", "success")
            else:
                flash("Question not found.", "error")

        elif action == "delete_answer":
            if question in questions:
                if answer in questions[question]:
                    questions[question].remove(answer)
                    if not questions[question]:  # when no answer delete question
                        del questions[question]
                    save_questions(questions)
                    flash("Answer deleted successfully.", "success")
                else:
                    flash("Answer not found for the given question.", "error")
            else:
                flash("Question not found.", "error")

        return redirect(url_for("edit_qa"))

    # Prepare data for display
    qa_list = [{"question": q, "answer": answers} for q, answers in questions.items()]
    return render_template("edit_qa.html", qa_list=qa_list)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
