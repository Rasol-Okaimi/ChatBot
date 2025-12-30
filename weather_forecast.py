import requests
from datetime import datetime

# OpenWeatherMap API key
API_KEY = "https://api.openweathermap.org/data/2.5/weather?q=Goslar&appid=f46611925675b3de42dbbccab8d83212"

BASE_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


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

    return format_weather(data)


def get_forecast_weather(location, target_date):
    """
    Fetch weather forecast for a specific date (within 5 days).
    If date is outside forecast range, fallback to current weather.
    """
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_FORECAST_URL, params=params)
    response.raise_for_status()
    data = response.json()

    target_date = datetime.strptime(target_date, "%Y-%m-%d").date()

    for entry in data["list"]:
        entry_date = datetime.fromtimestamp(entry["dt"]).date()
        if entry_date == target_date:
            return format_weather(entry)

    # Fallback if date not found
    return get_current_weather(location)


def format_weather(data):
    """Format weather data into readable text"""
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    city = data.get("name", "the location")

    return f"Weather in {city}: {description}, {temperature}°C"
