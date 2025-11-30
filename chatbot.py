import sys
import random
import re  # Added for regex splitting to handle compound questions
import csv
from datetime import datetime


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

keyword_suggestions = {  ## keyword_suggestions Handles (#12)
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

    user_input = user_input.lower().strip()

    # Handles (#13) Compound questions
    # 1. Define delimiters for compound questions.
    # We split by: ' and ', ' or ', ' & ', or punctuation like ',' '?' or ';'
    # The regex logic:
    # \s+ matches whitespace
    # (?: ... ) groups words like 'and', 'or' without capturing them as separate tokens in the result
    # [?,;] matches punctuation
    split_pattern = r'\s*(?:and|or|also|as well as|and also|or also)\s*|[?,;]+\s*'
    # Handles (#13) Compound questions
    # Split the input string into parts based on the pattern
    parts = re.split(split_pattern, user_input)

    found_answers = []

    for part in parts:
        # Clean up the specific part (remove trailing whitespace or ?)
        clean_part = part.strip().replace('?', '')

        if not clean_part:
            continue  # Skip empty strings caused by trailing punctuation

        # Handles (#14) Handle multiple variations of the same question
        if clean_part in question_variants:
            clean_part = question_variants[clean_part]

        # Check if this part exists in our knowledge base
        if clean_part in chat_questions:
            answer = random.choice(chat_questions[clean_part])
            found_answers.append(answer)

    # 2. Construct the final response
    if len(found_answers) > 0:
        # If we found multiple answers, join them nicely.
        if len(found_answers) == 1:
            return f"Chatbot: {found_answers[0]} What else would you like to know?"
        else:
            # Join multiple answers with a separator
            combined_response = " Also, ".join(found_answers)
            return f"Chatbot: {combined_response} What else would you like to know?"
    else:
        # If no parts matched, return the error message
        return "Chatbot: Sorry, I don't recognize that question (or combination of questions). Please ask another question."


def suggest_questions(keyword):  ## Handles (#12)
    keyword = keyword.lower()
    if keyword in keyword_suggestions:
        return keyword_suggestions[keyword]
    return None


def interactive_chat():
    # Handles #7 and #8
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
            print(f"{get_time()} Chatbot: Goodbye! Have a great day!")
            break

        ## Handles (#12) - Selection by Number
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

        ## Handles (#12) - Keyword Suggestions
        # Note: If the user types a compound question like "python and java",
        # suggest_questions might fail to find a direct match, which is fine.
        # It will pass through to chatbot_response to be handled as a compound question.
        suggestions = suggest_questions(user_input)
        if suggestions:
            last_suggestions = suggestions
            print(f"{get_time()} Chatbot: You might want to ask:")
            for i, q in enumerate(suggestions, 1):
                print(f"  {i}. {q}")
            print(f"{get_time()} Chatbot: Please type the number of your question choice.")
            continue

        last_suggestions = []  # Clear suggestions if user types something new

        ## Handles (#12) and Compound Questions
        response = chatbot_response(user_input)
        print(f"{get_time()} {response}")


def cli_mode(question):
    # Handles (9)
    response = chatbot_response(question)
    print(f"{get_time()} {response}")

# Handles (#15) Import CSV file
def import_csv(filepath):
    global chat_questions

    new_data = {}

    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            question = row["question"].strip().lower()

            answers = [
                row["answer1"],
                row["answer2"],
                row["answer3"],
                row["answer4"]
            ]

            # remove empty answers
            answers = [a for a in answers if a and a.strip()]

            new_data[question] = answers

    chat_questions = new_data
    print(f"{get_time()} Chatbot: CSV imported successfully! {len(chat_questions)} questions loaded.")


if __name__ == "__main__":
    # if len(sys.argv) > 2 and sys.argv[1] == "--question":
    #     question_arg = " ".join(sys.argv[2:])
    #     cli_mode(question_arg)
    # else:
    #     interactive_chat()
    
      # Import mode
    if "--import" in sys.argv:
        try:
            filetype = sys.argv[sys.argv.index("--filetype") + 1]
            filepath = sys.argv[sys.argv.index("--filepath") + 1]

            if filetype.upper() == "CSV":
                import_csv(filepath)
            else:
                print("Unsupported file type. Only CSV is allowed.")
                sys.exit(1)

        except Exception as e:
            print("Error during import:", e)
            sys.exit(1)

    # CLI question mode
    if len(sys.argv) > 2 and "--question" in sys.argv:
        question_arg = " ".join(sys.argv[sys.argv.index("--question") + 1:])
        cli_mode(question_arg)

    else:
        interactive_chat()