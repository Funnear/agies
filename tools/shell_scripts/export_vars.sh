#!/usr/bin/env bash
# Minimal environment initializer for tests and CLI tools
#
# This script is meant to be sourced, so 'set -euo pipefail' below would
# otherwise leak into the caller's shell permanently once sourcing returns
# (unlike running a script as its own process). Save the caller's options
# and restore them on return so sourcing this script has no lasting effect
# on an interactive shell.
_export_vars_restore_opts="$(set +o)"
trap '
  eval "$_export_vars_restore_opts"
  trap - RETURN
  unset _export_vars_restore_opts
' RETURN

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

usage() {
  cat <<'USAGE'
Usage:
  source tools/shell_scripts/export_vars.sh [--debug]

Options:
  --debug    Set verbose logging (LOG_LEVEL=DEBUG, TRANSFORMERS_VERBOSITY=info)
USAGE
}

MODE="info"

if [[ "${1-}" == "--help" || "${1-}" == "-h" ]]; then
  usage
  return 0 2>/dev/null || exit 0
fi

if [[ "${1-}" == "--debug" ]]; then
  MODE="debug"
  shift || true
elif [[ -n "${1-}" ]]; then
  usage
  return 1 2>/dev/null || exit 1
fi

# PYTHONPATH for imports (native Windows Python needs ';', not ':')
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) PATH_SEP=';' ;;
  *) PATH_SEP=':' ;;
esac
export PYTHONPATH="${PROJECT_ROOT}/src${PATH_SEP}${PYTHONPATH:-}"

# Logging defaults (info by default)
if [[ "${MODE}" == "debug" ]]; then
  export LOG_LEVEL="DEBUG"
  export TRANSFORMERS_VERBOSITY="${TRANSFORMERS_VERBOSITY:-info}"
else
  export LOG_LEVEL="${LOG_LEVEL:-INFO}"
  export TRANSFORMERS_VERBOSITY="${TRANSFORMERS_VERBOSITY:-warning}"
fi