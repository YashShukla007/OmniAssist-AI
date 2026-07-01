from huggingface_hub import InferenceClient

from backend.app.config.settings import settings
from backend.app.providers.base_provider import BaseProvider


class HuggingFaceProvider(BaseProvider):

    def __init__(self):

        self.client = InferenceClient(
            api_key=settings.HF_API_TOKEN,
        )

    async def generate(
        self,
        prompt: str,
        domain: str,
    ) -> dict:

        messages = [
            {
                "role": "system",
                "content": (
                    f"You are an expert assistant for the {domain} domain."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        response = self.client.chat.completions.create(
            model=settings.HF_MODEL,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "confidence": 1.0,
            "model": settings.HF_MODEL,
        }