#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

log_info() { echo "[INFO] $*"; }
log_warn() { echo "[WARN] $*"; }
log_error() { echo "[ERROR] $*" >&2; }

MODE="normal"
if [[ "${1-}" == "--self-update" ]]; then
  MODE="self-update"
  shift || true
  log_info "Running in self-update mode (re-installing tooling)."
fi

log_info "Setting up developer environment in ${PROJECT_ROOT}"

# ---------------------------
# Load shared project environment (optional)
# ---------------------------
if [[ -f "${PROJECT_ROOT}/tools/shell_scripts/export_vars.sh" ]]; then
  # shellcheck disable=SC1090
  source "${PROJECT_ROOT}/tools/shell_scripts/export_vars.sh"
fi

# ---------------------------
# Ensure tool scripts are executable
# ---------------------------
for script in "${PROJECT_ROOT}"/tools/shell_scripts/*.sh; do
  [[ -f "$script" ]] && chmod +x "$script" || true
done
log_info "Marked tool scripts as executable"

# ---------------------------
# Git pre-commit hook (if present)
# ---------------------------
HOOK_SRC="${PROJECT_ROOT}/tools/git_hooks/pre-commit"
HOOK_DST="${PROJECT_ROOT}/.git/hooks/pre-commit"

if [[ -f "$HOOK_SRC" ]]; then
  mkdir -p "${PROJECT_ROOT}/.git/hooks"
  cp "$HOOK_SRC" "$HOOK_DST"
  chmod +x "$HOOK_DST"
  log_info "Installed pre-commit hook"
else
  log_warn "Pre-commit hook not found at ${HOOK_SRC}"
fi

# ---------------------------
# Git submodules (data_ravers_utils)
# ---------------------------
SUBMODULE_URL="https://github.com/funnear/data_ravers_utils.git"
SUBMODULE_PATH="libs/data_ravers_utils"

if [[ -f "${PROJECT_ROOT}/.gitmodules" ]] && grep -q "path = ${SUBMODULE_PATH}" "${PROJECT_ROOT}/.gitmodules"; then
  log_info "Submodule ${SUBMODULE_PATH} already registered."
else
  # Some git versions refuse to create .gitmodules from scratch on `submodule add`
  # ("please make sure that the .gitmodules file is in the working tree") — make
  # sure the file exists first so a fresh clone with no .gitmodules yet still works.
  [[ -f "${PROJECT_ROOT}/.gitmodules" ]] || touch "${PROJECT_ROOT}/.gitmodules"
  log_info "Adding submodule ${SUBMODULE_PATH}"
  (cd "${PROJECT_ROOT}" && git submodule add "${SUBMODULE_URL}" "${SUBMODULE_PATH}")
fi

(cd "${PROJECT_ROOT}" && git submodule update --init --recursive)

# ---------------------------
# Python venv
# ---------------------------
# data_ravers_utils (installed later as an editable package) requires >=3.13,
# so the venv must be built with at least that version or the submodule
# install fails outright.
MIN_PY_MINOR=13

version_ok() {
  "$@" -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, ${MIN_PY_MINOR}) else 1)" >/dev/null 2>&1
}

PYTHON_CMD=()
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && version_ok "$candidate"; then
    PYTHON_CMD=("$candidate")
    break
  fi
done

# Windows commonly manages multiple Python installs via the `py` launcher
# rather than PATH — plain python3/python may resolve to an older version
# even when a compatible one is installed, so check the launcher explicitly.
if [[ ${#PYTHON_CMD[@]} -eq 0 ]] && command -v py >/dev/null 2>&1; then
  if version_ok py "-3.${MIN_PY_MINOR}"; then
    PYTHON_CMD=(py "-3.${MIN_PY_MINOR}")
  elif version_ok py -3; then
    PYTHON_CMD=(py -3)
  fi
fi

if [[ ${#PYTHON_CMD[@]} -eq 0 ]]; then
  log_error "Python >=3.${MIN_PY_MINOR} is required but was not found."
  log_error "Tried: python3, python, and (on Windows) 'py -3.${MIN_PY_MINOR}' / 'py -3'."
  log_error "Install Python 3.${MIN_PY_MINOR}+ from https://www.python.org/downloads/ (on Windows, keep the 'py launcher' option checked during install)."
  exit 1
fi

VENVDIR="${PROJECT_ROOT}/venv"
if [[ ! -d "${VENVDIR}" ]]; then
  log_info "Creating virtual environment at ${VENVDIR}"
  "${PYTHON_CMD[@]}" -m venv "${VENVDIR}"
else
  log_info "Virtual environment already exists at ${VENVDIR}"
fi

# POSIX venvs put the activate script in bin/, Windows venvs use Scripts/
if [[ -f "${VENVDIR}/Scripts/activate" ]]; then
  VENV_BIN_DIR="${VENVDIR}/Scripts"
else
  VENV_BIN_DIR="${VENVDIR}/bin"
fi

# shellcheck disable=SC1090
source "${VENV_BIN_DIR}/activate"

log_info "Upgrading pip and installing Python requirements"
# Use "python -m pip" rather than "pip install --upgrade pip": on Windows, pip.exe
# can't overwrite itself while it's the process doing the upgrading.
python -m pip install --upgrade pip
python -m pip install -r "${PROJECT_ROOT}/requirements.txt"

# ---------------------------
# Node tooling (markdownlint-cli)
# ---------------------------
if ! command -v node >/dev/null 2>&1; then
  log_error "Node.js is required but not installed."
  log_error "Install Node LTS (recommended)."
  exit 1
fi

NODE_MAJOR="$(node -v | sed 's/^v//' | cut -d. -f1)"
if [[ "$NODE_MAJOR" -gt 22 ]]; then
  log_warn "Node.js v$(node -v) detected. Tooling is tested best on Node LTS (20 or 22)."
  log_warn "If markdownlint breaks, switch Node to an LTS version."
fi

if [[ ! -f "${PROJECT_ROOT}/package.json" ]]; then
  log_warn "package.json not found; initializing minimal Node project in repo root."
  (cd "${PROJECT_ROOT}" && npm init -y)
fi

if [[ "$MODE" == "self-update" ]]; then
  log_info "Self-update: wiping Node deps (node_modules + package-lock.json)"
  rm -rf "${PROJECT_ROOT}/node_modules" || true
  rm -f "${PROJECT_ROOT}/package-lock.json" || true
fi

log_info "Installing Node dev dependencies (markdownlint-cli)"
if [[ -f "${PROJECT_ROOT}/package-lock.json" ]]; then
  (cd "${PROJECT_ROOT}" && npm ci)
else
  (cd "${PROJECT_ROOT}" && npm install)
fi

npm audit fix --force

# Pin markdownlint-cli explicitly (and ensure it's actually installed)
(cd "${PROJECT_ROOT}" && npm install --save-dev "markdownlint-cli@latest")

# ---------------------------
# Mermaid CLI (optional)
# ---------------------------
MERMAID_PKG="@mermaid-js/mermaid-cli"
LATEST_MERMAID_VERSION="$(npm view "$MERMAID_PKG" version)"

install_mermaid_cli() {
  log_info "Installing ${MERMAID_PKG}@${LATEST_MERMAID_VERSION} globally."
  npm install -g "${MERMAID_PKG}@${LATEST_MERMAID_VERSION}"

  # Match the Chromium build to whichever puppeteer version mermaid-cli actually
  # bundled, instead of guessing a chrome-headless-shell version independently.
  MERMAID_PKG_DIR="$(npm root -g)/${MERMAID_PKG}"
  BUNDLED_PUPPETEER_VERSION="$(node -p "require('${MERMAID_PKG_DIR}/node_modules/puppeteer/package.json').version" 2>/dev/null || true)"

  if [[ -n "$BUNDLED_PUPPETEER_VERSION" ]]; then
    npx -y "puppeteer@${BUNDLED_PUPPETEER_VERSION}" browsers install chrome-headless-shell
  else
    log_warn "Could not detect mermaid-cli's bundled puppeteer version; installing puppeteer's default browser build."
    npx -y puppeteer browsers install chrome-headless-shell
  fi
}

if ! command -v mmdc >/dev/null 2>&1; then
  log_warn "Mermaid CLI (mmdc) not found."
  install_mermaid_cli
else
  INSTALLED_MERMAID_VERSION="$(mmdc --version)"
  if [[ "$INSTALLED_MERMAID_VERSION" == "$LATEST_MERMAID_VERSION" ]]; then
    log_info "Mermaid CLI (mmdc) already up to date (v${INSTALLED_MERMAID_VERSION})."
  else
    log_warn "Mermaid CLI (mmdc) v${INSTALLED_MERMAID_VERSION} is outdated (latest: v${LATEST_MERMAID_VERSION}); updating."
    install_mermaid_cli
  fi
fi

# ---------------------------
# Jupyter kernel registration (optional)
# ---------------------------
if python -c "import ipykernel" >/dev/null 2>&1; then
  log_info "Registering Jupyter kernel 'python3 (venv)'"
  python -m ipykernel install --user \
    --name=venv \
    --display-name "python3 for Jupyter (venv)"
else
  log_warn "ipykernel not installed; skipping kernel registration."
fi

log_info "Python: $(python --version)"
log_info "Node:   $(node --version)"
log_info "npm:    $(npm --version)"
log_info "Developer setup completed (mode: ${MODE})"
echo "Next step in this shell:"
echo "  source ${VENV_BIN_DIR#$PROJECT_ROOT/}/activate"
echo "and in the activated shell:"
echo "  source tools/shell_scripts/export_vars.sh --debug"