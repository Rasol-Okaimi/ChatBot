import sys
import random
from datetime import datetime


def get_time():

    return datetime.now().strftime("%H:%M:%S")

 # Handles (#10)
chat_questions = {
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
         "Python is learn programming language.",
        "Python is a popular programming language used for many types of software development.",
    ],

    "what is the capital of france": [
        "The capital of France is Paris.",
        "Paris is the capital city of France.",
        "France’s capital is Paris.",
    ],

    "who created you": [
        "I was created by a developer using Python.",
        "I was developer by Python!",
        "A Python developer brought me to life!",
    ],

    "what can you do with python": [
        "I can answer basic questions and chat with you!",
        "I am here to help you!",
        "I’m able to respond to simple questions and keep you company!",
    ],

    "what is 2 plus 2": [
        "2 plus 2 equals 4.",
         " 4 is the answer.",
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

    "what is the tallest mountain": [
        "Mount Everest is the tallest mountain in the world.",
        "Everest the tallest mountain in the world.",
        "Everest is the highest mountain above sea level.",
    ],
}

keyword_suggestions = { ## keyword_suggestions Handles (#12)
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

last_suggestions = []

def chatbot_response(question):
    q = question.strip().lower()
    if q in chat_questions:
        answer = random.choice(chat_questions[q])  # Handles (#11)
        return f"Chatbot: {answer} What else would you like to know?"
    else:
        return "Chatbot: Sorry, I don't recognize that question. Please ask another question."

def suggest_questions(keyword): ## Handles (#12)
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
        user_input = input(f"{get_time()} You: ").strip()
        if user_input.lower() in ["bye", "exit", "quit"]:
            print(f"{get_time()} Chatbot: Goodbye! Have a great day!")
            break
        ## Handles (#12) # If the user enters a number, we check if it is a number selected from previous suggestions.
        if user_input.isdigit() and last_suggestions:
            choice = int(user_input)
            if 1 <= choice <= len(last_suggestions):
                selected_question = last_suggestions[choice - 1]
                response = chatbot_response(selected_question)
                print(f"{get_time()} {response}")

                ## Handles (#12) # After selection, we re-examine the suggestions to avoid errors later.
                last_suggestions = []
                continue
            else:
                print(f"{get_time()} Chatbot: Invalid question number. Please try again.")
                continue


        ## Handles (#12) #If it's not a number, we look for a keyword to suggest questions.
        suggestions = suggest_questions(user_input)
        if suggestions:
            last_suggestions = suggestions
            print(f"{get_time()} Chatbot: You might want to ask:-")
            for i, q in enumerate(suggestions, 1):
                print(f"  {i}. {q}")
            print(f"{get_time()} Chatbot: Please type the number of your question choice.")
            continue

        ## Handles (#12) # If it's neither a number nor a keyword, we'll reply directly.
        response = chatbot_response(user_input)
        print(f"{get_time()} {response}")


def cli_mode(question):
    # Handles (9)
    response = chatbot_response(question)
    print(f"{get_time()} {response}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--question":
        question_arg = sys.argv[2]
        cli_mode(question_arg)
    else:
        interactive_chat()