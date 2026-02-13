"""
Demo: Using Offline Coding Models with EPI Recorder
"""

from openai import OpenAI
from epi_recorder import record, wrap_openai

# Connect to local Ollama instance
client = wrap_openai(OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # API key is required but ignored by Ollama
))

print("[INFO] Using model: qwen2.5-coder:7b")
print("[INFO] Recording to: epi-recordings/offline_coding_demo.epi")

with record("offline_coding_demo.epi", goal="Generate fibonacci function"):
    response = client.chat.completions.create(
        model="qwen2.5-coder:7b",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Write a recursive Python function to calculate the nth Fibonacci number."}
        ]
    )
    
    print("\n" + "="*50)
    print("AI RESPONSE:")
    print("="*50)
    print(response.choices[0].message.content)
    print("="*50)

print("\n[SUCCESS] Done! Recording saved and signed.")
