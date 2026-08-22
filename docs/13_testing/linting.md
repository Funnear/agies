# Markdown linting

Markdown files are checked with `markdownlint-cli`.

## One-time setup (already done in the repo)

[macOS, linux, Windows (Git Bash)]

```bash
npm init -y; \
npm install --save-dev markdownlint-cli
```

## Run markdown linting

`make lint` automatically runs:

```bash
npx --yes markdownlint-cli@latest --fix "README.md" "docs/**/*.md" "docs/diagrams/sources/*.md"
```

This fixes most issues in place.
Warnings about headings, structure, or duplicate titles may still
require manual edits.
