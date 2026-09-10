from app.db.database import SessionLocal
from app.services.retriever import (
    retrieve,
    build_context,
    retrieval_debug,
)


def main():
    query = "How much does a custom website cost?"

    print("Starting retrieval test...")

    db = SessionLocal()

    try:
        results = retrieve(
    db=db,
    query=query,
    category="pricing",
    threshold=0.0,
)
        

        print("=" * 70)
        print("QUERY")
        print("=" * 70)
        print(query)

        print("\n" + "=" * 70)
        print("RETRIEVAL DEBUG")
        print("=" * 70)

        debug_results = retrieval_debug(results)

        if not debug_results:
            print("NO RESULTS ABOVE THRESHOLD")

        for item in debug_results:
            print(
                f"ID={item['id']} | "
                f"Score={item['score']} | "
                f"Title={item['title']} | "
                f"Category={item['category']}"
            )

        print("\n" + "=" * 70)
        print("RESULT COUNT")
        print("=" * 70)
        print(len(results))

        print("\n" + "=" * 70)
        print("CONTEXT")
        print("=" * 70)

        context = build_context(results)

        if context:
            print(context)
        else:
            print("NO CONTEXT")

    finally:
        db.close()


if __name__ == "__main__":
    main()