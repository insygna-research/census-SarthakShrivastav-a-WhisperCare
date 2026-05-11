# Local Development

1. Copy `.env.example` to `.env`.
2. Start the full stack with `docker compose up --build`.
3. For API-only development, start dependencies with `docker compose up postgres livekit`.
4. Install dependencies with `pip install -r requirements.txt`.
5. Start the API with `uvicorn app.main:app --reload`.
6. Open `web/index.html` for a basic intake demo.

