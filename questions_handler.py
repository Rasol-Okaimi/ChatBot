import os
import csv
import sys
import json
import logging
from utils import get_time

# Handles (#10)
chat_questions = {
    # Added greetings to handle "Hi, what is python?" scenarios
    "hi": [
        "Hello!",
        "Hi there!",
        "Greetings!",
    ],
    "hello": [
        "Hello!",
        "Hi there!",
    ],

    "what is your name": [
        "I am Chatbot Group 7.",
        "You can call me Chatbot Group 7.",
        "I'm known as Chatbot Group 7.",
    ],

    "how are you": [
        "I'm doing great, thank you!",
        "Feeling awesome today!",
        "I'm good! Thanks for asking.",
    ],

    "what is python": [
        "Python is a powerful and easy-to-learn programming language.",
        "Python is a great programming language to learn.",
        "Python is a popular programming language used for many types of software development.",
    ],

    "what is the capital of france": [
        "The capital of France is Paris.",
        "Paris is the capital city of France.",
        "France’s capital is Paris.",
    ],

    "what is the capital of germany": [
        "The capital of Germany is Berlin.",
        "Berlin is the capital city of Germany.",
        "Germany’s capital is Berlin.",
    ],

    "who created you": [
        "I was created by a developer using Python.",
        "I was developed using Python!",
        "A Python developer brought me to life!",
    ],

    "what can you do with python": [
        "I can answer basic questions and chat with you!",
        "I am here to help you!",
        "I’m able to respond to simple questions and keep you company!",
    ],

    "what is 2 plus 2": [
        "2 plus 2 equals 4.",
        "4 is the answer.",
        "The answer is 4.",
    ],

    "what is the largest planet": [
        "Jupiter is the largest planet in our solar system.",
        "The largest planet is Jupiter.",
        "The biggest planet in our solar system is Jupiter.",
    ],

    "who is the president of the usa": [
        "As of 2025, the President of the USA is Donald Trump.",
        "The President of the USA is Donald Trump.",
        "Donald Trump is the current President of the United States (2025).",
    ],

    "who is the president of america": [
        "As of 2025, the President of the USA is Donald Trump.",
        "The President of the USA is Donald Trump.",
    ],

    "what is the tallest mountain": [
        "Mount Everest is the tallest mountain in the world.",
        "Everest is the tallest mountain in the world.",
        "Everest is the highest mountain above sea level.",
    ],
}

def load_questions_from_file(filepath="data/chat_questions.json"):

    global chat_questions
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            chat_questions = json.load(f)
        #print(f"{get_time()} Chatbot: Loaded questions from {filepath}")
    except FileNotFoundError:
        print(f"{get_time()} Chatbot: No saved questions file found, starting fresh.")
        chat_questions = {}
    except json.JSONDecodeError:
        print(f"{get_time()} Chatbot: Error: JSON file is corrupted.")
        chat_questions = {}

def import_csv(filepath):
    #from chatbot import interactive_chat
    logging.info(f"Attempting CSV import: {filepath}")
    global chat_questions
    print(f"{get_time()} Chatbot: Starting CSV import...")

    if not os.path.exists(filepath):
        logging.warning("CSV file path invalid")
        print(f"{get_time()} WARNING: Invalid file path: {filepath}")
        sys.exit(1)

    if not filepath.lower().endswith(".csv"):
        print(f"{get_time()} WARNING: Unsupported file type. Only CSV allowed.")
        sys.exit(1)

    try:
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required = ["question", "answer1", "answer2", "answer3", "answer4"]
            for field in required:
                if field not in reader.fieldnames:
                    print(f"{get_time()} WARNING: Missing required CSV column: {field}")
                    sys.exit(1)

            new_data = {}

            for row in reader:
                question = row["question"].strip().lower()
                answers = [row.get(f"answer{i}", "").strip() for i in range(1, 5)]
                answers = [a for a in answers if a]
                if not answers:
                    print(f"{get_time()} WARNING: No answers for question: {question}")
                    continue
                new_data[question] = answers

        chat_questions = new_data
        logging.info("CSV import successful")
        print(f"{get_time()} Chatbot: CSV imported successfully! {len(chat_questions)} questions loaded.")
        save_questions_to_file()
        #interactive_chat()

    except PermissionError:
        print(f"{get_time()} WARNING: Permission denied for file: {filepath}")
        sys.exit(1)
    except csv.Error:
        print(f"{get_time()} WARNING: CSV file is corrupted.")
        sys.exit(1)
    except Exception as e:
        logging.warning(f"CSV import failed: {e}")
        print(f"{get_time()} WARNING: Unexpected CSV import error: {e}")
        sys.exit(1)

def print_full_list():
    print(f"{get_time()} Chatbot: Updated full questions and answers list:")
    for i, (q, answers) in enumerate(chat_questions.items(), 1):
        print(f"  {i}. Question: {q}")
        for j, ans in enumerate(answers, 1):
            print(f"     Answer {j}: {ans}")

def save_questions_to_file(filepath="data/chat_questions.json"):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(chat_questions, f, ensure_ascii=False, indent=4)
        print(f"{get_time()} Chatbot: Saved questions to {filepath}")
    except Exception as e:
        print(f"{get_time()} Chatbot: Error saving questions: {e}")

def add_question(question, answer):
    question = question.lower().strip()
    if question in chat_questions:
        if answer in chat_questions[question]:
            print(f"{get_time()} Chatbot: The answer already exists for the question: {question}")
        else:
            chat_questions[question].append(answer)
            print(f"{get_time()} Chatbot: Added new answer to existing question: {question}")
    else:
        chat_questions[question] = [answer]
        print(f"{get_time()} Chatbot: Added new question with answer.")

    print_full_list()
    save_questions_to_file()

def remove_question(question):
    question = question.lower().strip()
    if question in chat_questions:
        del chat_questions[question]
        print(f"{get_time()} Chatbot: Removed question: {question}")

        print_full_list()
        save_questions_to_file()

    else:
        print(f"{get_time()} Chatbot: Question not found.")

def remove_answer(question, answer):
    question = question.lower().strip()
    if question not in chat_questions:
        print(f"{get_time()} Chatbot: Question not found.")
        return

    if answer not in chat_questions[question]:
        print(f"{get_time()} Chatbot: Answer not found for this question.")
        return

    chat_questions[question].remove(answer)
    print(f"{get_time()} Chatbot: Removed answer from question: {question}")

    print_full_list()
    save_questions_to_file()

def list_all_questions():
    print(f"{get_time()} Chatbot: Listing all stored questions:")
    for i, q in enumerate(chat_questions.keys(), 1):
        print(f"  {i}. {q}")
    print(f"{get_time()} Chatbot: Total questions: {len(chat_questions)}")

# Call the loader function to load saved questions at module load time or call explicitly later
load_questions_from_file()
