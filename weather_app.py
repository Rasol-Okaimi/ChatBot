import requests
from datetime import datetime

# ✅ API KEY (ONLY the key, not a URL)
API_KEY = "f46611925675b3de42dbbccab8d83212"

BASE_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

#lecture_halls_events
locations_events = {
    "lecture hall a": {
        "location": "berlin",
        "description": "central campus building and seating for 200 people."
    },
    "research conference": {
        "location": "braunschweig",
        "event_date": "2026-01-24",
        "description": "Held at the Braunschweig Conference Center, Hall B."
    },
    "university seminar": {
        "location": "goslar",
         "event_date": "2026-01-23",
        "description": "Seminar room in the historic Goslar campus ,Hall C."
    },
    "when is university seminar": {
        "location": "goslar",
         "event_date": "2026-01-22",
        "description": "Seminar room in the historic Goslar campus ,Hall C."
    },
    "campus north": {
        "location": "wolfenbüttel",
        "description": "Main campus for engineering and sciences."
    },
    "library building": {
        "location": "berlin",
        "description": "Central library with extensive collections."
    }
}

def get_current_weather(location):
    """Fetch current weather for a location"""
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_CURRENT_URL, params=params)
    response.raise_for_status()
    data = response.json()

    return format_current_weather(data)


def get_forecast_weather(location, event_date):
    """
    Fetch weather forecast for a specific date (within 5 days).
    If not available, fallback to current weather.
    """
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_FORECAST_URL, params=params)
    response.raise_for_status()
    data = response.json()

    target_date = datetime.strptime(event_date, "%Y-%m-%d").date()

    for entry in data["list"]:
        entry_date = datetime.fromtimestamp(entry["dt"]).date()
        if entry_date == target_date:
            return format_forecast_weather(entry, location, event_date)

    # fallback
    return get_current_weather(location)


def format_current_weather(data):
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    city = data["name"]

    return f"Current weather in {city}: {description}, {temperature}°C"


def format_forecast_weather(entry, location, event_date):
    temperature = entry["main"]["temp"]
    description = entry["weather"][0]["description"]

    return f"Weather forecast on {event_date} in {location}: {description}, {temperature}°C"