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


def interactive_chat():
    print(f"{get_time()} Chatbot: Hello!")
    print(f"{get_time()} Chatbot: How can I help you?")

    global last_suggestions

    while True:
        try:
            user_input = input(f"{get_time()} You: ").strip()
        except EOFError:
            break

        if not user_input:
            continue

        if user_input.lower() in ["bye", "exit", "quit"]:
            logging.info("User exited application")
            print(f"{get_time()} Chatbot: Goodbye! Have a great day!")
            break

        if user_input.lower() == "trivia":
            play_trivia()
            continue

        if user_input.isdigit() and last_suggestions:
            choice = int(user_input)
            if 1 <= choice <= len(last_suggestions):
                selected_question = last_suggestions[choice - 1]
                response = chatbot_response(selected_question)
                print(f"{get_time()} {response}")
                last_suggestions = []
                continue
            else:
                print(f"{get_time()} Chatbot: Invalid question number. Please try again.")
                continue

        suggestions = suggest_questions(user_input)
        if suggestions:
            last_suggestions = suggestions
            print(f"{get_time()} Chatbot: You might want to ask:")
            for i, q in enumerate(suggestions, 1):
                print(f"  {i}. {q}")
            print(f"{get_time()} Chatbot: Please type the number of your question choice.")
            continue

        last_suggestions = []

        response = chatbot_response(user_input)
        print(f"{get_time()} {response}")


def cli_mode(question):
    response = chatbot_response(question)
    print(f"{get_time()} {response}")


# Handles (#15) Import CSV file
def import_csv(filepath):
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
            # REQUIRED CSV COLUMNS
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


# Handles (#17 + 18) Add and Remove questions

def print_full_list():
    print(f"{get_time()} Chatbot: Updated full questions and answers list:")
    for i, (q, answers) in enumerate(chat_questions.items(), 1):
        print(f"  {i}. Question: {q}")
        for j, ans in enumerate(answers, 1):
            print(f"     Answer {j}: {ans}")


def save_questions_to_file(filepath="chat_questions.json"):
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


# Handles (#16) List all internal questions
def list_all_questions():
    print(f"{get_time()} Chatbot: Listing all stored questions:")
    for i, q in enumerate(chat_questions.keys(), 1):
        print(f"  {i}. {q}")
    print(f"{get_time()} Chatbot: Total questions: {len(chat_questions)}")


if __name__ == "__main__":

    # (20)Run built-in self-tests using --test
    if "--test" in sys.argv:
        if DEBUG_MODE:
            print(f"{get_time()} DEBUG: Running tests with debug mode enabled...")
        else:
            print("Running unit tests...")

        subprocess.run([sys.executable, "test_chatbot.py"])
        sys.exit(0)

    # Import mode (15)
    if "--import" in sys.argv:
        try:
            filetype = sys.argv[sys.argv.index("--filetype") + 1]
            filepath = sys.argv[sys.argv.index("--filepath") + 1]

            if filetype.upper() == "CSV":
                import_csv(filepath)
            else:
                print(f"{get_time()} Chatbot: Unsupported file type. Only CSV is allowed.")
                sys.exit(1)

        except Exception as e:
            print(f"{get_time()} Chatbot: Error during import:", e)
            sys.exit(1)

    # Handles (#17 + 18) Add and Remove questions
    if "--add" in sys.argv:
        if "--question" in sys.argv and "--answer" in sys.argv:
            question = sys.argv[sys.argv.index("--question") + 1]
            answer = sys.argv[sys.argv.index("--answer") + 1]
            add_question(question, answer)
            sys.exit(0)
        else:
            print(f"{get_time()} Chatbot: Usage: --add --question \"Q\" --answer \"A\"")
            sys.exit(1)

    # Remove Question or Answer
    if "--remove" in sys.argv:
        if "--question" in sys.argv and "--answer" in sys.argv:
            question = sys.argv[sys.argv.index("--question") + 1]
            answer = sys.argv[sys.argv.index("--answer") + 1]
            remove_answer(question, answer)
            sys.exit(0)

        elif "--question" in sys.argv:
            question = sys.argv[sys.argv.index("--question") + 1]
            remove_question(question)
            sys.exit(0)

        else:
            print(f"{get_time()} Chatbot: Usage: --remove --question \"Q\" [--answer \"A\"]")
            sys.exit(1)

    # Handles (#16) List mode
    if "--list" in sys.argv:
        list_all_questions()
        sys.exit(0)

    # CLI question mode
    if len(sys.argv) > 2 and "--question" in sys.argv:
        question_arg = " ".join(sys.argv[sys.argv.index("--question") + 1:])
        cli_mode(question_arg)
        sys.exit(0)

    if len(sys.argv) > 2 and sys.argv[1] == "--question":
        question_arg = " ".join(sys.argv[2:])
        cli_mode(question_arg)
        sys.exit(0)

    else:
        interactive_chat()
