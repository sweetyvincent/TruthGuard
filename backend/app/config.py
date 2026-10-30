from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name: str = "TruthGuard API"
    database_url: str = f"sqlite:///{ROOT / 'truthguard.db'}"
    upload_dir: str = str(ROOT / "data" / "uploads")
    max_upload_mb: int = 20
    chunk_size: int = 900
    chunk_overlap: int = 150
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
