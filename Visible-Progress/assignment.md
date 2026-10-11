Part 1 — The Loop
Ex 1.5 — Visible Progress
📌 worth
10 points
· file
Fundamental · 1 hour

What you're building
Turn on streaming and print tokens as they arrive.

stream = client.chat.completions.create(model=MODEL, messages=messages, stream=True)
for chunk in stream:
    piece = chunk.choices[0].delta.content or ""
    print(piece, end="", flush=True)
flush=True is not optional — without it Python buffers and you get everything at once, which defeats the entire point.

Why a one-hour exercise earns its place
An 8-second silent wait and an 8-second streaming response take exactly the same time and feel completely different. One reads as broken; the other reads as thinking.

Perceived performance is a design decision, and it is nearly free. Your capstone will feel twice as good for these twenty lines.

The catch: your harness already has tools in it
Two things break the moment you put stream=True into the loop from Exercise 1.4, and the second one is not obvious.

There is no message object. A streamed response is a Stream, not a ChatCompletion, so the line you have written in every exercise since 1.1 simply stops existing:

msg = resp.choices[0].message
# AttributeError: 'Stream' object has no attribute 'choices'
There is nothing left to hand to messages.append(). You assemble that dict yourself, out of the fragments.

On a tool-calling turn, delta.content is empty the whole way through. Print only delta.content and you will watch a blank screen and conclude streaming is broken. It is not — the tokens are arriving in a different field.

Where the tokens actually are
Measured on gemma4:e2b-it-qat, asking for the weather in Seoul with one tool offered:

chunks	field	what arrived
0–122	reasoning	673 characters of the model's scratchpad
123	tool_calls	the entire call at once — name and arguments together
124	finish_reason	"tool_calls"
all 125	content	empty
So reasoning is not a bonus round. On a tool turn it is the only thing streaming, and it is the clearest view of tool selection anywhere in this course:

[thinking] To get the time in Seoul, I should call get_current_time with the timezone set to 'Asia/Seoul'.

It is an Ollama extension, not part of the OpenAI spec — print it, debug with it, never branch on it.

Note too that Ollama delivered the tool call whole, in a single chunk. Hosted APIs usually split delta.tool_calls across many, so accumulate by tc.index anyway: four extra lines, and the difference between code that works here and code that works anywhere.

The accumulator
Read this one rather than derive it — the exercise is the streaming, not the bookkeeping:

content, finish_reason, slots = "", None, {}

for chunk in resp:
    choice = chunk.choices[0]
    delta = choice.delta
    if choice.finish_reason:
        finish_reason = choice.finish_reason

    thought = (delta.model_extra or {}).get("reasoning")
    if thought:
        print(thought, end="", flush=True)

    if delta.content:
        print(delta.content, end="", flush=True)
        content += delta.content

    for tc in (delta.tool_calls or []):
        slot = slots.setdefault(tc.index, {"id": "", "name": "", "arguments": ""})
        if tc.id:                 slot["id"] = tc.id
        if tc.function.name:      slot["name"] += tc.function.name
        if tc.function.arguments: slot["arguments"] += tc.function.arguments

tool_calls = [{"id": s["id"], "type": "function",
               "function": {"name": s["name"], "arguments": s["arguments"]}}
              for _, s in sorted(slots.items())]
Then, in place of messages.append(msg), build the message by hand:

messages.append({"role": "assistant",
                 "content": content or None,
                 "tool_calls": tool_calls})
Everything else in your Exercise 1.4 loop stays exactly as it was — all three stopping conditions, the registry dispatch, the tool_call_id matching.

What to submit
The script, plus one sentence on where you'd want streaming in a real product and where you wouldn't.

You're done when
Text appears a piece at a time rather than all at once — remove flush=True once to see the difference
On a tool-calling turn delta.content stays empty the whole way through, and the tokens arrive in reasoning
Your Ex 1.4 loop still completes, with all three stopping conditions intact
You assembled the assistant message yourself, because a Stream has no .choices[0].message
If one of those is not true, the exercise is not finished — and the gap is where the lesson is.

Grading — 10 points
Criterion	Points
Streaming works, output appears incrementally	5
Your Exercise 1.4 loop still completes with streaming on	1
flush=True present and understood	2
Written answer shows judgment about when to stream	2