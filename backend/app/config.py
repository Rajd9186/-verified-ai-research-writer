from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./verified_ai.db"
    ollama_base_url: str = "https://ollama.com"
    ollama_api_key: str = ""
    ollama_model: str = "nemotron-3-super:cloud"
    tavily_api_key: Optional[str] = None
    secret_key: str = "change-me-in-production"
    environment: str = "development"
    log_level: str = "INFO"

    api_v1_prefix: str = "/api/v1"
    project_name: str = "Verified AI Research Writer"
    project_version: str = "1.0.0"

    trusted_domains: list[str] = [
        "reuters.com",
        "who.int",
        "nasa.gov",
        "nih.gov",
        "cdc.gov",
        "un.org",
        "worldbank.org",
        "imf.org",
        "ieee.org",
        "acm.org",
        "nature.com",
        "science.org",
        "oxford.ac.uk",
        "cam.ac.uk",
        "harvard.edu",
        "mit.edu",
        "stanford.edu",
        "berkeley.edu",
    ]

    domain_trust_scores: dict[str, float] = {
        "reuters.com": 0.95,
        "who.int": 0.93,
        "nasa.gov": 0.95,
        "nih.gov": 0.94,
        "cdc.gov": 0.93,
        "un.org": 0.90,
        "worldbank.org": 0.92,
        "imf.org": 0.92,
        "ieee.org": 0.88,
        "acm.org": 0.87,
        "nature.com": 0.92,
        "science.org": 0.91,
        "harvard.edu": 0.90,
        "mit.edu": 0.90,
        "stanford.edu": 0.90,
        "cam.ac.uk": 0.88,
        "oxford.ac.uk": 0.88,
    }

    default_trust_score: float = 0.60
    high_trust_threshold: float = 0.85
    medium_trust_threshold: float = 0.70

    model_class: str = "pkl"
    max_retries: int = 3
    retry_delay: float = 1.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
