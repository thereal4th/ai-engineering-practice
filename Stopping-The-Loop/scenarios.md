# Stopping Scenarios

## Scenario 1: Normal exit (`finish_reason == "stop"`)

- **What triggers it:** the model has everything it needs and answers in plain text.
- **Test prompt:** something that needs both tools in a row, e.g. *"What's the weather in Seoul, and what time is it there?"*
- **Expected transcript:** call 1 → `get_weather`, call 2 → `get_current_time`, call 3 → `stop`, then the answer and a label like `stopped: finish_reason=stop`.
- **Covers:** the 8 points for multiple sequential tool calls.
- **Decision:** what to do with other finish reasons like `length`. They could count as a normal stop, get their own label, or be treated as an error.

## Scenario 2: Ceiling (`max_iterations = 5`)

- **What triggers it:** the loop reaches 5 model calls without stopping.
- **Test prompt:** this is the hard one to capture. With no-progress turned on, the suggested prompts stop at call 2, long before the ceiling. Options:
  - (a) Temporarily turn off the no-progress check and run *"Call get_current_time over and over until the seconds read exactly 00."*
  - (b) Use a prompt that changes the arguments each time, e.g. *"Check the time in 6 different timezones, one call at a time."* No-progress never fires, so the ceiling does.
- **Expected transcript:** 5 calls, then `stopped: max_iterations (5)`.
- **Decisions:**
  - Does the counter count model calls or tool calls?
  - Which option, (a) or (b)? Option (a) needs a temporary switch in the code, like a flag or argument. Option (b) needs no code change, but depends on how the model behaves.
  - On a ceiling stop, should it return whatever text the model last produced, or only the label?

## Scenario 3: No progress (same tool, same arguments, twice in a row)

- **What triggers it:** the tool call in this model response is identical to the one in the previous response.
- **Test prompt:** one of the assignment's suggestions, e.g. *"What is the weather in Seoul? Check it again. Then check it again."*
- **Expected transcript:** call 1 → `get_weather({'city': 'Seoul'})`, call 2 → the same call, then `stopped: no-progress`. The assignment says this should fire on the 2nd model call.
- **Covers:** the 3 points for terminating gracefully on an unsatisfiable prompt.
- **Decisions:**
  - **What to compare:** the parsed arguments or the raw JSON string? Raw strings can differ only in spacing; parsed dicts compare cleanly.
  - **Several tool calls in one response:** compare them one at a time, or the whole set against the previous response's set?
  - **When to check:** before running the repeated tool, which saves a wasted tool run, or after?

## Shared across all three

- **Timeout:** add `timeout=120.0` to the `OpenAI(...)` client.
- **Exit label format:** e.g. `[stop]   reason=no-progress`. It should match the existing `[sent]`/`[recv]`/`[tool]` style.
- **Transcripts file:** a new `Stopping-The-Loop/transcripts.md` with one section per scenario, in the same format as last time.
