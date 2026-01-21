import argparse
import logging
import subprocess
import sys
from utils import get_time
from questions_handler import (
    add_question,
    remove_question,
    remove_answer,
    list_all_questions,
    import_csv,
)
from chatbot import play_trivia, cli_mode

def parse_args():
    parser = argparse.ArgumentParser(
        description="Chatbot Application",
        add_help=False
    )

    parser.add_argument("--help", action="store_true", help="Show help message and exit")
    parser.add_argument("--log", action="store_true", help="Enable file logging")
    parser.add_argument("--log-level", choices=["INFO", "WARNING"], default="WARNING",
                        help="Set logging level (default WARNING)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--test", action="store_true", help="Run unit tests and exit")

    parser.add_argument("--import", dest="import_file", action="store_true",
                        help="Import questions from file (use with --filetype and --filepath)")
    parser.add_argument("--filetype", type=str, help="Import file type (only CSV supported)")
    parser.add_argument("--filepath", type=str, help="Path to import file")

    parser.add_argument("--add", action="store_true", help="Add a new question with answer")
    parser.add_argument("--question", type=str, help="Question text")
    parser.add_argument("--answer", type=str, help="Answer text")

    parser.add_argument("--remove", action="store_true", help="Remove a question or specific answer")
    parser.add_argument("--list", action="store_true", help="List all stored questions")

    return parser.parse_args()

def handle_cli_args():
    args = parse_args()

    if args.help:
        from utils import HELP_TEXT
        print(HELP_TEXT)
        sys.exit(0)

    if args.log:
        logging.basicConfig(
            filename="chatbot.log",
            filemode="a",
            level=logging.INFO if args.log_level == "INFO" else logging.WARNING,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        logging.info("Logging enabled")
    else:
        logging.disable(logging.CRITICAL)

    DEBUG_MODE = args.debug

    if args.test:
        if DEBUG_MODE:
            print(f"{get_time()} DEBUG: Running tests with debug mode enabled...")
        else:
            print("Running unit tests...")
        subprocess.run([sys.executable, "test_chatbot.py"])
        sys.exit(0)

    if args.import_file:
        if not args.filetype or not args.filepath:
            print(f"{get_time()} Chatbot: --import requires --filetype and --filepath")
            sys.exit(1)
        if args.filetype.upper() != "CSV":
            print(f"{get_time()} Chatbot: Unsupported file type. Only CSV is allowed.")
            sys.exit(1)
        import_csv(args.filepath)
        sys.exit(0)

    if args.add:
        if not args.question or not args.answer:
            print(f"{get_time()} Chatbot: Usage: --add --question \"Q\" --answer \"A\"")
            sys.exit(1)
        add_question(args.question, args.answer)
        sys.exit(0)

    if args.remove:
        if not args.question:
            print(f"{get_time()} Chatbot: Usage: --remove --question \"Q\" [--answer \"A\"]")
            sys.exit(1)
        if args.answer:
            remove_answer(args.question, args.answer)
        else:
            remove_question(args.question)
        sys.exit(0)

    if args.list:
        list_all_questions()
        sys.exit(0)

    if args.question and not (args.add or args.remove or args.import_file):
        cli_mode(args.question)
        sys.exit(0)

    # If no recognized CLI command - return to interactive mode
