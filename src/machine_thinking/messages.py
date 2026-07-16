# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from .utils import (query,
                    default_model,
                    get_function,
                    get_func_args,
                    call_function)


def get_weather(location):
    # print(f"Executing weather tool for location: {location}")
    return {"temperature": "72F", "condition": "Sunny"}


def message(messages=None, instructions=None, tools=None, **kwargs):
    """A continuation of text with a given context and instruction.
    """
    messages = kwargs.get('messages', messages)

    payload = {
        'model':                    kwargs.get('model', default_model),
        'system':                   kwargs.get('system', instructions),
        'messages':                 kwargs.get('messages', messages),
        'output_config':            kwargs.get('output_config',{'effort': 'high'}),
        'thinking':                 kwargs.get('thinking', {
                                                            'type': 'enabled',
                                                            'budget_tokens': 10000,
                                                            }),
        'tool_choice':              kwargs.get('tool_choice', {'type': 'auto', 'disable_parallel_tool_use': False}),
        'max_tokens':               kwargs.get('max_tokens', 4096),
        'prompt_truncate_len':      kwargs.get('prompt_truncate_len', 100000),
        'n':                        kwargs.get('n', 1),
        'top_p':                    kwargs.get('top_p', 0.9),
        'top_k':                    kwargs.get('top_k', 10),
        'stream':                   False
    }
    if tools:
        payload['tools'] = tools
        payload['parallel_tool_calls'] = True
        payload['tool_choice'] = 'auto'

    while True:
        result = query(payload, '/messages')
        completion_message = result['choices'][0]['message']
        messages.append(completion_message)
        thoughts = completion_message.get('reasoning_content', '')
        text = completion_message.get('content', '')
        function_calls = completion_message.get('tool_calls', [])

        if function_calls:
            # Call all requested functions and create response messages.
            for function_call in function_calls:
                call_id = function_call.get('id')
                func_def = function_call.get('function')
                func_name = func_def.get('name', '')

                # Look up tool by name in globals and caller frames
                func = get_function(func_name)
                func_args = get_func_args(func_def)
                result = call_function(func, func_args)

                tool_message = {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": result
                }
                messages.append(tool_message)
        else:
            break

    return thoughts, text


if __name__ == '__main__':
    ...
