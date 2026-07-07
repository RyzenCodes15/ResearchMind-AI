from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ResearchMind AI"
    APP_DESCRIPTION: str = (
        "AI Research Assistant using Retrieval-Augmented Generation (RAG)"
    )
    APP_VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
