from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI SaaS Backend"
    environment: str = "local"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./ai_saas.db"
    auto_create_tables: bool = True
    secret_key: str = Field(default="change-me-in-production", min_length=16)
    access_token_expire_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    ai_provider: str = "mock"
    ai_model: str = "gpt-4.1-mini"
    openai_api_key: str | None = None

    free_plan_monthly_credits: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
