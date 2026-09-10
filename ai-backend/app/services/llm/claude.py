from anthropic import AsyncAnthropic

from app.core.config import settings
from app.services.llm.base import LLMProvider


class ClaudeProvider(LLMProvider):

    def __init__(self) -> None:
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured")

        self.client = AsyncAnthropic(
            api_key=settings.anthropic_api_key
        )

    async def generate(
        self,
        *,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> str:

        response = await self.client.messages.create(
            model=settings.anthropic_model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )

        if not response.content:
            raise RuntimeError("LLM returned an empty response")

        text_parts = [
            block.text
            for block in response.content
            if getattr(block, "type", None) == "text"
        ]

        content = "".join(text_parts).strip()

        if not content:
            raise RuntimeError("LLM returned an empty response")

        return content