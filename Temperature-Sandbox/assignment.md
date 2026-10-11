Ex 1.6 — Temperature Sandbox
📌 worth
20 points
· file
Intermediate · 1 hour

What you're building
You have read what temperature does. Now measure it on your own machine, because a number you produced yourself is worth more than one you were handed.

Run the same prompt 50 times at temperature=0.0, then 50 more at 1.2, and quantify how much the output moved.

Choose the prompt carefully
Pick something with a short, checkable answer. "Name three cities in Japan" beats "write me a poem" — you can count how often the set of three changes, rather than squinting at two poems and deciding whether they are meaningfully different.

That choice is not a convenience, it is the lesson underneath the exercise: measuring non-determinism requires something countable. Part 7 will ask you to write tests against this same model, and it runs into the same wall.

What to measure
For each temperature, at minimum:

how many distinct responses came back across the 50 runs
how many runs matched the single most common response
from collections import Counter

counts = Counter(responses)
print(f"distinct   : {len(counts)} / {len(responses)}")
print(f"most common: seen {counts.most_common(1)[0][1]} times")
Then do it again with a tool attached
Repeat the 1.2 run, but declare your Exercise 1.3 get_weather tool and ask "What's the weather in Seoul?". Count how many of the 50 runs actually came back with finish_reason == "tool_calls".

The concept module quotes 5 out of 6 from a small sample. Fifty runs will give you a tighter number — and that number is your harness's real failure rate at that setting. Write it down. It is the most useful thing you will produce today.

What to submit
Your script, your two sets of counts, and one paragraph answering this: at what temperature would you run an agent that calls tools, and what did you measure that convinced you?

You're done when
Two sets of counts, 50 runs each, not two impressions
At temperature=0 you get one distinct response; at 1.2 you get several
You have a tool-call rate at 1.2 — a real number, from your machine, that is your harness's failure rate at that setting
You can say which temperature you would run an agent at, and cite your own measurement for it
If one of those is not true, the exercise is not finished — and the gap is where the lesson is.

Grading — 20 points
Criterion	Points
50 runs at each temperature, both recorded	6
Variation quantified with counts, not described in prose	5
Tool-call rate measured at 1.2 over 50 runs	5
Written answer ties the setting to harness reliability	4
Note: at roughly 2–3 seconds per call, 150 calls is about seven minutes of waiting. Start the run, read the next module, come back.