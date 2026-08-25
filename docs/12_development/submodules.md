# Git Submodules for Internal Libraries

Reference: [Git Book — Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

## Already Set Up: data_ravers_utils

`data_ravers_utils` is this template's default internal library submodule.

* [tools/shell_scripts/setup_dev.sh](../../tools/shell_scripts/setup_dev.sh) adds and
  initializes it automatically — no manual step needed.
* Path: `libs/data_ravers_utils`

The rest of this page is a generic how-to for adding **other** submodules the same way.

## Add a Submodule

[macOS, linux]

```bash
git submodule add <repo-url> <path>; \
git submodule update --init --recursive
```

Example:

[macOS, linux]

```bash
git submodule add https://github.com/funnear/data_ravers_utils.git libs/data_ravers_utils; \
git submodule update --init --recursive
```

## Install a Submodule as an Editable Python Package

```bash
pip install -e ./<path>
```

## Import Inside a Jupyter Notebook

```python
import sys, os

# Append submodule parent path
module_path = os.path.abspath("./libs")
if module_path not in sys.path:
    sys.path.append(module_path)

# Example import
from <submodule_package>.module_name import some_function
```

## Update a Submodule

Pull the latest commits from the submodule's default branch (usually `main`):

[macOS, linux]

```bash
git submodule update --remote --merge; \
git add <path>; \
git commit -m "Update <submodule_name> submodule to latest commit"; \
git push origin main
```

## Push Changes Back to a Submodule's Own Repo

[macOS, linux]

```bash
cd <path>; \
git add --all; \
git commit -m "Syncing changes from downstream project"; \
git push origin main; \
cd -
```

## Remove a Submodule

[macOS, linux]

```bash
git submodule deinit -f <path>; \
git rm -f <path>; \
rm -rf .git/modules/<path>; \
git commit -m "Removed submodule <submodule_name>"
```
