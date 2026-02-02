import os
import re  # For regex splitting compound questions
import sys
import random
import logging
import threading
import subprocess
import logging
import time  # Sense HAT

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

from display import (
    show_startup_symbol,
    show_game_start_symbol,
    show_temperature,
    show_game_exit_symbol
)

# Allows the app to run even without Sense HAT
try:
    from sense_hat import SenseHat
    sense = SenseHat()
    sense.clear()
except ImportError:
    sense = None
    #print("Unable to find Sense HAT library — LED display will be disabled")


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
last_input_time = time.time()  # Last user entry time

IDLE_TIMEOUT = 60  # seconds of inactivity required before temperature display
temperature_shown = False

def save_chat_log(chat_log, directory="."):
    """Save chat log into a timestamped .txt file.
    Filename format: chat-log-YYYY-MM-DD-HH-MM.txt
    Returns the saved file path, or None if nothing was saved.
    """
    if not chat_log:
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename = f"chat-log-{timestamp}.txt"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(chat_log).strip() + "\n")

    return filepath

#Extract location and date from user input + Returns (location, date)
def extract_location_and_date(user_input):
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

#Display temperature on Sense HAT LED matrix.
def temperature_display_loop():
    global last_input_time, temperature_shown

    while True:
        idle_duration = time.time() - last_input_time

        if idle_duration >= IDLE_TIMEOUT and not temperature_shown:
            try:
                print(f"{get_time()} Idle mode → Display temperature")
                show_temperature()
                temperature_shown = True
                print(f"{get_time()} You: ", end="", flush=True)
            except Exception as e:
                logging.warning(f"Failed to display temperature: {e}")

        time.sleep(1)  # time check for display temperature

def interactive_chat():
    global last_suggestions, last_input_time, temperature_shown
    print(f"{get_time()} Chatbot: Hello!")
    print(f"{get_time()} Chatbot: How can I help you?")

    while True:
        try:
            user_input = input(f"{get_time()} You: ").strip()
            last_input_time = time.time()
            temperature_shown = False
        except EOFError:
            break
        
         if user_input.lower() in ["download", "download log", "save", "save log"]:
            if not chat_log:
                print(f"{get_time()} Chatbot: Chat log is empty. Nothing to download.")
           
            continue


        # Sense HAT - user input , clear screen
        if sense is not None:
            sense.clear()

        if not user_input:
            continue

        if user_input.lower() in ["bye", "exit", "quit"]:
            logging.info("User exited application")
            print(f"{get_time()} Chatbot: Goodbye! Have a great day!")
            break

        if user_input.lower() == "trivia":
            show_game_start_symbol()  #30 game start code
            score = play_trivia()       # trivia return  result
            show_game_exit_symbol(score)  #30 Game end displayed with score
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
    show_startup_symbol()  # 30 Display the app start code
    from cli_handler import handle_cli_args
    handle_cli_args()  # handle CLI commands first

    if sense is not None:
        # temperature display
        #print("Starting temperature display ...")
        temp_thread = threading.Thread(target=temperature_display_loop, daemon=True)
        temp_thread.start()

    interactive_chat()  # fallback to interactive chat if no CLI commands