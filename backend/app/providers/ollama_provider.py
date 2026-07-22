import httpx

from backend.app.config.settings import settings
from backend.app.providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Local LLM provider backed by Ollama (https://ollama.com).

    Setup:
        1. Install Ollama: https://ollama.com/download
        2. Pull a model:   ollama pull llama3
        3. In backend/.env set:
               LLM_PROVIDER=ollama
               OLLAMA_MODEL=llama3          # or mistral, phi3, gemma2, etc.
               OLLAMA_BASE_URL=http://localhost:11434
        4. Start the backend normally — no API key required.

    The provider calls the Ollama /api/generate REST endpoint and returns
    a response dict compatible with OpenRouterProvider.
    """

    def __init__(self) -> None:
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT_SECONDS

    async def generate(self, prompt: str, domain: str) -> dict:
        system_prompt = (
            f"You are an expert {domain} assistant for OmniAssist AI.\n"
            "Always:\n"
            "- Give accurate, professional answers.\n"
            "- Explain clearly and step-by-step when appropriate.\n"
            "- If you are unsure, say so instead of making up information.\n"
            "- Never diagnose, prescribe, or give dosage advice for medical conditions."
        )
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": full_prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 800,
                        },
                    },
                )
                response.raise_for_status()
                data = response.json()
                answer = data.get("response", "").strip()
                if not answer:
                    raise ValueError("Empty response from Ollama.")
                return {
                    "answer": answer,
                    "confidence": 1.0,
                    "model": f"ollama/{self.model}",
                }

        except httpx.ConnectError:
            return {
                "answer": (
                    f"⚠️ Could not connect to Ollama at `{self.base_url}`.\n\n"
                    "Make sure Ollama is running: open a terminal and run `ollama serve`.\n"
                    f"Then pull your chosen model: `ollama pull {self.model}`."
                ),
                "confidence": 0.0,
                "model": "Unavailable",
                "error": "Ollama server not reachable.",
            }

        except httpx.TimeoutException:
            return {
                "answer": (
                    f"⚠️ Ollama timed out after {self.timeout}s.\n\n"
                    "The model may still be loading. Try again in a moment, "
                    "or increase `OLLAMA_TIMEOUT_SECONDS` in `backend/.env`."
                ),
                "confidence": 0.0,
                "model": "Unavailable",
                "error": "Ollama request timed out.",
            }

        except Exception as exc:
            return {
                "answer": (
                    "⚠️ An unexpected error occurred while calling the local Ollama model.\n\n"
                    f"Details: {exc}"
                ),
                "confidence": 0.0,
                "model": "Unavailable",
                "error": str(exc),
            }