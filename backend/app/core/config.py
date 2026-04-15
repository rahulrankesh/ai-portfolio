from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Vedra API"
    api_prefix: str = "/api/v1"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    youtube_api_key: str | None = None
    google_cse_api_key: str | None = None
    google_cse_id: str | None = None
    unsplash_api_key: str | None = None
    redis_url: str | None = None
    default_model_timeout_seconds: float = Field(default=20.0, ge=5.0, le=120.0)
    cache_ttl_seconds: int = Field(default=300, ge=30)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
