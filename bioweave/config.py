
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./bioweave.db"  # fallback for quick demo
    benchling_api_token: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
