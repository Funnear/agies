#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"
SRC_HOOK="${PROJECT_ROOT}/tools/git_hooks/pre-commit"
DST_HOOK="${PROJECT_ROOT}/.git/hooks/pre-commit"

echo "[INFO] Updating git pre-commit hook"

# Check source hook exists
if [[ ! -f "$SRC_HOOK" ]]; then
  echo "[ERROR] Source hook not found at: $SRC_HOOK" >&2
  exit 1
fi

# Create hooks directory if missing
mkdir -p "${PROJECT_ROOT}/.git/hooks"

# If hook exists and no --force → abort
if [[ -f "$DST_HOOK" && "${1-}" != "--force" ]]; then
  echo "[WARN] Pre-commit hook already exists at:"
  echo "       $DST_HOOK"
  echo "[WARN] Not overwriting. Use:"
  echo "       tools/shell_scripts/update_githook.sh --force"
  exit 0
fi

# Copy hook
cp "$SRC_HOOK" "$DST_HOOK"
chmod +x "$DST_HOOK"

echo "[INFO] Installed pre-commit hook → ${DST_HOOK}"

# Show result
echo "[INFO] Current hook contents:"
echo "----------------------------------"
sed 's/^/|  /' "$DST_HOOK"
echo "----------------------------------"

echo "[INFO] Done."