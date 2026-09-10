from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Backend"
    app_env: str = "local"

    database_url: str = "postgresql+psycopg://syedamemonazahra@localhost:5432/ai_backend"
    cors_origins: str = "*"
    openai_api_key: str | None = None
    openai_base_url: str | None = None

    # LLM provider settings
    llm_provider: str = "gemini"

    openai_model: str = "gpt-4o-mini"
    
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-5-haiku-latest"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.6-flash"
    
    # Email settings
    email_provider: str = "smtp"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    notification_email: str = "info@moinsystemsai.com"
    email_use_tls: bool = True
    email_max_retries: int = 3

    # Retrieval settings
    retrieval_top_k: int = 5
    retrieval_threshold: float = 0.35

    rag_top_k: int = 5
    rag_similarity_threshold: float = 0.40

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
settings = Settings()


