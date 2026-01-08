import random
from datetime import datetime

def get_time():
    return datetime.now().strftime("%H:%M:%S")


TRIVIA_QUESTIONS = [
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Earth", "Jupiter", "Mars", "Saturn"],
        "answer": "Jupiter"
    },
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Rome", "Madrid"],
        "answer": "Paris"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Shakespeare", "Hemingway", "Tolstoy", "Dickens"],
        "answer": "Shakespeare"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["H2O", "CO2", "NaCl", "O2"],
        "answer": "H2O"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Mars", "Venus", "Jupiter", "Mercury"],
        "answer": "Mars"
    },
    {
        "question": "How many continents are there on Earth?",
        "options": ["5", "6", "7", "8"],
        "answer": "7"
    },
    {
        "question": "What is the smallest prime number?",
        "options": ["0", "1", "2", "3"],
        "answer": "2"
    },
    {
        "question": "Which organ pumps blood through the body?",
        "options": ["Liver", "Heart", "Kidney", "Lung"],
        "answer": "Heart"
    },
    {
        "question": "Which is the fastest land animal?",
        "options": ["Cheetah", "Lion", "Horse", "Tiger"],
        "answer": "Cheetah"
    },
    {
        "question": "What gas do plants absorb from the air?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"],
        "answer": "Carbon Dioxide"
    },
]


def play_trivia():
    print(f"{get_time()} Chatbot: Trivia game started! Answer the following questions:")
    score = 0
    total_questions = 10
    questions = random.sample(TRIVIA_QUESTIONS, 10)

    for idx, q in enumerate(questions, 1):
        print(f"\nQuestion {idx} of {total_questions} | Current Score: {score}/{total_questions}")
        print(f"{q['question']}")
        for i, option in enumerate(q["options"], 1):
            print(f"  {i}. {option}")

        while True:
            answer = input(f"{get_time()} Your answer (number, or type 'exit' to quit): ").strip()
            if answer.lower() == "exit":
                print(f"{get_time()} Chatbot: You exited the game early. Final Score: {score}/{idx - 1}")
                print(f"{get_time()} Chatbot: Resuming normal chat...\n")
                return

            if answer.isdigit() and 1 <= int(answer) <= len(q["options"]):
                answer_text = q["options"][int(answer) - 1]
                if answer_text == q["answer"]:
                    print(f"{get_time()} Correct! ")
                    score += 1
                else:
                    print(f"{get_time()} Wrong . Correct answer: {q['answer']}")
                break
            else:
                print(f"{get_time()} Invalid choice. Enter a number between 1 and {len(q['options'])}.")

    print(f"\n{get_time()} Chatbot: Trivia game ended! Your score: {score}/{len(questions)}")
    print(f"{get_time()} Chatbot: Resuming normal chat...\n")



