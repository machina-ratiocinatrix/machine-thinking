# Machine thinking
Tinker API calls to Inkling model without dependencies.
<pre>
  pip install machine-thinking
</pre>
Then:
```Python
  # Python
from yaml import safe_load as yl
from machine_thinking.chat import chat_complete as cc

kwargs = """  # this is a string in YAML format
  max_tokens:   32000
  stop_sequences:
    - STOP
    - "\nTitle"
  temperature:  1.0
  top_k:        10
  top_p:        0.5
  reasoning_effort: high
"""

instruction = 'You are a helpful assistant. Do not use markdown or lists in your responses.'

weather_tool = """ # YAML definition of a function (old format)
  type: function
  function:
    name: get_weather
    description: Determine weather in a location
    parameters:
      type: object
      properties:
        location:
          type: string
          description: The city and state, e.g. San Francisco, CA
      additionalProperties: false
      required:
        - location
"""

tools = [yl(weather_tool)]

msgs = [{'role': 'user', 'content': 'What is the weather like in Chicago, IL and Paris, France?'}]

thoughts, text = cc(
    messages=msgs,
    instructions=instruction,
    tools=tools,
    **yl(kwargs)
)
```

