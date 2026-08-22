#!/usr/bin/env bash

set -euo pipefail

# Resolve project root
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# Project env defaults (native Windows Python needs ';', not ':')
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) PATH_SEP=';' ;;
  *) PATH_SEP=':' ;;
esac
export PYTHONPATH="${PROJECT_ROOT}/src${PATH_SEP}${PYTHONPATH:-}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
export TRANSFORMERS_VERBOSITY="${TRANSFORMERS_VERBOSITY:-info}"

echo "== Pytest with coverage =="

if [ "$#" -eq 0 ]; then
  printf '\n== Running ALL tests with coverage ==\n'
  printf '\n== Pytest with coverage ==\n'
  coverage run -m pytest
else
  marker_expr="$1"
  shift
  for m in "$@"; do
    marker_expr="${marker_expr} or ${m}"
  done

  printf '\n== Running tests with markers: %s ==\n' "${marker_expr}"
  printf '\n== Pytest with coverage ==\n'
  coverage run -m pytest -m "${marker_expr}"
fi

printf '\n== Coverage report ==\n'
coverage report