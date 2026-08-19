# Using the Makefile

The [Makefile](../../Makefile) wraps common dev tasks into short `make <target>` commands.

## Targets

| Target | Runs | Purpose |
| --- | --- | --- |
| `setup` | `tools/shell_scripts/setup_dev.sh` | venv, pip deps, git hooks, submodules, Node/Mermaid tooling |
| `lint` | `ruff check src tests tools` + `npx markdownlint-cli --fix` | Python + Markdown lint |
| `format` | `black src tests tools` | Auto-format Python |
| `autofix` | `ruff check src tests tools --fix` | Auto-fix Python lint issues |
| `smoke_test` | `format` → `autofix` → `lint` | Full local format/lint sweep |
| `test_units` | ... → `tools/shell_scripts/run_tests.sh unit` | Unit tests + coverage |
| `test_components` | ... → `tools/shell_scripts/run_tests.sh component` | Component tests + coverage |
| `test_integration` | ... → `tools/shell_scripts/run_tests.sh integration` | Integration tests + coverage |
| `performance` | ... → `tools/shell_scripts/run_tests.sh performance` | Performance tests + coverage |
| `diagrams` | `tools/shell_scripts/gen_diagrams.sh` | Render Mermaid sources to PNG |
| `update_hook` | `tools/shell_scripts/update_githook.sh --force` | (Re)install pre-commit hook, overwriting |

Run any target with:

```bash
make <target>
```

## Test Targets in Detail

`test_units`, `test_components`, `test_integration`, and `performance` all:

1. Run `format`, `autofix`, `lint` first.
2. `source tools/shell_scripts/export_vars.sh --debug` — sets `PYTHONPATH`,
   `LOG_LEVEL=DEBUG`.
3. Call `run_tests.sh <marker>`, which runs `coverage run -m pytest -m <marker>`
   then prints a coverage report.

Markers are defined in [pytest.ini](../../pytest.ini):

```text
smoke, performance, component, unit, integration
```

## Implementation Notes

The Makefile sets:

```makefile
SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
```

Each target's recipe lines otherwise run in separate subshells — without `.ONESHELL`,
the `source tools/shell_scripts/export_vars.sh --debug` step's exports would not carry
over to the following `run_tests.sh` line. `SHELL := /bin/bash` is also required because
`source` is a Bash builtin, not available in every system's default `/bin/sh`.
