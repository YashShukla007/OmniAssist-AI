from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.app.services.department_service import department_service


@dataclass(frozen=True)
class RoutingDecision:
    department: str
    confidence: float


class DepartmentRoutingAgent:
    """Maps administrative language to an existing department; it does not diagnose."""

    system_prompt = "You are the Department Routing Agent. Route only administrative requests to supported departments. Never infer a diagnosis."

    def route(self, db: Session, request_text: str) -> RoutingDecision:
        normalised = request_text.lower()
        departments = department_service.active_departments(db)
        by_normalised_name = {department.name.casefold(): department.name for department in departments}
        matched_department = next(
            (department.name for department in departments if department.name.casefold() in normalised),
            None,
        )
        if matched_department is not None:
            return RoutingDecision(department=matched_department, confidence=0.88)
        cardiology_terms = ("cardiology", "cardiologist", "ecg", "ekg", "heart follow-up")
        if any(term in normalised for term in cardiology_terms) and "cardiology" in by_normalised_name:
            return RoutingDecision(department=by_normalised_name["cardiology"], confidence=0.92)

        general_department = next(
            (department.name for department in departments if "general" in department.name.casefold() or "medicine" in department.name.casefold()),
            None,
        )
        if general_department is not None:
            return RoutingDecision(department=general_department, confidence=0.68)

        # A real active catalogue, not a fixed fallback, remains the safe
        # administrative destination when the request is ambiguous.
        return RoutingDecision(department=departments[0].name, confidence=0.35)


routing_agent = DepartmentRoutingAgent()
