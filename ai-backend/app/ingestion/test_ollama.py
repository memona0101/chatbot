import asyncio

from app.services.llm.factory import get_llm_provider


async def main():
    provider = get_llm_provider()

    answer = await provider.generate(
        system_prompt="You are a helpful assistant.",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence.",
            }
        ],
    )

    print("=" * 70)
    print("OLLAMA TEST")
    print("=" * 70)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())