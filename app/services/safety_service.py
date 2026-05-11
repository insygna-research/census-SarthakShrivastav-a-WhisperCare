from __future__ import annotations

from app.core.config import get_settings


def detect_risk(text: str, scores: dict | None = None) -> dict:
    settings = get_settings()
    lowered = text.lower()
    crisis_hit = next((word for word in settings.safety.crisis_keywords if word in lowered), None)
    urgent_hit = next((word for word in settings.safety.urgent_symptom_keywords if word in lowered), None)
    item9_score = (scores or {}).get("phq9_item9", 0)

    if crisis_hit or item9_score:
        return {
            "risk_level": "crisis",
            "need_human": True,
            "signal": crisis_hit or "phq9_item9",
            "response": settings.safety.crisis_response,
        }
    if urgent_hit:
        return {
            "risk_level": "urgent",
            "need_human": True,
            "signal": urgent_hit,
            "response": settings.safety.urgent_response,
        }
    return {"risk_level": "low", "need_human": False, "signal": None, "response": None}

