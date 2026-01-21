"""
This code is Responsible for all visual output on the Raspberry Pi Sense HAT LED matrix.
This module is used to display application status symbols, game indicators,
scores, and idle information such as temperature.
User Stories covered:
- #28 Trivia visual feedback
- #29 Idle temperature display
- #30 Visual status indicators
"""

import time

#Allows the app to run even without Sense HAT
try:
    from sense_hat import SenseHat
    sense = SenseHat()
    sense.clear()
    SENSE_AVAILABLE = True
except ImportError:
    sense = None
    #print("Unable to find Sense HAT library — LED display will be disabled")
    SENSE_AVAILABLE = False

# Basic Colors (RGB)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


# Utility helpers
def _safe_clear():
    if SENSE_AVAILABLE:
        sense.clear()

def _safe_sleep(seconds=1):
    time.sleep(seconds)

# Startup (#30) - Displays a startup symbol when the app launches
def show_startup_symbol():
    if not SENSE_AVAILABLE:
        return

    sense.show_message(">>", text_colour=GREEN, back_colour=BLACK, scroll_speed=0.08)
    _safe_clear()


# Trivia game indicators (#28, #30) - Displays a symbol when the trivia game starts
def show_game_start_symbol():
    if not SENSE_AVAILABLE:
        return

    sense.show_message("??", text_colour=YELLOW, back_colour=BLACK, scroll_speed=0.08)
    _safe_clear()

# Trivia game - Displays a check mark (✔) for correct or a cross (✘) for incorrect answer.
def show_result_on_sensehat(is_correct):
    if not SENSE_AVAILABLE:
        return

    if is_correct:
        sense.show_letter("✔", text_colour=GREEN)
    else:
        sense.show_letter("✘", text_colour=RED)
    _safe_sleep(1)  # Keep the symbol visible for 1 second
    _safe_clear()

# Trivia exit game -     Displays a symbol when exiting the trivia game.
                    #Optionally shows the player's score before the exit symbol.
def show_game_exit_symbol(score=None):
    if not SENSE_AVAILABLE:
        return

    if score is not None:
        show_score(score)

    sense.show_message("X", text_colour=RED, back_colour=BLACK, scroll_speed=0.08)
    _safe_clear()

# Trivia score game - Displays the player's score on the LED matrix
                     #Args:score (int): Final score of the trivia game
def show_score(score):
    if not SENSE_AVAILABLE:
        return

    sense.show_message(
        f"{score}",
        text_colour=BLUE,
        back_colour=BLACK,
        scroll_speed=0.1
    )
    _safe_clear()


# Idle temperature display (#29) - Displays the current temperature on the LED matrix
def show_temperature():
    if not SENSE_AVAILABLE:
        return

    temperature = round(sense.get_temperature())
    sense.show_message(
        f"{temperature}C",
        text_colour=WHITE,
        back_colour=BLACK,
        scroll_speed=0.1
    )
    _safe_clear()


# Status helpers - Displays a simple idle indicator (dot)
def show_idle_symbol():
    if not SENSE_AVAILABLE:
        return
    sense.set_pixel(3, 3, GREEN)
    _safe_sleep(0.5)
    _safe_clear()
