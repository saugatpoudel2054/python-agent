import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt
from functions.get_files_info import available_functions

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
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    ),
)

if response and response.function_calls:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)
if is_verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
