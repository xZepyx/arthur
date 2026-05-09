import os
import requests
from dotenv import load_dotenv

from providers.base import BaseProvider


load_dotenv()


class OpenRouterProvider(BaseProvider):
    def __init__(
        self,
        model="meta-llama/llama-3.3-70b-instruct",
        max_tokens=600,
        api_key=None
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OpenRouter API key required. Set OPENROUTER_API_KEY "
                "environment variable or pass api_key."
            )

    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )

        data = response.json()

        if response.status_code != 200:
            error_msg = (
                data.get("error", {}).get("message")
                or str(data)
            )
            raise Exception(
                f"OpenRouter error ({response.status_code}): {error_msg}"
            )

        return data["choices"][0]["message"]["content"]
