# Markdown linting

Markdown files are checked with `markdownlint-cli`.

## One-time setup (already done in the repo)

```bash
npm init -y
npm install --save-dev markdownlint-cli
```

## Run markdown linting

`make test` automatically runs:

```bash
npm run lint:md
```

This fixes most issues in place.
Warnings about headings, structure, or duplicate titles may still
require manual edits.
