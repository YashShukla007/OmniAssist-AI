from openai import AsyncOpenAI, RateLimitError

from backend.app.config.settings import settings
from backend.app.providers.base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

        self.models = [

            model.strip().replace("\\", "")

            for model in settings.OPENROUTER_MODELS.split(",")

            if model.strip().replace("\\", "")

        ]

    async def generate(
        self,
        prompt: str,
        domain: str,
    ) -> dict:

        last_error = None

        for model in self.models:

            try:

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

                return {

                    "answer": answer,

                    "confidence": 1.0,

                    "model": model,

                }

            except RateLimitError:

                continue

            except Exception as e:

                last_error = str(e)

                continue

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
