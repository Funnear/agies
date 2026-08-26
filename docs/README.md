# Agentic Genre Intelligence Expert System [AGIES]

The Agentic Genre Intelligence Expert System is a human-in-the-loop multi-agent application for
high-quality music genre and subgenre classification. The system combines deterministic signal
processing, supervised machine learning, deep learning models for audio understanding, and
LLM-assisted reasoning to produce expert-validated genre annotations and high-quality datasets.

Rather than relying exclusively on LLMs, agents use the most appropriate execution strategy for
each task. Lightweight agents perform deterministic metadata analysis, rule-based validation,
dataset quality checks, taxonomy management, and workflow orchestration without token
consumption. Compute-intensive agents perform spectrogram generation, audio embedding
extraction, and deep neural network inference on selected tracks. LLM-powered agents are used
only where semantic reasoning or expert interaction provides additional value.

The initial MVP focuses on Electronic Dance Music (EDM), where fine-grained genre taxonomy
presents a challenging classification problem. The architecture is genre-agnostic and is designed
to expand to other music domains after the EDM scope proofs the general idea.

The project will adopt TOON (Token-Oriented Object Notation) as the primary structured
interchange format for LLM-enabled agents and MCP tool interactions. We will extend the existing
TOON ecosystem with reusable Python components and domain-specific schema definitions for
music genre intelligence, enabling compact, strongly typed communication between agents and
MCP servers. These TOON schemas will standardize requests and responses for tasks such as genre
taxonomy lookup, metadata enrichment, annotation workflows, and model inference. The Agentic
Genre Intelligence Expert System will serve as a real-world validation environment, demonstrating
how TOON-based MCP interfaces can reduce token consumption, improve interoperability, and
simplify the development of AI applications that combine deterministic pipelines, deep learning
models, and LLM-powered reasoning.

## Start Here

New to this repo? Read [10_setup/setup_workspace.md](10_setup/setup_workspace.md) first.
It covers preconditions, cloning, running `make setup`, and activating the environment.

## Documentation Index

### 00_overview

* [glossary.md](00_overview/glossary.md) — project-specific terms and abbreviations.

### 10_setup

* [setup_workspace.md](10_setup/setup_workspace.md) — clone, install, activate. Start here.

### 11_maintenance

* [git_lifehacks.md](11_maintenance/git_lifehacks.md) — small, reusable git/shell snippets.
* [troubleshooting.md](11_maintenance/troubleshooting.md) — resetting a broken dev environment.
* [use_make.md](11_maintenance/use_make.md) — what each `make <target>` does.

### 12_development

* [contribution_guidelines.md](12_development/contribution_guidelines.md) — SOLID, logging,
  error handling conventions.
* [documentation_guidelines.md](12_development/documentation_guidelines.md) — how to write
  docs in this repo.
* [protect_authorship.md](12_development/protect_authorship.md) — ORCID identity, commit
  signing (SSH/GPG), CITATION.cff, and Zenodo DOI archiving for contributors.
* [submodules.md](12_development/submodules.md) — adding/updating/removing git submodules.
* [uml_diagrams.md](12_development/uml_diagrams.md) — authoring and rendering Mermaid diagrams.

### 13_testing

* [linting.md](13_testing/linting.md) — Markdown linting setup and workflow.
* [testing.md](13_testing/testing.md) — running the test suite.

### 20_concept

Placeholder for product/concept docs (problem statement, scope, requirements). Empty in
the template — add your project's concept docs here.

### diagrams

* [diagrams/sources/](diagrams/sources/) — Mermaid `.md` sources (one fenced block per file).
* [diagrams/images/](diagrams/images/) — rendered PNG output (generated, not hand-edited).
* [diagrams/theme.json](diagrams/theme.json) — shared Mermaid CLI theme.

### presentations

Placeholder for slide decks / demo material. Empty in the template.

## Project Structure

| Path | Purpose |
| --- | --- |
| [src/](../src/) | Application/library source code. |
| [tests/](../tests/) | Test suite (pytest). |
| [config/](../config/) | Runtime config, e.g. [logging.yaml](../config/logging.yaml). |
| [notebooks/](../notebooks/) | Jupyter notebooks. |
| [tools/git_hooks/](../tools/git_hooks/) | Git hook scripts installed by setup. |
| [tools/python_scripts/](../tools/python_scripts/) | Standalone Python utility scripts. |
| [tools/shell_scripts/](../tools/shell_scripts/) | Dev tooling: setup, env reset, test runner, diagram generation. |
| [libs/](../libs/) | Git submodules (internal libraries), see [submodules.md](12_development/submodules.md). |
| [Makefile](../Makefile) | `make <target>` entry points, see [use_make.md](11_maintenance/use_make.md). |
| [requirements.txt](../requirements.txt) | Python dependencies. |
| [pytest.ini](../pytest.ini) | Pytest markers and config. |
| [package.json](../package.json) | Node dev tooling (markdownlint-cli). |
| [.gitmodules](../.gitmodules) | Registered git submodules. |
| [.markdownlint.json](../.markdownlint.json) | Markdown lint rules. |
| [LICENSE](../LICENSE) | Apache License 2.0. |

## Keeping This README Updated

List files added or removed on the current branch vs. `main`:

```bash
git diff --name-status --diff-filter=AD main...HEAD
```

Prompt for an LLM developer assistant (e.g. Claude Code):

```text
The following files were added (A) or deleted (D) on this branch:
<paste output of the git command above>

Using docs/README.md as the current documentation index and structure overview:
0. Strictly follow the markdown lint rules.
1. For each added file under docs/, add a linked entry with a one-line purpose,
   under the correct "### <folder>" section (create the section if the folder is new).
2. For each deleted file under docs/, remove its entry.
3. For each added/deleted top-level folder or key file (src/, tests/, config/,
   tools/*, Makefile, requirements.txt, etc.), update the "Project Structure" table.
4. Do not rewrite sections unrelated to the changed files.
5. Put the README update in its own commit, separate from code changes.
```
