from openai import AsyncOpenAI

from app.core.config import settings
from app.services.llm.base import LLMProvider


class GeminiProvider(LLMProvider):

    def __init__(self) -> None:
        api_key = settings.gemini_api_key or settings.openai_api_key

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        # Google Gemini provides an OpenAI-compatible REST API endpoint
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        self.model = settings.gemini_model or "gemini-3.6-flash"

    async def generate(
        self,
        *,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
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
            raise RuntimeError("Gemini returned an empty response")

        return content.strip()
