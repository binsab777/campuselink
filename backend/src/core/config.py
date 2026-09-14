import os
from pydantic_settings import BaseSettings

DB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH = os.path.join(DB_DIR, "campuslink_test.db")

class Settings(BaseSettings):
    # Default to PostgreSQL (Docker). Use SQLite for local testing if Docker is unavailable.
    # DATABASE_URL: str = "postgresql://campuslink:campuslink_password@localhost:5432/campuslink_db"
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    
    AUTH_JWT_SECRET: str = "super-secret-key-change-in-production"
    AUTH_JWT_ALGORITHM: str = "HS256"
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AUTH_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
