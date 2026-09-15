#!/bin/bash
set -e

DB_USER=$(docker compose exec -T postgres printenv POSTGRES_USER || echo "appuser")
DB_NAME=$(docker compose exec -T postgres printenv POSTGRES_DB || echo "appdb")

echo "Starting PostgreSQL backup..."
docker compose exec -T postgres pg_dump -U "$DB_USER" "$DB_NAME" > dump.sql
echo "[PASS] Database backup completed: dump.sql"
