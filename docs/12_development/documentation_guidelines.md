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

## Fixing documentation mistakes

Found a wrong statement, a dead link, or a broken code snippet while working on a branch?

* Fix it.
* Commit the fix **separately** from your feature/task commits.
* Scope the commit message to the doc fix, e.g. `docs: fix outdated lint:md example`.

## Impacted files under `tools/`

List files changed under `tools/` on the current branch vs. `main`:

```bash
git diff --name-only main...HEAD -- tools/
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
