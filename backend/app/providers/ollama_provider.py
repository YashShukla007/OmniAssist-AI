from backend.app.providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    async def generate(
        self,
        prompt: str,
        domain: str,
    ) -> dict:

        return {
            "answer": "Ollama Provider",
            "confidence": 1.0,
            "model": "Ollama",
        }