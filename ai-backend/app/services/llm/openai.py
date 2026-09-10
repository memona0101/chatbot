from openai import AsyncOpenAI

from app.core.config import settings
from app.services.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured")

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )

    async def generate(
        self,
        *,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> str:

        response = await self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                *messages,
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("LLM returned an empty response")

        return content.strip()