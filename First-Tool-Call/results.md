### PASS 1:
```
$ python First-Tool-Call/agent.py
[sent]   messages=1
[recv]   finish_reason=tool_calls
[tool]   get_weather({'city': 'Seoul'})
[result] Seoul: 7C, light rain
[sent]   messages=3
[recv]   finish_reason=stop
The weather in Seoul is 7°C with light rain.
```
---
