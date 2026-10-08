import json

from openai import OpenAI

MODEL = "gemma4:e2b-it-qat"
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def get_weather(city):
    return f"{city}: 7C, light rain"


REGISTRY = {"get_weather": get_weather}

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "City name, e.g. Seoul"}},
            "required": ["city"],
        },
    },
}]
