from backend.app.config.settings import settings

from backend.app.providers.openrouter_provider import OpenRouterProvider
from backend.app.providers.ollama_provider import OllamaProvider


class LLMManager:

    def __init__(self):

        if settings.LLM_PROVIDER == "openrouter":

            self.provider = OpenRouterProvider()

        elif settings.LLM_PROVIDER == "ollama":

            self.provider = OllamaProvider()

        else:

            raise ValueError(
                f"Unsupported provider: {settings.LLM_PROVIDER}"
            )

    async def generate(
        self,
        prompt,
        domain,
    ):

        return await self.provider.generate(
            prompt,
            domain,
        )


llm_manager = LLMManager()