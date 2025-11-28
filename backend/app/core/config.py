from functools import lru_cache
from typing import List, Literal

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "SIAD Agro API"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True

    backend_cors_origins: List[AnyHttpUrl] | str = ["http://localhost", "http://localhost:3000"]

    database_url: PostgresDsn = "postgresql+asyncpg://siad:siad@localhost:5432/siad"
    sync_database_url: PostgresDsn = "postgresql+psycopg://siad:siad@localhost:5432/siad"

    redis_url: str = "redis://localhost:6379/0"

    s3_endpoint: AnyHttpUrl | str = "http://localhost:9000"
    s3_bucket: str = "siad"
    s3_access_key: str = "siad"
    s3_secret_key: str = "siad-secret"
    storage_dir: str = "storage/uploads"

    jwt_secret: str = "change-me"
    jwt_refresh_secret: str = "change-me-too"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7

    otlp_endpoint: str = "http://localhost:4317"
    rate_limit_per_minute: int = 120

    default_locale: str = "pt-BR"

    class Config:
        env_file = ".env"

    @field_validator("backend_cors_origins")
    @classmethod
    def split_str(cls, v: List[AnyHttpUrl] | str) -> List[AnyHttpUrl] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
