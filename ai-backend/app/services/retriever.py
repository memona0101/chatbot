from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.embedding import generate_embedding


@dataclass
class RetrievalResult:
    id: str
    title: str
    category: Optional[str]
    content: str
    tags: Optional[list]
    intents: Optional[list]
    score: float


def prepare_query(
    query: str,
    recent_context: Optional[list[str]] = None,
) -> str:
    """Normalize the query and include recent conversation context."""

    query = query.strip()
    query = re.sub(r"\s+", " ", query)

    if not recent_context:
        return query

    recent = recent_context[-2:]

    context_text = " ".join(
        item.strip()
        for item in recent
        if item and item.strip()
    )

    if not context_text:
        return query

    return f"{context_text} {query}".strip()


def retrieve(
    db: Session,
    query: str,
    recent_context: Optional[list[str]] = None,
    category: Optional[str] = None,
    intent: Optional[str] = None,
    top_k: Optional[int] = None,
    threshold: Optional[float] = None,
) -> list[RetrievalResult]:
    """Retrieve relevant knowledge using pgvector similarity."""

    prepared_query = prepare_query(
        query=query,
        recent_context=recent_context,
    )

    embedding = generate_embedding(prepared_query)

    k = (
        top_k
        if top_k is not None
        else settings.retrieval_top_k
    )

    min_score = (
        threshold
        if threshold is not None
        else settings.retrieval_threshold
    )

    k = max(1, min(k, 20))

    sql = """
        SELECT
            kd.record_id AS record_id,
            kd.title AS title,
            kd.category AS category,
            kc.text AS content,
            kd.metadata AS document_metadata,
            1 - (
                kc.embedding <=> CAST(:embedding AS vector)
            ) AS score
        FROM knowledge_chunk kc
        JOIN knowledge_document kd
            ON kd.id = kc.document_id
        WHERE kc.embedding IS NOT NULL
    """

    params = {
        "embedding": str(embedding),
        "top_k": k,
    }

    if category:
        sql += """
            AND LOWER(kd.category) = LOWER(:category)
        """
        params["category"] = category

    if intent:
        sql += """
            AND EXISTS (
                SELECT 1
                FROM jsonb_array_elements_text(
                    kd.metadata->'intents'
                ) AS intent_value
                WHERE LOWER(intent_value) = LOWER(:intent)
            )
        """
        params["intent"] = intent

    sql += """
        ORDER BY kc.embedding <=> CAST(:embedding AS vector)
        LIMIT :top_k
    """

    rows = db.execute(
        text(sql),
        params,
    ).mappings().all()

    results: list[RetrievalResult] = []

    for row in rows:
        score = float(row["score"])

        if score < min_score:
            continue

        metadata = row["document_metadata"] or {}

        results.append(
            RetrievalResult(
                id=str(row["record_id"]),
                title=row["title"],
                category=row["category"],
                content=row["content"],
                tags=metadata.get("tags"),
                intents=metadata.get("intents"),
                score=score,
            )
        )

    return deduplicate_results(results)


def deduplicate_results(
    results: list[RetrievalResult],
) -> list[RetrievalResult]:
    """Remove duplicate or near-identical results."""

    unique_results: list[RetrievalResult] = []
    seen_content: set[str] = set()

    for result in results:
        normalized_content = re.sub(
            r"\s+",
            " ",
            result.content.lower().strip(),
        )

        if normalized_content in seen_content:
            continue

        is_near_duplicate = False

        for existing in unique_results:
            existing_content = re.sub(
                r"\s+",
                " ",
                existing.content.lower().strip(),
            )

            if (
                normalized_content in existing_content
                or existing_content in normalized_content
            ):
                is_near_duplicate = True
                break

        if is_near_duplicate:
            continue

        seen_content.add(normalized_content)
        unique_results.append(result)

    return unique_results
def build_context(
    results: list[RetrievalResult],
) -> str:
    """Build a readable knowledge context from retrieval results."""

    if not results:
        return ""

    context_parts: list[str] = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"[Knowledge {index}]\n"
            f"Title: {result.title}\n"
            f"Category: {result.category or 'N/A'}\n"
            f"Content: {result.content}\n"
            f"Relevance: {result.score:.4f}"
        )

    return "\n\n".join(context_parts)


def retrieval_debug(
    results: list[RetrievalResult],
) -> list[dict]:
    """Return retrieval results in a debug-friendly format."""

    return [
        {
            "id": result.id,
            "title": result.title,
            "category": result.category,
            "score": round(result.score, 4),
        }
        for result in results
    ]