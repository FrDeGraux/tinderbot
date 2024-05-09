API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
import os
from dotenv import load_dotenv
import requests

# System message
AI_SYSTEM_MESSAGE = "You are a helpful assistant"
load_dotenv('.env')

# Initialize message history with system message
API_KEY =os.getenv('OPENAPI_KEY')
import time
class ChatGPTCustom :

    def __init__(self) :
        self.message_history = [{"role": "system", "content": AI_SYSTEM_MESSAGE}]

    def invoke_chatgpt_sleep(self,message_history):

        return self.invoke_chatgpt(message_history)
    def invoke_chatgpt(self,message_history):
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
    def ask_to_gpt(self,question,n_alternatives = 1) :
        # Add new user prompt to² list of messages
        self.message_history.append({"role": "user", "content": question})

        # Query ChatGPT

        ai_response = [self.invoke_chatgpt(self.message_history) for idx in range((n_alternatives))]
        ai_response  = [item[:150] for item in ai_response]
        # Output response to a file and open it with the default text editor

        # Add ChatGPT response to list of messages
        self.message_history.append({"role": "assistant", "content": ai_response[0]})
        return ai_response
