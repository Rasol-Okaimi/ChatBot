import sys
from datetime import datetime


def get_time():

    return datetime.now().strftime("%H:%M:%S")

 # Handles (#10)
chat_questions = {
    "what is your name": "I am Chatbot Group 7.",
    "how are you": "I'm doing great, thank you!",
    "what is python": "Python is a powerful and easy-to-learn programming language.",
    "what is the capital of france": "The capital of France is Paris.",
    "who created you": "I was created by a developer using Python (Chatbot Group 7).",
    "what can you do": "I can answer basic questions and chat with you!",
    "what is 2 plus 2": "2 plus 2 equals 4.",
    "what is the largest planet": "Jupiter is the largest planet in our solar system.",
    "who is the president of the usa": "As of 2025, the President of the USA is Donald Trump.",
    "what is the tallest mountain": "Mount Everest is the tallest mountain in the world.",
}


def chatbot_response(question):
    q = question.strip().lower()
    if q in chat_questions:
        answer = chat_questions[q]
        return f"Chatbot: {answer} What else would you like to know?"
    else:
        return "Chatbot: Sorry, I don't recognize that question. Please ask another question."


def interactive_chat():
    # Handles #7 and #8
    print(f"{get_time()} Chatbot: Hello!")
    print(f"{get_time()} Chatbot: How can I help you?")

    while True:
        user_input = input(f"{get_time()} You: ").strip()
        if user_input.lower() in ["bye", "exit", "quit"]:
            print(f"{get_time()} Chatbot: Goodbye! Have a great day!")
            break
        else:
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