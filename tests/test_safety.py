from app.services.safety_service import detect_risk


def test_crisis_detection():
    risk = detect_risk("I want to kill myself")
    assert risk["need_human"] is True
    assert risk["risk_level"] == "crisis"


def test_urgent_symptom_detection():
    risk = detect_risk("I have chest pain")
    assert risk["need_human"] is True
    assert risk["risk_level"] == "urgent"

