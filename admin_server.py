from flask import Flask, render_template, request, redirect, url_for,flash
import logging
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

management_features = [
    {"name": "List Questions/Answers", "link": "/list-qa"},
    {"name": "Edit Questions/Answers", "link": "/edit-qa"},
    {"name": "App Logs", "link": "/logs"},
    {"name": "List Users", "link": "/users"},
    {"name": "User Activity", "link": "/activity"}
]

sample_qa = [
    {"question": "What is Python?", "answer": "A programming language"},
    {"question": "What is a chatbot?", "answer": "A program that talks to users"},
    {"question": "what is the largest planet?", "answer": "Jupiter is the largest planet"},
    {"question": "what is AI?", "answer": "AI means Artificial Intelligence."}
]

sample_users = [
    {"username": "alice", "email": "alice@example.com", "activity": "Active"},
    {"username": "bob", "email": "bob@example.com", "activity": "Inactive"}
]


@app.route("/")
def dashboard():
    return render_template("dashboard.html", features=management_features)

@app.route("/list-qa")
def list_qa():
    return render_template("list_qa.html", qa_list=sample_qa)

@app.route("/edit-qa", methods=["GET", "POST"])
def edit_qa():
    if request.method == "POST":
        new_question = request.form.get("question")
        new_answer = request.form.get("answer")

        if new_question and new_answer:
            sample_qa.append({
                "question": new_question,
                "answer": new_answer
            })

        return redirect(url_for("edit_qa"))

    return render_template("edit_qa.html", qa_list=sample_qa)

@app.route("/logs")
def logs():
    try:
        with open("app.log", "r") as file:
            log_lines = file.readlines()
    except FileNotFoundError:
        log_lines = ["No logs found"]

    return render_template("logs.html", logs=log_lines)

@app.route("/clear-logs")
def clear_logs():
    if os.path.exists("app.log"):
        open("app.log", "w").close()  
        flash("Log file cleared successfully!", "success")
    else:
        flash("Log file does not exist.", "error")
    return redirect(url_for("logs"))

@app.route("/users")
def users():
    return render_template("list_users.html", users=sample_users)

@app.route("/activity")
def activity():
    return render_template("user_activity.html", users=sample_users)

if __name__ == "__main__":
    app.run(debug=True)