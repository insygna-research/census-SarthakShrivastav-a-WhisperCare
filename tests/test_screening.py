from app.services.screening_service import normalize_answer, score_tool


def test_normalize_answer():
    assert normalize_answer("nearly every day") == "nearly_every_day"


def test_phq9_score():
    score = score_tool("phq9", {"phq9_0": "nearly_every_day", "phq9_1": "several_days"})
    assert score["total"] == 4

