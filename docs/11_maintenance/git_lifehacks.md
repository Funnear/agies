# Life hacks for git

## Assign the project root to a variable in a script

[macOS, Linux]

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel)" ; \
echo "$PROJECT_ROOT"
```

## Add all empty directories to be committed to preserve file structure upfront

Useful for project templates.

[macOS, Linux]

```bash
find . -type d -empty -exec touch {}/.gitkeep \;
```

## Sync fixes from the project template into the project

Repositories created from a GitHub template do not retain an upstream relationship with the
template. Add the template repository as a separate remote while keeping the project repository
as `origin`.

Run once per project.

[macOS, Linux]

```bash
git remote add template git@github.com:ORG/TEMPLATE_REPOSITORY.git ; \
git remote -v
```

When the template contains a fix that should be propagated, fetch the template and identify the
commit containing the required fix.

[macOS, Linux]

```bash
git fetch template ; \
git log --oneline template/main
```

Apply the selected commit and push it to the project repository.

[macOS, Linux]

```bash
git cherry-pick <COMMIT_HASH> ; \
git push
```

Keep template fixes in small, atomic commits so projects can cherry-pick only applicable changes.
Prefer cherry-picking individual fixes over merging `template/main`, because projects created from
a GitHub template have independent Git histories and may contain project-specific modifications.

If commit signing is enabled, verify that the new cherry-picked commit is signed.

[macOS, Linux]

```bash
git cat-file commit HEAD
```

The commit object should contain a `gpgsig` field. If DCO is required, also verify that the commit
message contains the appropriate `Signed-off-by:` trailer.

## List added, deleted, and modified files

Use `--name-status` without filtering to list all changed files and their status relative to
`main`.

[macOS, Linux]

```bash
git diff --name-status main...HEAD
```

The status prefix identifies the change type: `A` for added, `D` for deleted, and `M` for modified.
Git may also report other statuses, such as `R` for renamed or `C` for copied files.

To restrict the output strictly to added and deleted, filter by status.

[macOS, Linux]

```bash
git diff --name-status --diff-filter=AD main...HEAD
```

Prefer Git's `--diff-filter` over piping the output to `grep`, because the filtering is performed
directly by Git and does not depend on external text-processing tools.
