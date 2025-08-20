import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt
from call_functions import call_function, available_functions

MODEL = 'gemini-2.0-flash-001'
MAX_ITERATIONS = 20

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) < 2:
    print("Please provide a prompt")
    exit(1)

prompt = sys.argv[1]
is_verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

messages = [
    types.Content(
        parts = [types.Part(text=prompt)],
        role="user"
    )
]

client = genai.Client(api_key=api_key)

def generate_content(client, messages, is_verbose):
    resp = client.models.generate_content( 
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if is_verbose and resp.usage_metadata:
        print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")

    if resp.candidates:
        for candidate in resp.candidates:
            function_call_content = candidate.content
            if function_call_content:
                messages.append(function_call_content)

    if not resp.function_calls:
        return resp.text

    function_responses: list[types.Part] = []
    for function_call_part in resp.function_calls:
        result = call_function(function_call_part, is_verbose)
        if not result:
            raise Exception(f"no result from calling \"{function_call_part.name}\" with args \"{function_call_part.args}\"")

        if (
            not result.parts
            or not result.parts[0].function_response
        ):
            raise Exception("empty function call result")

        if is_verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))

i = 0
while True:
    i += 1
    if i > MAX_ITERATIONS:
        print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
        sys.exit(1)
    try:
        final_response = generate_content(client, messages, is_verbose)
        if final_response:
            print("Final response:")
            print(final_response)
            break
    except Exception as e:
        print(f"Error in generate_content: {e}")