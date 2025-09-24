import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt for the AI
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Write a Python function that reverses a string."}
]

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # cheaper GPT-4 variant
        messages=messages,
        temperature=0.3,       # deterministic output
        max_tokens=100          # enough for a small function
    )

    # Print AI response
    print("=== AI Response ===")
    print(response.choices[0].message.content)

except Exception as e:
    print("Error communicating with OpenAI API:", e)
