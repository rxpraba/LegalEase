#!/usr/bin/env bash
# Starts backend (port 8000) and frontend (port 8501)
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

if [ -f "$DIR/.venv/bin/activate" ]; then
    source "$DIR/.venv/bin/activate"
elif [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
fi

uvicorn legalEaseAPI.main:app --reload --port 8000 &
BACK=$!
trap "kill $BACK 2>/dev/null || true" EXIT

streamlit run frontend/app.py

