# WhisperCare

**India-focused, voice-first healthcare workflow platform.**

WhisperCare is a FastAPI + LangGraph + LiveKit backend for patient onboarding, consent, voice-led intake, triage, clinician handoff, care planning, and ABDM/FHIR-ready exports. It is designed around Indian telehealth workflows, multilingual expansion, and config-driven deployment.

> WhisperCare is a healthcare workflow assistant. It is not a medical device, does not diagnose, does not prescribe, and does not replace a Registered Medical Practitioner.

## What It Does

- **Patient onboarding** with phone-first profile fields, emergency contact, language, and optional ABHA identifiers.
- **Consent capture** for telehealth and AI-assisted workflows with audit logging.
- **Voice-first intake** using LiveKit session provisioning and a worker bridge.
- **Mental-health screening** with PHQ-9 and GAD-7 style scoring from YAML configuration.
- **India safety routing** for urgent symptoms and crisis signals.
- **Clinician handoff** through intake summaries, appointments, visits, and care-plan foundations.
- **ABDM/FHIR-ready export preview** using FHIR-shaped Patient and QuestionnaireResponse resources.
- **Dockerized local stack** with API, Postgres, LiveKit, and voice-worker services.

## Architecture

```text
Browser / Mobile
      |
      | REST + LiveKit token
      v
FastAPI Backend -------------- PostgreSQL
      |                             |
      | LangGraph                   | audit, patients,
      v                             | intakes, visits
Intake / Triage Graph
      ^
      |
LiveKit Voice Worker <-------> LiveKit Server
      |
      | STT / TTS / LLM providers configured by YAML
      v
Patient voice session
```

Core services:

- `api`: FastAPI application.
- `postgres`: primary relational datastore.
- `livekit`: local LiveKit SFU for voice rooms.
- `voice-worker`: LiveKit/backend bridge. Current mode is a safe stub that stays alive and exposes configured runtime details.

## Tech Stack

| Area | Choice |
| --- | --- |
| API | FastAPI |
| Workflow orchestration | LangGraph |
| Voice transport | LiveKit |
| Database | PostgreSQL via async SQLAlchemy |
| Migrations | Alembic |
| Config | YAML + env-var references |
| Tests | Pytest |
| Container | Docker / Docker Compose |

## Quick Start

Clone and run the full stack:

```bash
git clone https://github.com/SarthakShrivastav-a/WhisperCare.git
cd WhisperCare
copy .env.example .env
docker compose up --build
```

Open:

- API health: `http://localhost:8000/api/health`
- Demo page: `web/index.html`
- LiveKit HTTP port: `http://localhost:7880`

Run locally without Docker:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:

```bash
python -m pytest -q
```

## Docker Image

The GitHub Actions workflow publishes Docker images to Docker Hub after merged pull requests.

Current image namespace:

```text
sarthak73/whispercare
```

Expected release tags:

```text
sarthak73/whispercare:latest
sarthak73/whispercare:main-<short_sha>
sarthak73/whispercare:dev-latest
sarthak73/whispercare:dev-<short_sha>
```

Required GitHub Actions secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

## Configuration Policy

All runtime values live in `config/app.yaml`.

Do not hardcode:

- model names
- provider names
- LiveKit agent names
- LiveKit URLs
- emergency numbers
- crisis response text
- scoring thresholds
- supported languages
- Docker image repositories
- API base URLs

Secrets are referenced by environment variable names in YAML, then resolved at runtime.

Important config files:

```text
config/app.yaml
config/livekit.dev.yaml
.env.example
docker-compose.yml
```

## API Overview

All routes are mounted under `/api`.

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health check |
| `POST` | `/patients` | Create patient profile |
| `GET` | `/patients/{patient_id}` | Read patient profile |
| `PATCH` | `/patients/{patient_id}` | Update patient profile |
| `POST` | `/consents` | Capture patient consent |
| `GET` | `/consents/{patient_id}` | List patient consents |
| `POST` | `/intake/sessions` | Start intake session |
| `PUT` | `/intake/sessions/{session_id}` | Advance intake graph |
| `GET` | `/intake/sessions/{session_id}` | Read intake session |
| `POST` | `/voice/connect` | Create LiveKit voice session token |
| `POST` | `/voice/disconnect` | Close voice session |
| `POST` | `/appointments` | Create appointment |
| `POST` | `/visits/summary` | Create visit summary |
| `GET` | `/abdm/export/{patient_id}` | Export FHIR-shaped bundle |

## India Safety Defaults

Configured emergency and crisis resources:

- National emergency: `112`
- Ambulance defaults: `108`, `102`
- Tele-MANAS: `14416`, `1-800-891-4416`
- KIRAN: `1800-599-0019`

Safety behavior:

- Crisis signals stop the regular intake path.
- Urgent cases are flagged for human review.
- AI responses include escalation guidance.
- The system prepares clinical context; it does not provide diagnosis or prescriptions.

## Project Layout

```text
app/
  api/              FastAPI routers
  core/             YAML config loader
  db/               async SQLAlchemy setup
  graphs/intake/    LangGraph intake flow
  livekit/          voice worker bridge
  models/           SQLAlchemy models
  schemas/          Pydantic schemas
  services/         business logic
config/
  app.yaml
  livekit.dev.yaml
docs/
tests/
web/
```

## Development Workflow

Branch model:

- `main`: release branch.
- `dev`: integration branch.
- `feature/*`: scoped work branches.

Preferred flow:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/my-change

# work, test, commit
python -m pytest -q

git push -u origin feature/my-change
gh pr create --base dev --head feature/my-change
gh pr merge --merge
```

Release flow:

```bash
gh pr create --base main --head dev --title "release: merge dev into main"
gh pr merge --merge
```

## Current Status

Implemented foundation:

- FastAPI backend shell
- YAML config loader
- async DB setup
- patient and consent modules
- intake graph
- PHQ-9/GAD-7 scoring
- India safety routing
- LiveKit connect/disconnect foundation
- Docker Compose stack with LiveKit
- ABDM/FHIR-style export preview

Next meaningful work:

- Replace voice-worker stub with full LiveKit `AgentSession` loop.
- Add real OTP/auth flow.
- Add Alembic generated migration revisions.
- Expand clinician dashboard APIs.
- Add production ABDM sandbox integration.
- Add provider-specific STT/TTS/LLM adapters.

## License

MIT. See `LICENSE`.
