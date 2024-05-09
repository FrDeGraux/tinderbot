import requests
import json
from datetime import datetime
import os

# Define API key and endpoint
API_KEY = "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"
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# System message
AI_SYSTEM_MESSAGE = "You are a helpful assistant"

# Initialize message history with system message
message_history = [{"role": "system", "content": AI_SYSTEM_MESSAGE}]

def invoke_chatgpt(message_history):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4",
        "messages": message_history,
        "max_tokens": 1000,
        "temperature": 0.7
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    response_json = response.json()
    return response_json['choices'][0]['message']['content']

# Main loop
while True:
    user_message = input("\nYou: ")

    # Check if user wants to exit or reset
    if user_message.lower() == "exit":
        break
    if user_message.lower() == "reset":
        # Reset the message history
        message_history = [{"role": "system", "content": AI_SYSTEM_MESSAGE}]
        print("Messages reset.")
        continue

    # Add new user prompt to list of messages
    message_history.append({"role": "user", "content": user_message})

    # Query ChatGPT
    ai_response = invoke_chatgpt(message_history)

    # Output response to a file and open it with the default text editor

    # Add ChatGPT response to list of messages
    message_history.append({"role": "assistant", "content": ai_response})
