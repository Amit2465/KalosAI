from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_CLIENT_ID: str

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
