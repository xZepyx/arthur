import ollama

from providers.base import BaseProvider


class OllamaProvider(BaseProvider):
    def __init__(self, model="llama3"):
        self.model = model

    def chat(self, messages):
        response = ollama.chat(
            model=self.model,
            messages=messages
        )
        return response["message"]["content"]
