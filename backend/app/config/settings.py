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
    # Choose "openrouter" (cloud) or "ollama" (local, fully offline).
    LLM_PROVIDER: str = "openrouter"

    # --- OpenRouter (cloud) ---
    OPENROUTER_API_KEY: str = ""

    # OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    # OPENROUTER_MODEL: str = "openrouter/free"

    OPENROUTER_MODELS: str = ""

    # --- Ollama (local model) ---
    # Install Ollama from https://ollama.com, pull a model (e.g. `ollama pull llama3`),
    # then set LLM_PROVIDER=ollama in backend/.env to run fully offline.
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    # Large local models can be slow — increase this if you get timeouts.
    OLLAMA_TIMEOUT_SECONDS: int = 120

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
