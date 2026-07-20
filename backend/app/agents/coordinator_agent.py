from dataclasses import dataclass

from backend.app.config.settings import settings
from backend.app.services.llm_manager import llm_manager


@dataclass(frozen=True)
class CoordinationPlan:
    administrative_summary: str


class CoordinatorAgent:
    """Creates a bounded administrative plan before delegating to specialist agents."""

    system_prompt = "You are the Coordinator Agent for healthcare administration. Plan routing, appointment, document, reminder, and escalation steps only. Never diagnose, prescribe, or give dosage advice."

    async def plan(self, request_text: str) -> CoordinationPlan:
        if settings.OPENROUTER_API_KEY and settings.OPENROUTER_MODELS:
            result = await llm_manager.generate(prompt=f"{self.system_prompt}\n\nPatient request: {request_text}\n\nReturn a short administrative coordination summary.", domain="Healthcare")
            if result.get("model") != "Unavailable" and result.get("answer"):
                return CoordinationPlan(administrative_summary=result["answer"].strip())
        return CoordinationPlan(administrative_summary=f"Administrative coordination requested for: {request_text.strip()}")


coordinator_agent = CoordinatorAgent()
