Part 1 — The Loop
Ex 1.4 — Stopping the Loop
📌 worth
25 points
· file
Intermediate · 2 hours

What you're building
Exercise 1.3 handled tool calls one turn at a time. Real tasks need several in sequence — so wrap it in a while loop. You already have two tools from Pass 3, so ask something that needs both.

Then make it stop. Three different ways:

1.  finish_reason == "stop"     the model is done — the normal exit
2.  max_iterations              a hard ceiling. start at 5.
3.  no-progress detection       same tool, same arguments, twice running
Why three
An agent is a loop with an exit condition. Which exit conditions you choose is the design of your harness — not boilerplate you bolt on at the end.

Condition 1 is the happy path. Condition 2 is your seatbelt. Condition 3 catches the genuinely nasty case: an agent confidently doing the same useless thing forever — which condition 1 never catches and condition 2 only catches slowly.

Also: set a timeout
client = OpenAI(base_url=..., api_key="ollama", timeout=120.0)
A hung request must not hang your harness forever.

A note on retries. You may be tempted to add exponential backoff. Don't — not here. Backoff is for rate-limited hosted APIs. Running locally, if the server is down, retrying just delays the error; if the model is loading, you needed a longer timeout, not a second request. When you port this harness to a hosted API later, backoff becomes essential. Knowing when a pattern applies is worth more than knowing the pattern.

Try to break it
Temporarily remove the ceiling and give it something it cannot finish. All three of these trip the no-progress check on the second model call — measured against gemma4:e2b-it-qat, not guessed:

Call get_current_time over and over until the seconds read exactly 00.
What is the weather in Seoul? Check it again. Then check it again.
Keep calling get_current_time until the time is 3am in Seoul.
Notice which condition catches them. Not the ceiling — condition 3, on the second call, because the model asked for the identical thing twice running. Condition 2 would have caught it too, three calls later and three API calls more expensive. That gap is the entire reason condition 3 exists.

The obvious prompt does not work. "Keep checking the time until it is yesterday" sounds unsatisfiable, and it is — but the model checks once and answers anyway. An impossible goal is not the same as a loop that cannot progress. Worth knowing before you go looking for a runaway that never comes.

What to submit
The script, plus a transcript showing a loop stopped by each of the three conditions — including which one fired.

You're done when
You have three transcripts, and each one names which condition stopped it
The no-progress check fires on the second model call, before the ceiling ever gets near
An unsatisfiable prompt terminates instead of running until you kill it
A timeout is set explicitly, and you can say why backoff would be wrong here
If one of those is not true, the exercise is not finished — and the gap is where the lesson is.

Grading — 25 points
Criterion	Points
Loop handles multiple sequential tool calls	8
All three stopping conditions implemented	12
Explicit request timeout set	2
Terminates gracefully on an unsatisfiable prompt	3
Deduction: no iteration ceiling, −25. This is the one that costs someone a laptop.