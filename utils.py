from datetime import datetime

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

def get_time():
    return datetime.now().strftime("%H:%M:%S")
