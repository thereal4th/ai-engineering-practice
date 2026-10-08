import datetime
import json
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo


def get_weather(city):
    try:
        g = json.load(urllib.request.urlopen(
            "https://geocoding-api.open-meteo.com/v1/search?"
            + urllib.parse.urlencode({"name": city, "count": 1}), timeout=10))
        if not g.get("results"):
            return f"Error: no place called {city!r} was found."
        loc = g["results"][0]
        w = json.load(urllib.request.urlopen(
            "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
                "latitude": loc["latitude"], "longitude": loc["longitude"],
                "current": "temperature_2m,precipitation"}), timeout=10))["current"]
        return f"{loc['name']}, {loc.get('country', '')}: {w['temperature_2m']}C, precipitation {w['precipitation']}mm"
    except Exception as e:
        return f"Error: could not get weather for {city} ({e})"


def get_current_time(timezone="UTC"):
    try:
        return datetime.datetime.now(ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception as e:
        return f"Error: unknown timezone {timezone!r} ({e})"


REGISTRY = {"get_weather": get_weather, "get_current_time": get_current_time}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {"type": "object",
                           "properties": {"city": {"type": "string", "description": "City name, e.g. Seoul"}},
                           "required": ["city"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time, in UTC unless a timezone is given.",
            "parameters": {"type": "object",
                           "properties": {"timezone": {"type": "string",
                                          "description": "Optional IANA timezone name, e.g. 'Asia/Seoul'. Omit for UTC."}},
                           "required": []},
        },
    },
]
