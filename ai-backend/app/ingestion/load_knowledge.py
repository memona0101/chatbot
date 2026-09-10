from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import delete

from app.db.database import SessionLocal
from app.db.models import KnowledgeDocument, KnowledgeChunk
from app.services.embedding import generate_embedding


DATASET_PATH = Path("data/knowledge_base.jsonl")


def load_dataset() -> list[dict]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    records = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            records.append(record)

    return records


def build_metadata(record: dict) -> dict:
    metadata = record.get("metadata", {})

    return {
        "category": record.get("category", ""),
        "tags": record.get("tags", []),
        "intents": record.get("intents", []),
        "source": metadata.get("source", ""),
        "version": metadata.get("version", "v2"),
        "record_id": record.get("id", ""),
        "data_status": metadata.get(
            "data_status",
            "cleaned_validated",
        ),
    }


def ingest() -> None:
    records = load_dataset()

    print(f"Records loaded from JSONL: {len(records)}")

    db = SessionLocal()

    try:
        # Clear existing knowledge data for a clean/repeatable load.
        db.execute(delete(KnowledgeChunk))
        db.execute(delete(KnowledgeDocument))
        db.commit()

        print("Existing knowledge data cleared.")

        documents_created = 0
        chunks_created = 0

        for index, record in enumerate(records, start=1):

            record_id = str(record["id"])
            title = str(record["title"])
            category = str(record["category"])
            content = str(record["content"])

            embedding_text = str(
                record.get("embedding_text")
                or content
            )

            metadata = build_metadata(record)

            document = KnowledgeDocument(
                record_id=record_id,
                title=title,
                category=category,
                content=content,
                metadata_=metadata,
            )

            db.add(document)
            db.flush()

            # Generate local 384-dimensional embedding.
            embedding = generate_embedding(embedding_text)

            if len(embedding) != 384:
                raise ValueError(
                    f"Embedding dimension mismatch for "
                    f"{record_id}: expected 384, "
                    f"got {len(embedding)}"
                )

            chunk = KnowledgeChunk(
                document_id=document.id,
                chunk_index=0,
                text=content,
                embedding=embedding,
                metadata_=metadata,
            )

            db.add(chunk)

            documents_created += 1
            chunks_created += 1

            if index % 10 == 0 or index == len(records):
                print(
                    f"Processed {index}/{len(records)} records"
                )

        db.commit()

        print()
        print("Knowledge ingestion PASSED")
        print(f"Documents inserted: {documents_created}")
        print(f"Chunks inserted: {chunks_created}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    ingest()
    
    