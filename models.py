from typing import List, Dict
import openai


class ModelInterface:
    def chat_completion(self, messages: List[Dict]) -> str:
        pass

    def image_generation(self, prompt: str) -> str:
        pass


class OpenAIModel(ModelInterface):
    def __init__(self, api_key: str, model_engine: str, image_size: str = '512x512'):
        openai.api_key = api_key
        self.model_engine = model_engine
        self.image_size = image_size

    def chat_completion(self, prompt):
        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt[1]['content'],
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def image_generation(self, prompt: str) -> str:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=self.image_size
        )
        image_url = response.data[0].url
        return image_url
