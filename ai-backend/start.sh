#!/usr/bin/env bash
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Seeding knowledge base..."
python -m app.ingestion.load_knowledge || true

echo "Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
