import json
import sys

from openai import OpenAI

from tools import REGISTRY, TOOLS

MODEL = "gemma4:e2b-it-qat"
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama", timeout=120.0)


def call_tool(name, arguments):
    """Run one tool call. Any failure comes back as an error string, never a raise."""
    try:
        args = json.loads(arguments or "{}")
    except json.JSONDecodeError as e:
        print(f"[tool]   {name}({arguments})")
        return f"Error: arguments for {name} were not valid JSON ({e})"

    print(f"[tool]   {name}({args})")
    if name not in REGISTRY:
        return f"Error: unknown tool {name!r}"
    try:
        return REGISTRY[name](**args)
    except Exception as e:
        return f"Error: {name} failed ({type(e).__name__}: {e})"


def run(prompt):
    messages = [{"role": "user", "content": prompt}]

    while True:
        print(f"[sent]   messages={len(messages)}")
        resp = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
        choice = resp.choices[0]
        msg = choice.message
        print(f"[recv]   finish_reason={choice.finish_reason}")

        if choice.finish_reason == "stop":
            print("[stop]   reason=finish_reason=stop")
            return msg.content

        messages.append(msg.model_dump(exclude_none=True))
        for call in msg.tool_calls:
            result = call_tool(call.function.name, call.function.arguments)
            print(f"[result] {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "What's the weather in Seoul?"
    print(run(prompt))
