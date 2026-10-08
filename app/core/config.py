from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    APP_NAME: str = "Agentic Fact Checking System"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.8-flash"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    RETRIEVAL_TOP_K: int = 5

    DATA_DIR: str = "data"
    VECTOR_DB_DIR: str = "data/vector_db"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def project_root(self) -> Path:
        return BASE_DIR

    @property
    def data_path(self) -> Path:
        return BASE_DIR / self.DATA_DIR

    @property
    def vector_db_path(self) -> Path:
        return BASE_DIR / self.VECTOR_DB_DIR

    @property
    def logs_path(self) -> Path:
        return BASE_DIR / "logs"


settings = Settings()
