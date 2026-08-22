# Documentation guidelines

Nobody enjoys long reads. Write the fewest words that carry full meaning.

* Prefer short sentences and structured lists over paragraphs.
* Use code snippets instead of describing commands in prose.
* Document *why*, not *what* — code already shows *what*.
* Keep each doc file focused on one topic.
* Undocumented code is a liability. A little documentation beats none.

## Markdown reference

* Beginners: [Markdown Guide — Basic Syntax](https://www.markdownguide.org/basic-syntax/)
* Advanced / cheatsheet: [Markdown Cheatsheet](https://github.com/lifeparticle/Markdown-Cheatsheet)

## Documenting Python code

Relevant PEPs:

* [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/) (comments, docstring placement)
* [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

## Adding code snippets for a missing operating system

Shell snippets in this repo default to macOS; some also work unchanged on Linux.

Tag every OS-specific shell snippet, right above its code fence:

* `[macOS]` — macOS only.
* `[linux]` — linux only.
* `[macOS, linux]` — works on both as-is.
* `[windows]` — PowerShell or `cmd`, not a POSIX shell.
* `[Windows (Git Bash)]` — Windows via Git Bash, running the same POSIX command as the
  `[macOS, linux]` tag. This repo's setup and tooling scripts are bash-only (see
  [setup_workspace.md](../10_setup/setup_workspace.md)), so most Windows guidance in this repo
  uses this tag rather than native PowerShell/cmd.

If a snippet you need is missing, or untagged: add both the tag and the snippet.

[macOS, linux]

```bash
ls -la
```

[windows]

```powershell
Get-ChildItem
```

### The trailing `\;`

Only needed to terminate a command passed to `find -exec`. The shell would otherwise treat the
bare `;` as its own command separator before `find` ever sees it:

```bash
find . -name "*.tmp" -exec rm {} \;
```

Don't use `\;` to chain ordinary commands — it escapes the `;` into a literal character instead
of a separator, so it won't do what a plain `;`, `&&`, or a new line does:

```bash
brew update
brew install node
```

### Chaining commands with `; \`

Joins several commands into a single line the reader can paste and run at once: `;` separates
the commands, `\` escapes the newline so the shell reads them as one logical line.

```bash
git clone <repo-url>; \
cd <repo-dir>
```

Use it only when the commands must run together as one paste (e.g. `cd` only matters for the
command right after it). Independent steps don't need it — plain separate lines paste and run
just as well, and are easier to read:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Fixing documentation mistakes

Found a wrong statement, a dead link, or a broken code snippet while working on a branch?

* Fix it.
* Commit the fix **separately** from your feature/task commits.
* Scope the commit message to the doc fix, e.g. `docs: fix outdated lint:md example`.

## Impacted files under `tools/`

List files changed under `tools/` on the current branch vs. `main`:

```bash
git diff --name-status --diff-filter=AD main...HEAD
```

## Prompt: sync docs with a changed file list

Feed the output of the command above into an LLM developer assistant (e.g. Claude Code):

```text
The following files under tools/ changed on this branch:
<paste output of the git command above>

For each file:
1. Search docs/ for any reference to it — file paths, flags, function names,
   config keys, or example commands/snippets.
2. Flag doc sections that are now outdated, incorrect, or missing.
3. Propose the smallest edit that makes each flagged section accurate again.
4. Do not add new sections — only fix what no longer matches the code.
5. Put all doc fixes in one commit, separate from code changes.
```
