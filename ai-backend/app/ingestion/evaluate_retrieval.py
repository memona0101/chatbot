from app.db.database import SessionLocal
from app.services.retriever import retrieve, retrieval_debug


EVALUATION_QUERIES = [
    {
        "name": "Company overview",
        "query": "What does MoinSystems AI do?",
        "expected_ids": ["company_001"],
    },
    {
        "name": "Services",
        "query": "What services does MoinSystems AI provide?",
        "expected_ids": ["company_001"],
    },
    {
        "name": "Web development",
        "query": "Do you build custom websites?",
        "expected_ids": ["service_001", "faq_001"],
    },
    {
        "name": "Pricing",
        "query": "How much does a custom website cost?",
        "expected_ids": ["pricing_001", "pricing_002"],
    },
    {
        "name": "Pricing policy",
        "query": "What is your pricing policy?",
        "expected_ids": ["pricing_001", "phase2_pricing_001"],
    },
    {
        "name": "Project timeline",
        "query": "How long does a website project take?",
        "expected_ids": ["timeline_001"],
    },
    {
        "name": "AI services",
        "query": "Do you provide AI agents and chatbots?",
        "expected_ids": ["company_001"],
    },
    {
        "name": "E-commerce",
        "query": "Can you build an e-commerce website?",
        "expected_ids": ["service_001"],
    },
    {
        "name": "Unknown",
        "query": "Can you repair my refrigerator?",
        "expected_ids": [],
    },
    {
        "name": "Out of scope",
        "query": "What is the weather in Lahore today?",
        "expected_ids": [],
    },
]


def evaluate_query(db, item):
    results = retrieve(
        db=db,
        query=item["query"],
    )

    debug = retrieval_debug(results)

    retrieved_ids = [result["id"] for result in debug]

    expected_ids = item["expected_ids"]

    if not expected_ids:
        passed = len(results) == 0
    else:
        passed = any(
            expected_id in retrieved_ids
            for expected_id in expected_ids
        )

    print("\n" + "=" * 70)
    print(item["name"])
    print("=" * 70)

    print("Query:")
    print(item["query"])

    print("\nExpected IDs:")
    print(expected_ids)

    print("\nRetrieved:")

    if not debug:
        print("NO RESULTS ABOVE THRESHOLD")
    else:
        for result in debug:
            print(
                f"ID={result['id']} | "
                f"Score={result['score']} | "
                f"Title={result['title']} | "
                f"Category={result['category']}"
            )

    print("\nSTATUS:", "PASS" if passed else "FAIL")

    return passed


def main():
    print("Starting retrieval evaluation...")

    db = SessionLocal()

    try:
        passed = 0
        failed = 0

        for item in EVALUATION_QUERIES:
            result = evaluate_query(db, item)

            if result:
                passed += 1
            else:
                failed += 1

        total = passed + failed

        print("\n" + "=" * 70)
        print("EVALUATION SUMMARY")
        print("=" * 70)

        print(f"Total queries : {total}")
        print(f"Passed        : {passed}")
        print(f"Failed        : {failed}")

        if total:
            accuracy = (passed / total) * 100
            print(f"Accuracy      : {accuracy:.1f}%")

        print("=" * 70)

    finally:
        db.close()


if __name__ == "__main__":
    main()