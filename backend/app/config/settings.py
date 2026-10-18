from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    database_url: str
    groq_api_key: str
    model_name: str = "openai/gpt-oss-120b"

    # "llm": the LLM selects the tool, keywords are the fallback.
    # "keyword": keyword rules only (offline development, debugging).
    router_mode: str = "llm"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()