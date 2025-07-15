from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/nextgen_tech"
    
    # Application
    APP_NAME: str = "NextGen Technologies Portal"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Scraping
    SCRAPING_INTERVAL_HOURS: int = 24
    MAX_ARTICLES_PER_SOURCE: int = 50
    REQUEST_DELAY: float = 1.0
    
    # Categories
    TECH_CATEGORIES: list = [
        "AI",
        "Quantum Computing", 
        "Defence Tech",
        "Space Tech",
        "Renewable Energy"
    ]
    
    class Config:
        env_file = ".env"

settings = Settings()