import random
from datetime import datetime

def get_time():
    return datetime.now().strftime("%H:%M:%S")


TRIVIA_QUESTIONS = [
    {
        "question": "Which programming language is mainly used for data science?",
        "options": ["Python", "HTML", "CSS", "SQL"],
        "answer": "Python"
    },
    {
        "question": "What does CPU stand for?",
        "options": ["Central Processing Unit", "Computer Power Unit", "Core Processing Utility", "Central Program Unit"],
        "answer": "Central Processing Unit"
    },
    {
        "question": "Which company developed the Windows operating system?",
        "options": ["Apple", "Microsoft", "Google", "IBM"],
        "answer": "Microsoft"
    },
    {
        "question": "What does HTTP stand for?",
        "options": ["HyperText Transfer Protocol", "High Transfer Text Program", "Host Transfer Protocol", "Hyper Transfer Tool Package"],
        "answer": "HyperText Transfer Protocol"
    },
    {
        "question": "Which of the following is a database system?",
        "options": ["MySQL", "Python", "HTML", "Linux"],
        "answer": "MySQL"
    },
    {
        "question": "What is the correct file extension for a Python file?",
        "options": [".py", ".java", ".html", ".exe"],
        "answer": ".py"
    },
    {
        "question": "Which device is used to store data permanently?",
        "options": ["RAM", "CPU", "Hard Drive", "Cache"],
        "answer": "Hard Drive"
    },
    {
        "question": "What does GUI stand for?",
        "options": ["Graphical User Interface", "General User Input", "Global User Interaction", "Graphic Utility Interface"],
        "answer": "Graphical User Interface"
    },
    {
        "question": "Which operating system is open-source?",
        "options": ["Windows", "macOS", "Linux", "iOS"],
        "answer": "Linux"
    },
    {
        "question": "What is the purpose of a firewall?",
        "options": ["Increase internet speed", "Protect a network", "Store data", "Run applications"],
        "answer": "Protect a network"
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



