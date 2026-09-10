import asyncio

from app.db.database import SessionLocal
from app.services.retriever import retrieve
from app.services.prompts import (
    APPROVED_FALLBACK,
    build_system_prompt,
)
from app.services.llm.factory import get_llm_provider


async def main():
    query = "How much does a custom website cost?"

    print("Starting RAG + LLM test...")

    db = SessionLocal()

    try:
        # 1. Retrieve relevant knowledge
        results = retrieve(
            db=db,
            query=query,
            category="pricing",
            threshold=0.0,
        )

        print("=" * 70)
        print("RETRIEVED KNOWLEDGE")
        print("=" * 70)

        for index, result in enumerate(results, start=1):
            print(
                f"{index}. "
                f"{result.title} | "
                f"score={result.score:.4f}"
            )

        if not results:
            print("No relevant knowledge found.")
            print(APPROVED_FALLBACK)
            return

        # 2. Convert retrieval results to dictionaries
        knowledge_chunks = [
            {
                "content": result.content,
                "score": result.score,
                "document_id": result.id,
            }
            for result in results
        ]

        # 3. Build grounded system prompt
        system_prompt = build_system_prompt(
            knowledge_chunks=knowledge_chunks,
            intent="pricing",
            lead_state="unknown",
        )

        # 4. Get configured LLM provider
        provider = get_llm_provider()

        # 5. Generate final answer
        answer = await provider.generate(
            system_prompt=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
        )

        print("\n" + "=" * 70)
        print("FINAL ANSWER")
        print("=" * 70)
        print(answer)

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
    