# Local Development

1. Copy `.env.example` to `.env`.
2. Start dependencies with `docker compose up postgres livekit`.
3. Install dependencies with `pip install -r requirements.txt`.
4. Start the API with `uvicorn app.main:app --reload`.
5. Open `web/index.html` for a basic intake demo.

