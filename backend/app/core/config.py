from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    env: str = Field("local", env="ENV")
    database_url: str = Field(..., env="DATABASE_URL")
    firebase_project_id: str = Field("prompt-wars-project-3", env="FIREBASE_PROJECT_ID")
    gemini_api_key: str = Field("placeholder_key", env="GEMINI_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
