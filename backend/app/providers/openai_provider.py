from backend.app.providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):

    async def generate(
        self,
        prompt: str,
        domain: str,
    ) -> dict:

        return {
            "answer": "OpenAI Provider",
            "confidence": 1.0,
            "model": "OpenAI",
        }