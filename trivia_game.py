import json
import os
import random
from datetime import datetime
import time

# Sense HAT display (User Stories #28 and #30)
from display import (
    show_game_start_symbol,
    show_game_exit_symbol,
    show_result_on_sensehat,
    show_score
)

def get_time():
    return datetime.now().strftime("%H:%M:%S")


def load_trivia_questions():
    path = os.path.join("data", "trivia_questions.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Runs the trivia game - Visual feedback is displayed via Sense HAT if available.
def play_trivia():
    # Visual indicator: game started (Story #30)
    show_game_start_symbol()

    print(f"{get_time()} Chatbot: Trivia game started! Answer the following questions:")
    score = 0
    total_questions = 10

    all_questions = load_trivia_questions()

    total_questions = min(10, len(all_questions))
    questions = random.sample(all_questions, total_questions)

    for idx, q in enumerate(questions, 1):
        print(f"\nQuestion {idx} of {total_questions} | Current Score: {score}/{total_questions}")
        print(f"{q['question']}")

        for i, option in enumerate(q["options"], 1):
            print(f"  {i}. {option}")

        while True:
            answer = input(f"{get_time()} Your answer (number, or type 'exit' to quit): ").strip()

            # Early exit handling
            if answer.lower() == "exit":
                print(f"{get_time()} Chatbot: You exited the game early. Final Score: {score}/{idx - 1}")

                # Show score + exit symbol (Story #30)
                show_score(score)
                show_game_exit_symbol()

                print(f"{get_time()} Chatbot: Resuming normal chat...\n")
                return score  # Return score on early exit

            if answer.isdigit() and 1 <= int(answer) <= len(q["options"]):
                answer_text = q["options"][int(answer) - 1]

                if answer_text == q["answer"]:
                    print(f"{get_time()} Correct!")
                    show_result_on_sensehat(True)  # Display True score
                    score += 1
                else:
                    print(f"{get_time()} Wrong. Correct answer: {q['answer']}")
                    show_result_on_sensehat(False)  # Display False score

                break
            else:
                print(f"{get_time()} Invalid choice. Enter a number between 1 and {len(q['options'])}.")

    # Game finished normally
    print(f"\n{get_time()} Chatbot: Trivia game ended! Your score: {score}/{len(questions)}")

    # Show final score + exit symbol (Story #30)
    show_score(score)
    show_game_exit_symbol()

    print(f"{get_time()} Chatbot: Resuming normal chat...\n")
    return score  # Return score on normal finish
