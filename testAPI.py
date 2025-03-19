import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit()

client = genai.Client(api_key=api_key, http_options=types.HttpOptions(api_version='v1'))

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="What is the capital of France?"
    )
    print("API Response:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")