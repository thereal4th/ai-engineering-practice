# Ex 1.5 — Visible Progress: Objectives

## Code changes on top of Ex 1.4 (`agent.py`)

1. Add `stream=True` to the `create()` call.
2. Replace `choice = resp.choices[0]` / `msg = choice.message` with the accumulator loop:
   1. Capture `finish_reason` when a chunk carries one.
   2. Print `reasoning` (from `delta.model_extra`) as it arrives, with `flush=True`.
   3. Print and accumulate `delta.content`, with `flush=True`.
   4. Accumulate `delta.tool_calls` into slots keyed by `tc.index` (id, name, arguments).
3. Rebuild `tool_calls` from the slots as a list of dicts, sorted by index.
4. Print a newline after the stream ends so log lines don't run into streamed text.
5. Point the stopping conditions at the accumulated values: `finish_reason` for the stop check, `content` for the return.
6. Switch the no-progress set and tool dispatch to dict access (`call["function"]["name"]`, `call["function"]["arguments"]`, `call["id"]`).
7. Replace `msg.model_dump(...)` with the hand-assembled message: `{"role": "assistant", "content": content or None, "tool_calls": tool_calls}`.

## Complete assignment objectives

### Done when
1. Text appears a piece at a time, not all at once.
2. Removing `flush=True` once shows everything arriving at once; then restore it.
3. On a tool-calling turn, `delta.content` stays empty throughout and the tokens arrive in `reasoning`.
4. The Ex 1.4 loop still completes, with all three stopping conditions intact (`finish_reason == "stop"`, no-progress, `max_iterations`).
5. The assistant message is assembled by hand, because a `Stream` has no `.choices[0].message`.

### Rules
1. Print `reasoning` and debug with it, but never branch on it; it's an Ollama extension, not part of the OpenAI spec.
2. Accumulate tool calls by `tc.index`, even though Ollama sends each call in one chunk; hosted APIs split them across chunks.
3. Leave everything else from Ex 1.4 unchanged: the stopping conditions, the registry dispatch and the `tool_call_id` matching.

### Understand
1. Why `flush=True` is required: Python buffers output, so without it the stream prints all at once.
2. Why the message must be rebuilt: a streamed response is a `Stream`, not a `ChatCompletion`.
3. Why streaming matters: it doesn't make the response faster, but a streamed wait reads as thinking while a silent one reads as broken.

### Submit
1. The script.
2. One sentence on where you'd want streaming in a real product and where you wouldn't.

### Grading (10 pts)
1. Streaming works, output appears incrementally: 5
2. Ex 1.4 loop still completes with streaming on: 1
3. `flush=True` present and understood: 2
4. Written answer shows judgment about when to stream: 2
