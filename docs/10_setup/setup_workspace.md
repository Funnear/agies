# How to setup development workspace for this project

## Preconditions

### Mermaid requires NodeJS, install it

[macOS]

```bash
brew update \;
brew install node
```

## Clone and enter the project

[macOS, linux]

```bash
git clone https://github.com/Funnear/data_science_project_template_by_faen; \
cd data_science_project_template_by_faen
```

## Run the developer setup script

It makes tools executable, creates venv, installs deps, registers Jupyter kernel, installs git hook.

```bash
chmod +x tools/shell_scripts/setup_dev.sh; \
.tools/shell_scripts/setup_dev.sh
```

or better:

```bash
chmod +x tools/shell_scripts/setup_dev.sh; \
make setup
```

## Activate the virtual environment for day-to-day work

```bash
source venv/bin/activate
```

## Set environment variables

Use in the current shell (recommended)

```sh
source tools/shell_scripts/export_vars.sh
```

Enable debug verbosity

```sh
source tools/shell_scripts/export_vars.sh --debug
```
