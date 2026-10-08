### SCENARIO 1:
```
$ python First-Tool-Call/agent.py "What's the weather in Seoul, and what time is it there?"
[sent]   messages=1
[recv]   finish_reason=tool_calls
[tool]   get_weather({'city': 'Seoul'})
[result] Seoul, South Korea: 14.7C, precipitation 0.0mm
[tool]   get_current_time({'timezone': 'Asia/Seoul'})
[result] 2026-10-09 01:18:00 KST
[sent]   messages=4
[recv]   finish_reason=stop
The weather in Seoul is 14.7°C with no precipitation. It is currently 01:18:00 am on October 9, 2026 (KST).
```
---
### SCENARIO 2