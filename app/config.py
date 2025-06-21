from pydantic_settings import BaseSettings
from app.secrets_loader import get_database_url, get_google_client_id

class Settings(BaseSettings):
    DATABASE_URL: str = get_database_url()
    GOOGLE_CLIENT_ID: str = get_google_client_id()

settings = Settings()
