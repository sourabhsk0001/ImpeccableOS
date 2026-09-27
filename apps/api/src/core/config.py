from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application runtime configuration backed by environment variables."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    APP_NAME: str = "ImpeccableOS"
    PROJECT_VERSION: str = "1.0.0"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    SECRET_KEY: str = "default_secret_key_for_development_purposes_only"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres_secure_pass@localhost:5432/impeccable_os"
    SYNC_DATABASE_URL: str = "postgresql://postgres:postgres_secure_pass@localhost:5432/impeccable_os"

    # LLM & Embeddings
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS: int = 1536
    PRIMARY_LLM_MODEL: str = "gpt-4o-mini"
    REASONING_LLM_MODEL: str = "gpt-4o"

    # Web Research & Reranking
    TAVILY_API_KEY: str = ""
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    RERANKER_FALLBACK_THRESHOLD: float = 0.50

    # Mastery Engine Parameters
    DEFAULT_EMA_ALPHA: float = 0.30
    DEFAULT_MASTERY_THRESHOLD: float = 0.70


settings = Settings()
