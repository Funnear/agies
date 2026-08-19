# Life hacks for git

## Assign the project root to a variable in a script

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel)" \;
echo "$PROJECT_ROOT"
```

## Add all empty directories to be committed to preserve file structure upfront. USeful for project templates

```bash
find . -type d -empty -exec touch {}/.gitkeep \;
```
