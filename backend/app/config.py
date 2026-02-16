from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:tirepro123@db:5432/tirepro"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    PORT: int = 8000
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
