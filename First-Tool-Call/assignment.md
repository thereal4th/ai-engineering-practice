Ex 1.3 — First Tool Call ★
📌 worth
40 points
· file
Intermediate · 2.5 hours

This is the most important exercise in the course. When it works, you have an agent.

What you're building
You have just watched get_weather("Seoul") go all the way round the loop. Now you build it — in three passes, each one adding exactly one new thing on top of a version that already runs.

Pass	What you add	Why this order
1	The round trip, with a fake weather function	if it breaks, it is your wiring — nothing else
2	A real API call inside that same function	proves the loop does not care what a tool does
3	A second tool, get_current_time()	now the model has to choose
Get each pass running before you start the next. If you are ever debugging two new things at once, you skipped a pass.

Pass 1 — The round trip, faked
Write the loop from the concept page, and give it a function that simply lies:

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
Ask it "What's the weather in Seoul?" and do not move on until the final answer contains your fake string. When it does, the round trip is sound: finish_reason flipped, the tool_call_id matched, and the model read your result.

Use a fixed question written into your code here, not input(). The loop you are writing turns once per model call, not once per human turn — they are different loops, and Exercise 1.4 is where you nest one inside the other.

That description is not a comment. The model reads it to decide whether to call the tool. Part 2 is largely about that one sentence.

The line that does the real work
args = json.loads(call.function.arguments)     # -> {'city': 'Seoul'}
result = REGISTRY[call.function.name](**args)
You wrote the word Seoul in an ordinary English sentence. The model found it, matched it to the city parameter you declared, and handed it back as JSON your Python could call. That is what tool parameters are for — and it is why a tool with no parameters would teach you only half of this lesson.

Pass 2 — Make it true
Now replace only the body of get_weather. Do not touch the loop, TOOLS, or REGISTRY.

import json, urllib.request, urllib.parse

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
        return f"{loc['name']}, {loc.get('country','')}: {w['temperature_2m']}C, precipitation {w['precipitation']}mm"
    except Exception as e:
        return f"Error: could not get weather for {city} ({e})"
No API key and no signup — Open-Meteo is free and keyless. Run the same prompt and you should get the real temperature in a real city.

Now stop and look at what you did not change. The loop is the same. The schema is the same. The registry is the same. You swapped the inside of one function and your agent went from pretend to real. That is the whole point of the tool boundary: your harness does not know or care what happens inside a tool, only that it takes arguments and gives back a string.

Failure is a result, not a crash
Look closely at that except block. A failing tool returns text; it does not raise. Ask for the weather in Zzqqxplt and watch what the model does with it entirely on its own:

"I'm sorry, I could not find any location or city called 'Zzqqxplt'. Could you please provide a valid city name?"

That recovery is only possible because the error travelled the same path as a result would have. A tool that raises kills your loop. A tool that returns its own failure lets the model deal with it.

One warning about that except Exception, and it is the reason the message interpolates {e} rather than just the exception type. A broad except catches network failures — which is what you want — but it also catches your own bugs, and dresses them up as tool failures. Forget the urllib import and your agent will calmly report a weather-service problem forever, because Error: could not get weather for Seoul (NameError) looks exactly like a broken API. Error: could not get weather for Seoul (name 'urllib' is not defined) is a five-second fix. Make your error strings carry enough detail to tell broken code apart from a broken service.

One more, for the paranoia it will earn you
Now ask for the weather in Wakanda. The geocoder helpfully finds "Wakanda Park, United States" and your agent will confidently report its temperature. The tool did not fail — it succeeded and returned something useless, and nothing in your harness can tell the difference. Remember this the next time you are tempted to trust a tool result.

Pass 3 — A second tool
Add get_current_time() to both TOOLS and REGISTRY. Give it an optional timezone that defaults to UTC:

import datetime
from zoneinfo import ZoneInfo

def get_current_time(timezone="UTC"):
    try:
        return datetime.datetime.now(ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception as e:
        return f"Error: unknown timezone {timezone!r} ({e})"
Both halves matter. The schema goes in TOOLS so the model knows the tool exists; the function goes in REGISTRY so your code can find it. Watch the brackets — the second tool is a sibling of the first inside the list, not nested inside it:

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

REGISTRY = {"get_weather": get_weather, "get_current_time": get_current_time}
Notice that timezone is declared but not required — it appears in properties but not in required. That is a distinction worth internalising now: the model may send it, and when your question does not mention a place it simply will not. You will see get_current_time({}) in your telemetry, and **args unpacks an empty dict perfectly happily into a function whose parameter already has a default.

The registry key must match the name in the schema, not the name of your Python function. Your loop looks up REGISTRY[call.function.name], and call.function.name is whatever you told the model the tool was called. Declare it as get_time while your function is get_current_time and you get a KeyError the first time the model reaches for it — with code that reads perfectly fine.

Once again the loop does not change. But now the model has a choice to make, so test all three cases:

Prompt	Expected
"What's the weather in Seoul?"	get_weather only
"What time is it?"	get_current_time({}) — no timezone sent, so UTC
"What time is it in Seoul?"	get_current_time({"timezone": "Asia/Seoul"})
"What time is it, and what's the weather in Paris?"	both tools
"What is the capital of France?"	no tool at all — finish_reason is "stop"
The last row matters as much as the first. A model that reaches for a tool on every single turn is nearly impossible to build a harness around. Yours knows when not to.

Watch the middle row carefully: the model may hand you two tool calls inside one message. If you wrote for call in msg.tool_calls: you already handle that. If you wrote msg.tool_calls[0], this is where you find out.

Requirements
Your [TOOL] telemetry line prints the function name and its arguments before the function runs
Each result is appended with its matching tool_call_id, never by position in the array
get_weather calls the live API, and returns its errors as strings instead of raising
The final answer demonstrably contains a value your function returned
What to submit
Your script, plus one transcript for each row of the Pass 3 table — the tool called, both tools called, and the tool correctly not called.

You're done when
finish_reason flipped to "tool_calls" and message.content came back empty
Your four telemetry lines appear in order: [sent] [tool] [result] [sent], and the message count goes 1 → 3
The final answer contains a value your own function returned — not one the model invented
"What is the capital of France?" produces no tool call at all
If one of those is not true, the exercise is not finished — and the gap is where the lesson is.

Grading — 40 points
Criterion	Points
Round trip completes: the tool_calls branch, result appended, model answers	10
Arguments read via json.loads and passed into the real function	8
get_weather calls the live API and returns a real reading	8
A failing tool returns an error string and the loop survives	7
Results matched by tool_call_id, not by position	4
Correctly abstains on the no-tool question	3
Automatic fail: putting the weather into the prompt yourself, or submitting with the Pass 1 fake still in place. That is the assignment, not a shortcut around it.

No internet today? Passes 1 and 3 run completely offline. Submit those, say so in your notes, and finish Pass 2 once you are back online.