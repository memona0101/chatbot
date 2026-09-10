from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        *,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> str:
        """Generate a response from the LLM provider."""
        raise NotImplementedError