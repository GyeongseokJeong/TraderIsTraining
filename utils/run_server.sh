#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
FRONTEND_DIR="${ROOT_DIR}/frontend"

POSTGRES_SERVICE="postgres"
BACKEND_HOST="${BACKEND_HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-18000}"
FRONTEND_HOST="${FRONTEND_HOST:-0.0.0.0}"
FRONTEND_PORT="${FRONTEND_PORT:-15173}"
API_BASE_URL="${VITE_API_BASE_URL:-http://localhost:${BACKEND_PORT}/api}"
# CORS_ORIGINS accepts both a JSON array string and a comma-separated string.
CORS_ORIGINS_VALUE="${CORS_ORIGINS:-[\"http://localhost:${FRONTEND_PORT}\"]}"

BACKEND_PID=""
FRONTEND_PID=""

log() {
  printf '[trader-is-training] %s\n' "$1"
}

fail() {
  printf '[trader-is-training] ERROR: %s\n' "$1" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

copy_env_if_missing() {
  local source_file="$1"
  local target_file="$2"

  if [[ ! -f "${target_file}" ]]; then
    cp "${source_file}" "${target_file}"
    log "Created ${target_file} from ${source_file}"
  fi
}

prepare_environment_files() {
  copy_env_if_missing "${ROOT_DIR}/.env.example" "${ROOT_DIR}/.env"
  copy_env_if_missing "${ROOT_DIR}/.env.example" "${BACKEND_DIR}/.env"
  copy_env_if_missing "${FRONTEND_DIR}/.env.example" "${FRONTEND_DIR}/.env"
}

ensure_backend_dependencies() {
  if [[ ! -x "${BACKEND_DIR}/.venv/bin/python" ]]; then
    log "Creating backend virtual environment"
    python3 -m venv "${BACKEND_DIR}/.venv"
  fi

  log "Installing backend dependencies"
  "${BACKEND_DIR}/.venv/bin/python" -m pip install -e "${BACKEND_DIR}[dev]"
}

ensure_frontend_dependencies() {
  if [[ ! -d "${FRONTEND_DIR}/node_modules" ]]; then
    log "Installing frontend dependencies"
    npm --prefix "${FRONTEND_DIR}" install
  fi
}

start_postgres() {
  log "Starting PostgreSQL"
  docker compose --env-file "${ROOT_DIR}/.env" -f "${ROOT_DIR}/docker-compose.yml" up -d "${POSTGRES_SERVICE}"
}

run_migrations() {
  log "Running database migrations"
  (cd "${BACKEND_DIR}" && CORS_ORIGINS="${CORS_ORIGINS_VALUE}" .venv/bin/alembic upgrade head)
}

start_backend() {
  log "Starting backend at http://${BACKEND_HOST}:${BACKEND_PORT}"
  (cd "${BACKEND_DIR}" && CORS_ORIGINS="${CORS_ORIGINS_VALUE}" .venv/bin/uvicorn app.main:app --host "${BACKEND_HOST}" --port "${BACKEND_PORT}") &
  BACKEND_PID="$!"
}

start_frontend() {
  log "Starting frontend at http://${FRONTEND_HOST}:${FRONTEND_PORT}"
  VITE_API_BASE_URL="${API_BASE_URL}" npm --prefix "${FRONTEND_DIR}" run dev -- --host "${FRONTEND_HOST}" --port "${FRONTEND_PORT}" &
  FRONTEND_PID="$!"
}

cleanup() {
  log "Stopping application processes"
  if [[ -n "${FRONTEND_PID}" ]]; then
    kill "${FRONTEND_PID}" 2>/dev/null || true
  fi
  if [[ -n "${BACKEND_PID}" ]]; then
    kill "${BACKEND_PID}" 2>/dev/null || true
  fi
}

wait_for_processes() {
  wait -n "${BACKEND_PID}" "${FRONTEND_PID}"
}

main() {
  require_command docker
  require_command python3
  require_command npm

  prepare_environment_files
  start_postgres
  ensure_backend_dependencies
  run_migrations
  ensure_frontend_dependencies

  trap cleanup EXIT INT TERM
  start_backend
  start_frontend
  wait_for_processes
}

main "$@"
