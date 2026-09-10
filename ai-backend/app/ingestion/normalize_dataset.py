import json
import re
from pathlib import Path

import openpyxl


DATASET = "data/MoinSystems_AI_Public_Chatbot_RAG_Dataset_v2 (1).xlsx"
SHEET = "RAG_Knowledge"

OUTPUT = "data/knowledge_base.jsonl"
DATASET_VERSION = "v2"


def clean_text(value):
    """Normalize whitespace without changing the meaning."""
    if value is None:
        return ""

    text = str(value).strip()

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing spaces from each line
    text = "\n".join(line.strip() for line in text.split("\n"))

    # Normalize excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_list(value):
    """Convert comma-separated tags/intents into a clean list."""
    if value is None:
        return []

    items = str(value).split(",")

    return [
        item.strip()
        for item in items
        if item.strip()
    ]


def normalize_dataset():
    workbook = openpyxl.load_workbook(
        DATASET,
        read_only=True,
        data_only=True,
    )

    if SHEET not in workbook.sheetnames:
        raise ValueError(f"Missing sheet: {SHEET}")

    sheet = workbook[SHEET]

    rows = sheet.iter_rows(values_only=True)
    headers = list(next(rows))

    header_indexes = {
        str(header).strip(): index
        for index, header in enumerate(headers)
        if header is not None and str(header).strip()
    }

    output_path = Path(OUTPUT)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    record_count = 0

    with output_path.open("w", encoding="utf-8") as output_file:

        for row in rows:

            # Ignore completely empty Excel rows
            if not any(
                value is not None and str(value).strip()
                for value in row
            ):
                continue

            record_id = clean_text(
                row[header_indexes["ID"]]
            )

            title = clean_text(
                row[header_indexes["Title"]]
            )

            category = clean_text(
                row[header_indexes["Category"]]
            )

            tags = clean_list(
                row[header_indexes["Tags"]]
            )

            intents = clean_list(
                row[header_indexes["Intents"]]
            )

            content = clean_text(
                row[header_indexes["Content"]]
            )

            embedding_text = clean_text(
                row[header_indexes["Embedding Text"]]
            )

            data_status = clean_text(
                row[header_indexes["Data Status"]]
            )

            source_basis = clean_text(
                row[header_indexes["Source Basis"]]
            )

            record = {
                "id": record_id,
                "title": title,
                "category": category,
                "tags": tags,
                "intents": intents,
                "content": content,
                "embedding_text": embedding_text,
                "metadata": {
                    "category": category,
                    "tags": tags,
                    "intents": intents,
                    "source": source_basis,
                    "version": DATASET_VERSION,
                    "record_id": record_id,
                    "data_status": data_status,
                },
            }

            output_file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

            record_count += 1

    print(f"Dataset version: {DATASET_VERSION}")
    print(f"Records normalized: {record_count}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    normalize_dataset()