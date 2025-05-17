#!/bin/bash
set -e

if [ "$ENVIRONMENT" = "development" ]; then
    echo "Running in development mode with reload..."
    exec uvicorn api.app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running in production mode..."
    exec uvicorn api.app.main:app --host 0.0.0.0 --port 8000
fi

