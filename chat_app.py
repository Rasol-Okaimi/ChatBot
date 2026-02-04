from flask import Flask, render_template, request, jsonify, session, send_from_directory
from chatbot import chatbot_response, save_chat_log, suggest_questions
import random
import json
from utils import get_time
import logging
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("chat.html")

tips = [
    "Tip: Type 'question' to chat with me.",
    "Tip: Type 'Keyword' to ask me a question.",
    "Tip: Type 'location' to ask me about weather ex:Berlin.",
    "Tip: You can ask multiple questions like: 'what is python and what is the largest planet?'",
    "Tip: Type 'bye' to exit."
]

DATA_DIR = "data"
QUESTIONS_FILE = os.path.join(DATA_DIR, "chat_questions.json")

def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)  # dict: {question: [answers]}
            except json.JSONDecodeError:
                return {}
    else:
        return {}

@app.route("/get_suggestions")
def get_suggestions():
    questions_dict = load_questions()
    all_questions = list(questions_dict.keys())
    random_questions = random.sample(all_questions, min(3, len(all_questions))) if all_questions else []
    return jsonify({
        "tips": tips,
        "questions": random_questions
    })

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.form.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please type a message."})

    if "chat_log" not in session:
        session["chat_log"] = []

    if "last_suggestions" not in session:
        session["last_suggestions"] = []

    session["chat_log"].append(f"You: {user_message}")

    try:
        lower_msg = user_message.lower()

        if lower_msg in ["bye", "exit", "quit"]:
            response_text = "Goodbye! Have a great day!"
            session["chat_log"].append(response_text)
            session.pop("chat_log", None)
            session.pop("last_suggestions", None)
            full_response = f"{get_time()} {response_text}"
            return jsonify({"response": full_response})

        # save log
        if lower_msg in ["save log", "download", "save"]:
            if session["chat_log"]:
                path = save_chat_log(session["chat_log"], directory=LOG_DIR)
                filename = os.path.basename(path)
                response_text = f"Chat log saved to: {filename}"
            else:
                response_text = "No chat log to save."
            session["chat_log"].append(response_text)
            full_response = f"{get_time()} {response_text}"
            return jsonify({"response": full_response})

        if user_message.isdigit() and session["last_suggestions"]:
            choice = int(user_message)
            if 1 <= choice <= len(session["last_suggestions"]):
                selected_question = session["last_suggestions"][choice - 1]
                response_text = chatbot_response(selected_question)
                session["chat_log"].append(response_text)
                # clear suggestions
                session["last_suggestions"] = []
                full_response = f"{get_time()} {response_text}"
                return jsonify({"response": full_response})
            else:
                response_text = f"Invalid choice. Please enter a number between 1 and {len(session['last_suggestions'])}."
                full_response = f"{get_time()} {response_text}"
                return jsonify({"response": full_response})


        response_text = chatbot_response(user_message)
        session["chat_log"].append(response_text)

        suggestions = suggest_questions(user_message)
        if suggestions:
            session["last_suggestions"] = suggestions
            suggestion_text = "You might want to ask:\n" + "\n".join(f"{i+1}. {q}" for i, q in enumerate(suggestions))
            response_text += "\n" + suggestion_text
            session["chat_log"].append(suggestion_text)
        else:
            session["last_suggestions"] = []

        full_response = f"{get_time()} {response_text}"
        return jsonify({"response": full_response})

    except Exception as e:
        logging.exception("Error in send_message")
        response_text = "An internal error occurred."
        full_response = f"{get_time()} {response_text}"
        return jsonify({"response": full_response})

@app.route("/download_log")
def download_log():
    filename = request.args.get("path", "")
    if not filename or ".." in filename or "/" in filename:
        return "Invalid filename", 400
    try:
        return send_from_directory(LOG_DIR, filename, as_attachment=True)
    except Exception as e:
        return "File not found", 404

def save_chat_log(chat_log, directory="chat_logs"):
    if not chat_log:
        return None

    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chat_log_{timestamp}.txt"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write("\n".join(chat_log))

    return filepath

if __name__ == "__main__":
    app.run(debug=True, port=5000)