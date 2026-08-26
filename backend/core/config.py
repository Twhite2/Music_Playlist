from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROVIDER_API_KEY: str = ""
    PROVIDER_BASE_URL: str = "https://api.openai.com/v1"
    MODEL_NAME: str
    ENABLE_ENRICHMENT: bool = True
    USE_STUB_PROVIDER: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    REQUEST_TIMEOUT: int = 20

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
