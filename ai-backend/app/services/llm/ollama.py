from ollama import AsyncClient

from app.core.config import settings
from app.services.llm.base import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(self) -> None:
        self.client = AsyncClient(
            host=settings.ollama_base_url
        )

    async def generate(
        self,
        *,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> str:

        response = await self.client.chat(
            model=settings.ollama_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                *messages,
            ],
        )

        content = response.message.content

        if not content:
            raise RuntimeError("Ollama returned an empty response")

        return content.strip()