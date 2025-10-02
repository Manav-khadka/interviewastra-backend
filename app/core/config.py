from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    gemini_api_key: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Testing configuration
    testing_mode: bool = True  # Set to False in production
    default_test_user_email: str = "manav@test.com"
    default_test_user_password: str = "manav123"
    default_test_user_name: str = "Manav"
    
    # Add other settings as needed

    class Config:
        env_file = ".env"

settings = Settings()