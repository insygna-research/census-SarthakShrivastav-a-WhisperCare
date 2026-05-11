from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import os
from typing import Any

import yaml
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    name: str
    version: str
    description: str
    api_prefix: str
    environment: str
    api_base_url_env: str
    default_api_base_url: str

    @property
    def api_base_url(self) -> str:
        return os.getenv(self.api_base_url_env, self.default_api_base_url)


class CorsSettings(BaseModel):
    allowed_origins: list[str]
    allow_credentials: bool
    allowed_methods: list[str]
    allowed_headers: list[str]


class DatabaseSettings(BaseModel):
    url_env: str
    default_url: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    @property
    def url(self) -> str:
        return os.getenv(self.url_env, self.default_url)


class LiveKitSettings(BaseModel):
    url_env: str
    api_key_env: str
    api_secret_env: str
    agent_name: str
    room_prefix: str
    empty_timeout_seconds: int
    max_participants: int
    session_timeout_seconds: int

    @property
    def url(self) -> str:
        return os.getenv(self.url_env, "")

    @property
    def api_key(self) -> str:
        return os.getenv(self.api_key_env, "")

    @property
    def api_secret(self) -> str:
        return os.getenv(self.api_secret_env, "")


class ModelProviderSettings(BaseModel):
    provider: str
    model: str
    api_key_env: str | None = None
    voice_id: str | None = None

    @property
    def api_key(self) -> str:
        if not self.api_key_env:
            return ""
        return os.getenv(self.api_key_env, "")


class AiModelSettings(BaseModel):
    llm: ModelProviderSettings
    stt: ModelProviderSettings
    tts: ModelProviderSettings


class LanguageSettings(BaseModel):
    default: str
    supported: list[str]


class IndiaEmergencySettings(BaseModel):
    national: str
    ambulance_primary: str
    ambulance_secondary: str


class IndiaMentalHealthSettings(BaseModel):
    tele_manas: list[str]
    kiran: str


class IndiaSettings(BaseModel):
    default_country: str
    default_state: str
    emergency: IndiaEmergencySettings
    mental_health: IndiaMentalHealthSettings


class SafetySettings(BaseModel):
    crisis_keywords: list[str]
    urgent_symptom_keywords: list[str]
    crisis_response: str
    urgent_response: str


class ScreeningToolSettings(BaseModel):
    answer_scores: dict[str, int]
    severity: dict[str, tuple[int, int]]
    questions: list[str]


class ScreeningSettings(BaseModel):
    phq9: ScreeningToolSettings
    gad7: ScreeningToolSettings


class DockerSettings(BaseModel):
    image_repository: str
    dev_tag_prefix: str


class Settings(BaseModel):
    app: AppSettings
    cors: CorsSettings
    database: DatabaseSettings
    livekit: LiveKitSettings
    ai_models: AiModelSettings
    languages: LanguageSettings
    india: IndiaSettings
    safety: SafetySettings
    screening: ScreeningSettings
    docker: DockerSettings
    raw: dict[str, Any] = Field(default_factory=dict)


def _config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "config" / "app.yaml"


def load_settings() -> Settings:
    path = _config_path()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    settings = Settings(**data, raw=data)
    _validate_settings(settings)
    return settings


def _validate_settings(settings: Settings) -> None:
    required_sections = [
        settings.app,
        settings.database,
        settings.livekit,
        settings.ai_models,
        settings.india,
        settings.safety,
        settings.screening,
        settings.docker,
    ]
    if any(section is None for section in required_sections):
        raise ValueError("Missing required configuration section")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()

