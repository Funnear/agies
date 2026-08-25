# How to setup development workspace for this project

## Preconditions

### Windows: use Git Bash, not PowerShell/cmd

All setup and tooling scripts in this repo are bash scripts. On Windows they must be run from
**Git Bash** (installed as part of [Git for Windows](https://gitforwindows.org/), which you need
anyway to clone the repo) — not PowerShell or cmd.exe. Every command below with a `[Windows]` tag
assumes a Git Bash shell.

### `make` is required (setup shortcut, linting, and the pre-commit hook)

[macOS]

Usually preinstalled with Xcode Command Line Tools. If missing:

```bash
xcode-select --install
```

[Windows]

Not installed by default — install GNU Make via winget:

```bash
winget install GnuWin32.Make
```

Then make sure `C:\Program Files (x86)\GnuWin32\bin` is on your `PATH` (restart Git Bash after
installing, or add it for the current session with
`export PATH="/c/Program Files (x86)/GnuWin32/bin:$PATH"`). Without this, `make setup` and the
pre-commit hook (which runs `make smoke_test`) will fail with `make: command not found`.

### Python >=3.13 is required

`data_ravers_utils` (the internal library submodule that `setup_dev.sh` installs automatically —
see [submodules.md](../12_development/submodules.md)) requires Python 3.13 or newer.
`tools/shell_scripts/setup_dev.sh` looks for a compatible `python3`/`python` on `PATH` first; on
Windows it also falls back to the `py` launcher (`py -3.13`) if plain `python`/`python3` resolves
to an older version. It exits with an error if nothing >=3.13 is found.

[macOS]

```bash
brew install python@3.13
```

[Windows]

Install from [python.org](https://www.python.org/downloads/) (or
`winget install Python.Python.3.13`), keeping the **"py launcher"** option checked during install.
List installed versions with:

```bash
py -0p
```

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
git clone https://github.com/Funnear/agies.git; \
cd agies
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
