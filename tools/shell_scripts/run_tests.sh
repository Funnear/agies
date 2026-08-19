#!/usr/bin/env zsh

set -euo pipefail

# Resolve project root
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# Project env defaults
export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH:-}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
export TRANSFORMERS_VERBOSITY="${TRANSFORMERS_VERBOSITY:-info}"

echo "== Pytest with coverage =="

if [ "$#" -eq 0 ]; then
  echo "\n== Running ALL tests with coverage =="
  echo "\n== Pytest with coverage =="
  coverage run -m pytest
else
  marker_expr="$1"
  shift
  for m in "$@"; do
    marker_expr="${marker_expr} or ${m}"
  done

  echo "\n== Running tests with markers: ${marker_expr} =="
  echo "\n== Pytest with coverage =="
  coverage run -m pytest -m "${marker_expr}"
fi

echo "\n== Coverage report =="
coverage report