SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: test performance lint format diagrams setup

setup:
	./tools/shell_scripts/setup_dev.sh

lint:
	ruff check src tests tools
	npx --yes markdownlint-cli@latest --fix "README.md" "docs/**/*.md" "docs/diagrams/sources/*.md"

format:
	black src tests tools

autofix:
	ruff check src tests tools --fix

smoke_test: format autofix lint

performance: format autofix lint
	source tools/shell_scripts/export_vars.sh --debug
	tools/shell_scripts/run_tests.sh performance

test_units: format autofix lint
	source tools/shell_scripts/export_vars.sh --debug
	tools/shell_scripts/run_tests.sh unit

test_components: format autofix lint
	source tools/shell_scripts/export_vars.sh --debug
	tools/shell_scripts/run_tests.sh component

test_integration: format autofix lint
	source tools/shell_scripts/export_vars.sh --debug
	tools/shell_scripts/run_tests.sh integration

diagrams:
	@echo "== Generating UML diagrams =="
	@tools/shell_scripts/gen_diagrams.sh

update_hook:
	tools/shell_scripts/update_githook.sh --force
