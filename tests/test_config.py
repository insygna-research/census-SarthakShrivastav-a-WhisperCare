from app.core.config import get_settings


def test_config_loads():
    settings = get_settings()
    assert settings.app.name == "WhisperCare"
    assert settings.livekit.agent_name
    assert settings.docker.image_repository

