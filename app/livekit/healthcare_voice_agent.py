from __future__ import annotations

import json
import os
import time

import httpx

from app.core.config import get_settings


async def send_turn_to_backend(intake_session_id: str, input_text: str, api_base_url: str) -> str:
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.put(
            f"{api_base_url}/intake/sessions/{intake_session_id}",
            json={"input_text": input_text, "source": "voice"},
        )
        response.raise_for_status()
        payload = response.json()
        return payload.get("assistant_text", "")


def main() -> None:
    settings = get_settings()
    runtime = {
        "agent_name": settings.livekit.agent_name,
        "llm_model": settings.ai_models.llm.model,
        "stt_model": settings.ai_models.stt.model,
        "tts_model": settings.ai_models.tts.model,
        "api_base_url": settings.app.api_base_url,
        "mode": os.getenv("WHISPERCARE_WORKER_MODE", "stub"),
    }
    print(json.dumps(runtime), flush=True)

    if runtime["mode"] == "stub":
        while True:
            time.sleep(settings.livekit.session_timeout_seconds)


if __name__ == "__main__":
    main()

