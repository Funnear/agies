#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

RESET_TEST_CACHE=false
RESET_LOGS=false
RESET_NODE=false

# dry-run is DEFAULT
DRY_RUN=true

usage() {
  cat <<'USAGE'
Usage: ./tools/shell_scripts/env_reset.sh [options]

Model cache options:

Other reset options:
  --test-cache                 Clear pytest/ruff/coverage caches
  --logs                       Clear project logs
  --node                       Delete Node deps (node_modules + package-lock.json)
  --all                        Perform model-cache + test-cache + logs + node reset

Execution:
  --apply                      Actually perform deletions (dry-run is default)

Examples:
  ./tools/shell_scripts/env_reset.sh --node --apply
  ./tools/shell_scripts/env_reset.sh --all --apply
USAGE
  exit 1
}

run_cmd() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
  else
    echo "[apply] $*"
    "$@"
  fi
}

print_plan() {
  echo "== Plan =="
  if $DRY_RUN; then
    echo "Mode: dry-run (no changes will be made)"
  else
    echo "Mode: APPLY"
  fi

  echo "Actions:"
  echo "  Test cache reset:   ${RESET_TEST_CACHE}"
  echo "  Logs reset:         ${RESET_LOGS}"
  echo "  Node deps reset:    ${RESET_NODE}"
}

# ---------------- CLI parsing ----------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --test-cache)
      RESET_TEST_CACHE=true
      shift
      ;;
    --logs)
      RESET_LOGS=true
      shift
      ;;
    --node)
      RESET_NODE=true
      shift
      ;;
    --all)
      RESET_TEST_CACHE=true
      RESET_LOGS=true
      RESET_NODE=true
      shift
      ;;
    --apply)
      DRY_RUN=false
      shift
      ;;
    *)
      usage
      ;;
  esac
done

echo "== Environment reset =="
print_plan

if ! $RESET_TEST_CACHE && ! $RESET_LOGS && ! $RESET_NODE; then
  echo "No actions selected."
  exit 0
fi

# ---------------- Actions ----------------

if $RESET_TEST_CACHE; then
  run_cmd rm -rf "${PROJECT_ROOT}/.pytest_cache" "${PROJECT_ROOT}/.ruff_cache" || true
  run_cmd rm -f "${PROJECT_ROOT}/.coverage" || true
fi

if $RESET_LOGS; then
  run_cmd mkdir -p "${PROJECT_ROOT}/logs"
  run_cmd rm -f "${PROJECT_ROOT}/logs"/*.log || true
fi

if $RESET_NODE; then
  run_cmd rm -rf "${PROJECT_ROOT}/node_modules" || true
  run_cmd rm -f "${PROJECT_ROOT}/package-lock.json" || true
fi

echo "Done."
