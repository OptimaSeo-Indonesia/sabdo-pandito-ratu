from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000"]
    log_level: str = "INFO"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "spr"
    postgres_user: str = "spr"
    postgres_password: str = "spr_secret"

    redis_host: str = "localhost"
    redis_port: int = 6379

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_default_model: str = "gpt-4-turbo"

    anthropic_api_key: str = ""
    anthropic_base_url: str = "https://api.anthropic.com"
    anthropic_default_model: str = "claude-3-opus-20240229"

    ollama_base_url: str = "http://localhost:11434"
    ollama_default_model: str = "llama3"

    embedding_dimension: int = 1536
    embedding_provider: str = "openai"

    model_config = {"env_prefix": "", "case_sensitive": False}


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
