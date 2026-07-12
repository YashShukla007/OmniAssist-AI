from openai import AsyncOpenAI, RateLimitError

from backend.app.config.settings import settings
from backend.app.providers.base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

        print("Loaded API Key:", settings.OPENROUTER_API_KEY[:15])

        self.models = [

            model.strip().replace("\\", "")

            for model in settings.OPENROUTER_MODELS.split(",")

            if model.strip().replace("\\", "")

        ]

        print("=" * 60)
        print("Configured OpenRouter Models")
        print("=" * 60)

        for model in self.models:
            print(repr(model))

        print("=" * 60)

    async def generate(
        self,
        prompt: str,
        domain: str,
    ) -> dict:

        last_error = None

        for model in self.models:

            try:

                print(f"\nTrying Model : {model}")

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

                print(f"Success : {model}")

                return {

                    "answer": answer,

                    "confidence": 1.0,

                    "model": model,

                }

            except RateLimitError:

                print(f"[OpenRouter] {model} is busy. Trying next model...")

                continue

            except Exception as e:

                last_error = str(e)

                print("=" * 60)
                print(f"Model Failed : {model}")
                print(f"Reason       : {last_error}")
                print("=" * 60)

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