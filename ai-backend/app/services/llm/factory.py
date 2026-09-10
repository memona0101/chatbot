from app.core.config import settings
from app.services.llm.base import LLMProvider


def get_llm_provider() -> LLMProvider:

    provider = settings.llm_provider.lower().strip()

    if provider == "openai":
        from app.services.llm.openai import OpenAIProvider

        return OpenAIProvider()

    if provider == "claude":
        from app.services.llm.claude import ClaudeProvider

        return ClaudeProvider()
    
    if provider == "gemini":
        from app.services.llm.gemini import GeminiProvider

        return GeminiProvider()

    if provider == "ollama":
        from app.services.llm.ollama import OllamaProvider

        return OllamaProvider()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )
    