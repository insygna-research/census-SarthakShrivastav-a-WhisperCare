# WhisperCare

WhisperCare is an India-focused, voice-first healthcare workflow platform. It combines FastAPI, LangGraph, LiveKit, and PostgreSQL to support patient onboarding, consent, intake, triage, doctor handoff, care planning, and ABDM/FHIR-ready exports.

The current implementation is a foundation intended for portfolio-grade development. It is not a medical device and does not diagnose, prescribe, or replace a Registered Medical Practitioner.

## Local Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest
```

## Configuration

All runtime settings live in `config/app.yaml`. Python code must not hardcode model names, LiveKit agent names, emergency numbers, crisis text, scoring thresholds, Docker image names, or service URLs.

Secrets are referenced through environment variable names configured in YAML.

