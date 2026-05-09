import os
from openai import OpenAI
from dotenv import load_dotenv

from providers.base import BaseProvider

load_dotenv()


class GroqProvider(BaseProvider):
    def __init__(self, model="llama-3.3-70b-versatile", api_key=None):
        self.model = model
        api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
        )

    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content
