# Troubleshooting Guide

## Resetting the Developer Environment

Sometimes the local environment becomes inconsistent due to:

- stale `.pytest_cache`, `.ruff_cache`, or `.coverage`
- partially installed dependencies
- experiments inside `venv`

This guide explains how to perform a **safe, explicit, minimal reset** of the development environment.

> IMPORTANT
> The reset tool runs in **dry-run mode by default**.
> Nothing is deleted unless you explicitly confirm with `--apply`.

---

## Automated reset steps (recommended)

The project provides a unified reset tool:

```sh
tools/shell_scripts/env_reset.sh
```

Running without flags will:

- print the reset plan
- perform **no changes** (dry-run)

---

## Common reset scenarios

### 1) Reset everything

Preview (dry-run):

```sh
tools/shell_scripts/env_reset.sh --all
```

Apply (actually deletes caches):

```sh
tools/shell_scripts/env_reset.sh --all --apply
```

---

### 2) Reset only test caches

```sh
tools/shell_scripts/env_reset.sh --test-cache --apply
```

Effect:

- removes `.pytest_cache`
- removes `.ruff_cache`
- removes `.coverage`

Recommended when:

- tests behave inconsistently
- coverage is wrong or empty
- imports behave strangely under `pytest`

---

### 3) Reset only logs

```sh
tools/shell_scripts/env_reset.sh --logs --apply
```

Effect:

- deletes `logs/*.log`
- preserves the `logs/` directory

---

## Manual reset steps (fallback)

### 1) Clear test caches manually

```sh
rm -rf .pytest_cache .ruff_cache .coverage
```

---

### 2) Full dependency refresh (lightweight reset)

If dependencies are broken but venv is still intact:

[macOS, linux]

```sh
pip install --upgrade pip; \
pip install --force-reinstall -r requirements.txt
```

[Windows (Git Bash)]

```sh
python -m pip install --upgrade pip; \
python -m pip install --force-reinstall -r requirements.txt
```

`python -m pip` is required here instead of `pip install --upgrade pip` directly — on Windows,
`pip.exe` can't overwrite itself while it's the process doing the upgrading.

Useful when:

- notebooks fail to import modules
- Transformers behaves inconsistently between runs
- environment drift occurs after OS / Xcode updates

---

### 3) Hard reset (manual venv deletion)

If everything else fails:

[macOS, linux]

```sh
deactivate || true; \
rm -rf venv; \
python3 -m venv venv; \
source venv/bin/activate; \
python -m pip install --upgrade pip; \
python -m pip install -r requirements.txt
```

[Windows (Git Bash)]

```sh
deactivate || true; \
rm -rf venv; \
py -3.13 -m venv venv; \
source venv/Scripts/activate; \
python -m pip install --upgrade pip; \
python -m pip install -r requirements.txt
```

`data_ravers_utils` (installed separately as an editable package, see
[submodules.md](../12_development/submodules.md)) requires Python >=3.13. On Windows, use the
`py` launcher (`py -3.13`) to select it explicitly — plain `python3`/`python` may resolve to an
older version even when 3.13 is installed.

Then restore development setup:

```sh
tools/shell_scripts/setup_dev.sh
```

---

## When to use which reset?

| Symptom | Action |
| ------- | ------ |
| Tests behave inconsistently | Reset test caches |
| Logs not updating / too noisy | Reset logs |
| Transformers import inconsistencies | Dependency refresh |
| Missing modules, broken venv, kernel crashes | Hard reset |

---

## Verify environment after reset

Run:

```sh
make smoke_test
```

Or run demo:

<TODO: Implement demo launch script and document its call here.>

Expected after a clean reset:

- smoke tests pass
- demo logs show fresh timestamps and clean startup
