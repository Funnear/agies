#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"
SRC_ROOT="${PROJECT_ROOT}/docs/diagrams/sources"
OUT_ROOT="${PROJECT_ROOT}/docs/diagrams/images"
THEME_FILE="${PROJECT_ROOT}/docs/diagrams/theme.json"

echo "== Generating Mermaid diagrams =="

mkdir -p "${OUT_ROOT}"

find "${SRC_ROOT}" -type f -name '*.md' | while IFS= read -r src; do
  rel="${src#${SRC_ROOT}/}"
  base_no_ext="${rel%.md}"

  out_dir="${OUT_ROOT}/$(dirname "${rel}")"
  mkdir -p "${out_dir}"
  out="${out_dir}/$(basename "${base_no_ext}").png"

  tmp="$(mktemp)"

  # Extract first ```mermaid``` block
  sed -n '/```mermaid/,/```/p' "${src}" | sed '1d;$d' > "${tmp}"

  if [ ! -s "${tmp}" ]; then
    echo "Skipping ${rel} (no mermaid block found)"
    rm -f "${tmp}"
    continue
  fi

  # Detect diagram type (mindmap vs everything else)
  if grep -q 'mindmap' "${tmp}"; then
    echo "Rendering (mindmap) ${rel} → ${out#$PROJECT_ROOT/}"
    # Mindmaps: default/light theme with solid white background
    mmdc \
      -i "${tmp}" \
      -o "${out}" \
      --quiet \
      --backgroundColor "#ffffff"
  else
    echo "Rendering ${rel} → ${out#$PROJECT_ROOT/}"
    # Flowcharts and others: custom dark-ish theme, transparent background
    mmdc \
      -i "${tmp}" \
      -o "${out}" \
      --quiet \
      --backgroundColor transparent \
      -c "${THEME_FILE}"
  fi

  rm -f "${tmp}"
done

echo "== Mermaid diagram generation completed =="