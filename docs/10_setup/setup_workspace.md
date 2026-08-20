# How to setup development workspace for this project

## Preconditions

### Windows: use Git Bash, not PowerShell/cmd

All setup and tooling scripts in this repo are bash scripts. On Windows they must be run from
**Git Bash** (installed as part of [Git for Windows](https://gitforwindows.org/), which you need
anyway to clone the repo) — not PowerShell or cmd.exe. Every command below with a `[Windows]` tag
assumes a Git Bash shell.

### Mermaid requires NodeJS, install it

[macOS]

```bash
brew update; \
brew install node
```

[Windows]

Install the LTS release from [nodejs.org](https://nodejs.org/) (or `winget install OpenJS.NodeJS.LTS`),
then verify `node` and `npm` are on PATH inside Git Bash:

```bash
node --version; npm --version
```

## Clone and enter the project

[macOS, linux, Windows (Git Bash)]

```bash
git clone https://github.com/Funnear/data_science_project_template_by_faen; \
cd data_science_project_template_by_faen
```

## Run the developer setup script

It makes tools executable, creates venv, installs deps, registers Jupyter kernel, installs git hook.
It auto-detects the platform (Windows vs macOS/Linux) — no separate steps needed per OS, just run it
from Git Bash on Windows.

[macOS, linux, Windows (Git Bash)]

```bash
chmod +x tools/shell_scripts/setup_dev.sh; \
./tools/shell_scripts/setup_dev.sh
```

or better:

[macOS, linux, Windows (Git Bash)]

```bash
chmod +x tools/shell_scripts/setup_dev.sh; \
make setup
```

## Activate the virtual environment for day-to-day work

[macOS, linux]

```bash
source venv/bin/activate
```

[Windows (Git Bash)]

```bash
source venv/Scripts/activate
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
