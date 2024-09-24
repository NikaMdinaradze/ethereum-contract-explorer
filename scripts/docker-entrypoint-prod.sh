#!/bin/sh
set -e

echo "Running app with uvicorn"
uvicorn src.main:app --host 0.0.0.0 --port 8000

exec "$@"
