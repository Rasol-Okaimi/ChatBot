# ChatBot_Projekt7
```
"This project is a chatbot designed to assist users by providing information 
and answers, interacting with them, and offering full support similar to a customer service representative. 
It has been trained on a limited knowledge base for now.
```


## Development Team - Group 7 :
```
Rasol Mohammed Ali Al-Okaimi
Samarth Ghanshyambhai Jyani
Srushti Ghanshyambhai Sanghani
Krupaliben Ribadia
```


### Installation Steps
```
cd existing_repo
git remote add origin https://gitlab-fi.ostfalia.de/id137458/chatbot_projekt7.git
git branch -M main
git push -uf origin main
```

```
Run main chatbot python (chatbot.py) to start chat with system.
```

```
Run chat_app.py to start chat with system using our webpage.
```

```
Run admin_server.py to start Chatbot Admin Panel.
```

## Project Structure and functions 
```
1-Folders 
A-data/Project data files :
--user.json (user data)
-- chat_questions.json (questions database)
-- trivia_questions.json (trivia)
-- chat_questions.json
-- questions.csv (sample to be used for import questions test)
B-logs/Project logs 
C-templates/Html Web Pages

2-Flask
--------------------------------------
A- admin_server.py -- Admin Flask application - port  : http://127.0.0.1:5000/ 
#31 Create base management web-page (dashboard.html)
** user managment page () list_users.html + log page (logs.html)
#32 Allow service-provider to view questions/answers (list_qa.html)
#33 Allow service-provider to search for questions/answers (list_qa.html)
#36 Allow service-provider to edit questions/answers (edit_qa.html)   
#35 Allow service-provider to add/remove questions/answers (edit_qa.html) 

B- chat_app.py -- Chat Flask application - port  : http://127.0.0.1:5000/
#34 Create base chat page (chat.html)
#37 Allow user to chat without page reloads (chat.html)
#38 Suggest tips/questions after a period of inactivity  (chat.html)
#39 Allow user to download chat log  (chat.html) 

3-Python Files 
A-chatbot.py - Main chatbot application (Start & Run)
-Manages the interactive chat loop with the user.
-Processes user inputs and provides answers based on stored questions and weather info.
-Supports multiple questions in one input, saves chat logs, and handles idle suggestions and temperature display.
-Integrates a trivia game and Sense HAT LED display (if available).
-Supports commands like "save log," "trivia," and exit commands.
B-cli_handler.py (Command-line interface handler)
-Parses command-line arguments to enable features like logging, importing questions from CSV, adding/removing questions, running tests, and asking questions directly.
-Enables non-interactive use of the chatbot through CLI flags and arguments.

C-display.py (Visual output manager for Sense HAT)
-Displays startup and trivia game status symbols on the Raspberry Pi Sense HAT LED matrix.
-Shows game results, player's score, and idle temperature info visually.
-Handles LED clearing and safe display timing.

D-questions_handler.py (Question and answer management)
-Stores the main database of chatbot questions and answers.
-Loads and saves questions from/to JSON files.
-Imports questions from CSV files with validation.
-Allows adding/removing questions or specific answers.
-Provides listing of all stored questions.

E-test_chatbot.py (Unit tests for chatbot)
-Tests chatbot's response accuracy for known questions and variants.
-Verifies handling of compound questions and unknown queries.
-Tests suggestion system for question prompts.
-Uses Python's unittest framework for automated testing.
F-trivia_game.py (Trivia game module)
-Loads trivia questions from a JSON file and runs an interactive quiz game.
-Displays game status and results via Sense HAT LED (if available).
-Tracks and shows the player’s score, supports early exit.
-Provides user prompts and input validation during the game.
G-utils.py (Utility functions and help text)
-Provides a formatted current time string for logging and prompts.
-Contains detailed CLI help text explaining available command-line options and usage examples.
H-weather_app.py(Weather information module)
-Fetches current weather and forecast data using the OpenWeatherMap API.
-Contains predefined event locations with descriptions and event dates.
-Provides formatted weather reports for current or future dates at specified locations.
-Handles fallback to current weather if forecast data for a date is unavailable.

```

## Support Files
README.md
requirements.txt

