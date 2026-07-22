import logging

from openai import AsyncOpenAI, RateLimitError

from backend.app.config.settings import settings
from backend.app.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class OpenRouterProvider(BaseProvider):

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost:5173",
                "X-Title": settings.APP_NAME,
            },
        )

        self.models = [
            model.strip().replace("\\", "")
            for model in settings.OPENROUTER_MODELS.split(",")
            if model.strip().replace("\\", "")
        ]

        if not self.models:
            raise ValueError(
                "No OpenRouter models configured. Please set OPENROUTER_MODELS in backend/.env."
            )

    async def generate(
        self,
        prompt: str,
        domain: str,
    ) -> dict:

        last_error = None

        for model in self.models:

            try:

                logger.info("Trying OpenRouter model: %s", model)

                response = await self.client.chat.completions.create(

                    model=model,

                    messages=[

                        {
                            "role": "system",
                            "content": (
                                f"""
You are an expert {domain} assistant.

Always:

- Give accurate answers.
- Be professional.
- Explain clearly.
- Provide step-by-step guidance whenever appropriate.
- If you are unsure, say so instead of making up information.
"""
                            ),
                        },

                        {
                            "role": "user",
                            "content": prompt,
                        },

                    ],

                    temperature=0.7,
                    max_tokens=800,

                )

                answer = response.choices[0].message.content

                logger.info(
                    "OpenRouter response generated successfully using model: %s",
                    model,
                )

                return {

                    "answer": answer,

                    "confidence": 1.0,

                    "model": model,

                }

            except RateLimitError:

                logger.warning(
                    "Model '%s' hit the rate limit. Trying the next model.",
                    model,
                )

                continue

            except Exception as e:

                logger.warning(
                    "Model '%s' failed with error: %s",
                    model,
                    str(e),
                )

                last_error = str(e)

                continue

        logger.error(
            "All configured OpenRouter models failed. Last error: %s",
            last_error,
        )

        return {

            "answer": (
                "⚠️ The configured OpenRouter models are temporarily unavailable.\n\n"
                "This is usually caused by provider overload or temporary service interruptions.\n\n"
                "Please try again in a few moments."
            ),

            "confidence": 0.0,

            "model": "Unavailable",

            "error": last_error,

        }