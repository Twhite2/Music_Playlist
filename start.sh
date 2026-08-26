#!/usr/bin/env bash
# Starts the backend and frontend together for local development.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

if [ ! -f "$BACKEND_DIR/.env" ]; then
  echo "ERROR: backend/.env is missing." >&2
  echo "Copy backend/.env.example to backend/.env and fill in PROVIDER_API_KEY and MODEL_NAME, then run this script again." >&2
  exit 1
fi

PYTHON_BIN=python3
command -v python3 >/dev/null 2>&1 || PYTHON_BIN=python

if [ ! -d "$BACKEND_DIR/venv" ]; then
  echo "Creating backend virtual environment..."
  "$PYTHON_BIN" -m venv "$BACKEND_DIR/venv"
fi

if [ -f "$BACKEND_DIR/venv/Scripts/activate" ]; then
  VENV_BIN="$BACKEND_DIR/venv/Scripts"
else
  VENV_BIN="$BACKEND_DIR/venv/bin"
fi

echo "Installing backend dependencies..."
"$VENV_BIN/pip" install -q -r "$BACKEND_DIR/requirements.txt"

echo "Starting backend on http://localhost:8000 ..."
(cd "$BACKEND_DIR" && "$VENV_BIN/uvicorn" main:app --reload) &
BACKEND_PID=$!

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
  echo "Installing frontend dependencies..."
  (cd "$FRONTEND_DIR" && npm install)
fi

echo "Starting frontend on http://localhost:5173 ..."
(cd "$FRONTEND_DIR" && npm run dev) &
FRONTEND_PID=$!

trap 'echo "Stopping..."; kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null' SIGINT SIGTERM

wait
