import os
import re  # For regex splitting compound questions
import sys
import random
import subprocess
import logging
from trivia_game import play_trivia
from utils import HELP_TEXT, get_time
from weather_app import locations_events, get_current_weather, get_forecast_weather
from questions_handler import (
    chat_questions,
    add_question,
    remove_question,
    remove_answer,
    list_all_questions,
    import_csv,
    save_questions_to_file,
)

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

question_variants = {
    "what is python programing": "what is python",
    "can you describe python programming": "what is python",
    "what do you mean by python programming": "what is python",
    "what is the meaning of python programming": "what is python",
    "what is python language": "what is python",
}

last_suggestions = []

def extract_location_and_date(user_input):
    """
    Extract location and date from user input.
    Returns (location, date)
    """
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", user_input)
    event_date = date_match.group() if date_match else None

    known_locations = list(set(
        event["location"].lower()
        for event in locations_events.values()
        if "location" in event
    ))

    location = None
    for city in known_locations:
        if city in user_input.lower():
            location = city.title()
            break

    return location, event_date

def chatbot_response(user_input):
    logging.info(f"User asked: {user_input}")

    user_input = user_input.lower().strip()

    if user_input in locations_events:
        location = locations_events[user_input]["location"]
        description = locations_events[user_input].get("description", "")
        event_date = locations_events[user_input].get("event_date", None)

        answers = chat_questions.get(user_input, [])
        answer = random.choice(answers) if answers else ""

        try:
            if event_date:
                weather = get_forecast_weather(location, event_date)
                if weather is None:
                    weather = "I found the location, but could not get the weather right now."
            else:
                weather = get_current_weather(location)
        except Exception:
            weather = "I found the location, but could not get the weather right now."

        response_parts = []
        if answer:
            response_parts.append(answer)
        if location:
            response_parts.append(f"Location: {location.title()},")
        if event_date:
            response_parts.append(f"Event date: {event_date},")
        if description:
            response_parts.append(f"Description: {description}")

        response_parts.append(f"{weather}")

        combined_response = " ".join(response_parts)
        return f"Chatbot: {combined_response} . What else would you like to know?"

    location, event_date = extract_location_and_date(user_input)

    if location:
        try:
            if event_date:
                weather = get_forecast_weather(location, event_date)
                return f"Chatbot: {weather} , What else would you like to know?"
            else:
                weather = get_current_weather(location)
                return f"Chatbot: {weather} , What else would you like to know?"
        except Exception:
            return "Chatbot: I found the location, but could not get the weather right now."

    split_pattern = r'\s*(?:and|or|also|as well as|and also|or also)\s*|[?,;]+\s*'
    parts = re.split(split_pattern, user_input)

    found_answers = []

    for part in parts:
        clean_part = part.strip().replace('?', '')

        if not clean_part:
            continue

        if clean_part in question_variants:
            clean_part = question_variants[clean_part]

        if clean_part in chat_questions:
            answer = random.choice(chat_questions[clean_part])
            found_answers.append(answer)
            logging.info(f"Answer found for: {part}")
        else:
            logging.warning(f"Unknown question: {part}")

    if found_answers:
        if len(found_answers) == 1:
            return f"Chatbot: {found_answers[0]} What else would you like to know?"
        else:
            combined_response = " Also, ".join(found_answers)
            return f"Chatbot: {combined_response} What else would you like to know?"
    else:
        return "Chatbot: Sorry, I don't recognize that question (or combination of questions). Please ask another question."

def suggest_questions(keyword):
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

if __name__ == "__main__":
    from cli_handler import handle_cli_args
    handle_cli_args()  # handle CLI commands first
    interactive_chat()  # fallback to interactive chat if no CLI commands
