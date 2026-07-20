from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "OmniAssist AI"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    HOST: str = "127.0.0.1"

    PORT: int = 8000

    # SQLite gives contributors a persistent local database out of the box.
    # Production deployments override this with a PostgreSQL URL in backend/.env.
    DATABASE_URL: str = "sqlite:///./omniassist.db"

    # ---------- LLM Configuration ----------

    LLM_PROVIDER: str = "openrouter"

    OPENROUTER_API_KEY: str = ""

    OPENROUTER_MODELS: str = ""

    # ---------- Authentication -----------

    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    UPLOAD_DIRECTORY: str = "backend/uploads"

    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
    )


settings = Settings()
