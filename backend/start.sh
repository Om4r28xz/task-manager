#!/bin/bash
# Render startup script for the backend

echo "Starting Task Manager Backend..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
