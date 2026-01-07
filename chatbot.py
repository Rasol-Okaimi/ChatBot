import os
import re  # Added for regex splitting to handle compound questions
import csv
import sys
import json
import random
import subprocess
import logging
from datetime import datetime
from trivia_game import play_trivia
from weather_app import get_current_weather, get_forecast_weather


# Handle task number 22
HELP_TEXT = """
CHATBOT APPLICATION - HELP

Syntax:
  python chatbot.py [OPTIONS]

Options:
  --help
      Show this help message and exit

  --log
      Enable file-based logging (disabled by default)

  --log-level LEVEL
      Set logging level: INFO or WARNING
      Default: WARNING

  --debug
      Enable debug mode

  --question "TEXT"
      Ask a single question via CLI and exit

  --import
      Import questions from a file (use with --filetype and --filepath)

  --filetype CSV
      Specify import file type

  --filepath PATH
      Path to the import file

  --add --question "Q" --answer "A"
      Add a new question and answer

  --remove --question "Q" [--answer "A"]
      Remove a question or a specific answer

  --list
      List all stored questions

  --test
      Run unit tests and exit

Examples:
  python chatbot.py --help
  python chatbot.py --log --log-level INFO
  python chatbot.py --question "what is python"
  python chatbot.py --import --filetype CSV --filepath questions.csv
"""


def print_help_and_exit():
    print(HELP_TEXT)
    sys.exit(0)


def error_and_help(message):
    print(f"ERROR: {message}\n")
    print(HELP_TEXT)
    sys.exit(1)


if "--help" in sys.argv:
    print_help_and_exit()

KNOWN_ARGS = {
    "--help", "--log", "--log-level", "--debug",
    "--question", "--import", "--filetype", "--filepath",
    "--add", "--answer", "--remove", "--list", "--test"
}

for arg in sys.argv[1:]:
    if arg.startswith("--") and arg not in KNOWN_ARGS:
        error_and_help(f"Unknown command line argument: {arg}")

##Handle task number 21
LOG_ENABLED = "--log" in sys.argv
LOG_LEVEL = "WARNING"

if "--log-level" in sys.argv:
    try:
        LOG_LEVEL = sys.argv[sys.argv.index("--log-level") + 1].upper()
    except IndexError:
        LOG_LEVEL = "WARNING"

if LOG_ENABLED:
    logging.basicConfig(
        filename="chatbot.log",
        filemode="a",
        level=logging.INFO if LOG_LEVEL == "INFO" else logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logging.info("Logging enabled")
else:
    logging.disable(logging.CRITICAL)

DEBUG_MODE = "--debug" in sys.argv

def get_time():
    return datetime.now().strftime("%H:%M:%S")


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

## keyword_suggestions Handles (#12)
keyword_suggestions = {
    "python": [
        "what is python",
        "what can you do with python",
    ],
    "president": [
        "who is the president of the usa",
        "who is the president of America",
    ],
    "planet": [
        "what is the largest planet",
    ],
    "mountain": [
        "what is the tallest mountain",
    ],
}

# Handles (#14) Handle multiple variations of the same question
question_variants = {
    "what is python programing": "what is python",
    "can you describe python programming": "what is python",
    "what do you mean by python programming": "what is python",
    "what is the meaning of python programming": "what is python",
    "what is python language": "what is python",
}

last_suggestions = []


def chatbot_response(user_input):
    logging.info(f"User asked: {user_input}")

    user_input = user_input.lower().strip()
    
    # Handles(25) 🌦 Weather handling
    location, event_date = extract_location_and_date(user_input)

    if location:
        try:
            if event_date:
                weather = get_forecast_weather(location, event_date)
            else:
                weather = get_current_weather(location)

            return f"Chatbot: {weather} What else would you like to know?"
        except Exception:
            return "Chatbot: I found the location, but could not get the weather right now."


    # Handles (#13) Compound questions
    split_pattern = r'\s*(?:and|or|also|as well as|and also|or also)\s*|[?,;]+\s*'
    parts = re.split(split_pattern, user_input)

    found_answers = []

    for part in parts:
        clean_part = part.strip().replace('?', '')

        if not clean_part:
            continue  # Skip empty

        # Handles (#14)
        if clean_part in question_variants:
            clean_part = question_variants[clean_part]

        if clean_part in chat_questions:
            answer = random.choice(chat_questions[clean_part])
            found_answers.append(answer)
            logging.info(f"Answer found for: {part}")
        else:
            logging.warning(f"Unknown question: {part}")

    if len(found_answers) > 0:
        if len(found_answers) == 1:
            return f"Chatbot: {found_answers[0]} What else would you like to know?"
        else:
            combined_response = " Also, ".join(found_answers)
            return f"Chatbot: {combined_response} What else would you like to know?"
    else:
        return "Chatbot: Sorry, I don't recognize that question (or combination of questions). Please ask another question."


def suggest_questions(keyword):  ## Handles (#12)
    keyword = keyword.lower()
    if keyword in keyword_suggestions:
        return keyword_suggestions[keyword]
    return None

# Hanldle (#25) Weather forecast integration
def extract_location_and_date(user_input):
    """
    Extract location and date from user input.
    Returns (location, date)
    """
    # Simple date pattern: YYYY-MM-DD
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", user_input)
    event_date = date_match.group() if date_match else None

    # Very simple location list (can be extended)
    known_locations = ["goslar", "wolfenbüttel", "braunschweig", "berlin"]

    location = None
    for city in known_locations:
        if city in user_input.lower():
            location = city.title()
            break

    return location, event_date

# ===============================
# CLI QUESTION HANDLER (REQUIRED)
# ===============================

if "--question" in sys.argv:
    try:
        question_index = sys.argv.index("--question") + 1
        user_question = sys.argv[question_index]
    except IndexError:
        error_and_help("Missing text after --question")

    response = chatbot_response(user_question)
    print(response)
    sys.exit(0)