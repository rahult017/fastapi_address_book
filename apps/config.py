import os
from pydantic_settings import BaseSettings
from pydantic import SecretStr

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Address Service API")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./addresses.db")
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    VERSION: str = os.getenv("VERSION", "1.0.0")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DEBUG: bool = os.getenv("DEBUG", False)
    RELOAD: bool = os.getenv("DEBUG", True)
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = os.getenv("PORT", 8000)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
