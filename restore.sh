#!/bin/bash
set -e

DB_USER=$(docker compose exec -T postgres printenv POSTGRES_USER || echo "appuser")
DB_NAME=$(docker compose exec -T postgres printenv POSTGRES_DB || echo "appdb")

echo "Restoring PostgreSQL database..."
docker compose exec -T postgres psql -U "$DB_USER" "$DB_NAME" < dump.sql
echo "[PASS] Database restoration completed successfully!"
