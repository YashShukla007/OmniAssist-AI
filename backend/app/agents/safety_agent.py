from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    should_escalate: bool
    reason: str | None = None


class SafetyEscalationAgent:
    """Blocks medical decision-making and flags urgent/sensitive requests for people."""

    system_prompt = "You are the Safety and Escalation Agent. You never diagnose, prescribe, or triage. Escalate urgent or medication-related requests to a human."
    unsafe_terms = (
        "chest pain",
        "heart attack",
        "stroke",
        "cannot breathe",
        "can't breathe",
        "severe bleeding",
        "unconscious",
        "suicid",
        "overdose",
        "dosage",
        "medication",
        "medicine",
        "prescribe",
        "diagnose",
        "treatment",
        "emergency",
    )

    def assess(self, request_text: str) -> SafetyDecision:
        normalised = request_text.lower()
        matched = next((term for term in self.unsafe_terms if term in normalised), None)
        if matched is None:
            return SafetyDecision(should_escalate=False)
        return SafetyDecision(should_escalate=True, reason=f"Human review required because the request contains sensitive term: {matched}.")


safety_agent = SafetyEscalationAgent()
