#!/usr/bin/env bash
# Simple smoke test: start backend, query health endpoint, verify response, then shutdown.
set -euo pipefail

# Start backend in background
uvicorn backend/app/main:app --host 127.0.0.1 --port 8000 &
PID=$!

# Wait for server to be ready (simple loop)
for i in {1..10}; do
  if curl -s http://127.0.0.1:8000/api/health > /dev/null; then
    break
  fi
  sleep 0.5
done

# Perform health check
RESPONSE=$(curl -s http://127.0.0.1:8000/api/health)
# Expect JSON with field "status":"ok"
if echo "$RESPONSE" | grep -q '"status":"ok"'; then
  echo "Smoke test passed"
else
  echo "Smoke test failed: $RESPONSE"
  kill $PID || true
  exit 1
fi

# Cleanup backend process
kill $PID || true
