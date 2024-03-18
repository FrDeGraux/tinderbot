import requests

def ask_chatgpt4(question, api_key):
    model = "gpt-4"  # Replace with the correct ChatGPT-4 model identifier if different
    url = f"https://api.openai.com/v1/models/{model}/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": question,
        "temperature": 0.7,
        "max_tokens": 150,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['text'].strip()
    else:
        return f"Error: {response.status_code}, {response.text}"

API_KEY = "Your_OpenAI_API_Key_Here"  # Replace with your actual OpenAI API key
question = "What is the capital of France?"

# Send the question to ChatGPT-4 and print the response
response = ask_chatgpt4(question, API_KEY)
print(response)
