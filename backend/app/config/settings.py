from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "OmniAssist AI"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    HOST: str = "127.0.0.1"

    PORT: int = 8000

    DATABASE_URL: str = ""

    # ---------- LLM Configuration ----------

    LLM_PROVIDER: str = "openrouter"

    OPENROUTER_API_KEY: str = ""

    OPENROUTER_MODELS: str = ""

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
    )


settings = Settings()