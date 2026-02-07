from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Address Book"
    DATABASE_URL: str = "sqlite:///./addresses.db"
    BACKEND_CORS_ORIGINS: list = ["*"]
    LOG_LEVEL: str = "INFO"
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
