from __future__ import annotations

from app.core.config import get_settings


ANSWER_ALIASES = {
    "0": "not_at_all",
    "no": "not_at_all",
    "not at all": "not_at_all",
    "1": "several_days",
    "several": "several_days",
    "several days": "several_days",
    "2": "more_than_half",
    "more than half": "more_than_half",
    "half": "more_than_half",
    "3": "nearly_every_day",
    "nearly": "nearly_every_day",
    "every day": "nearly_every_day",
    "daily": "nearly_every_day",
}


def normalize_answer(text: str) -> str | None:
    lowered = text.strip().lower()
    for key, value in ANSWER_ALIASES.items():
        if key in lowered:
            return value
    return None


def score_tool(tool_name: str, answers: dict[str, str]) -> dict:
    settings = get_settings()
    tool = getattr(settings.screening, tool_name)
    total = sum(tool.answer_scores.get(value, 0) for value in answers.values())
    severity = "unknown"
    for label, bounds in tool.severity.items():
        if bounds[0] <= total <= bounds[1]:
            severity = label
            break
    return {"total": total, "severity": severity, "answered": len(answers)}

