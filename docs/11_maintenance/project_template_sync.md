# Synchronizing projects with the project template

Projects created from the GitHub project template have independent Git histories. GitHub does not
retain an upstream relationship between a repository created from a template and the template
repository.

Reusable fixes and improvements should therefore be synchronized explicitly at the commit level.

The synchronization workflow is bidirectional:

- generic improvements made in the project template may be propagated to projects;
- generic improvements discovered while developing a project may be propagated back to the
  project template;
- project-specific changes must remain in the project repository.

Prefer `git cherry-pick` over copying files manually or merging repository histories. Cherry-picking
preserves the original commit author while recording the person performing the synchronization as
the committer.

## Configure the template remote in a project

The project repository remains `origin`. Add the project template as a separate remote.

Run once per project.

[macOS, Linux]

```bash
git remote add template git@github.com:Funnear/data_science_project_template_by_faen.git ; \
git fetch template ; \
git remote -v
```

The expected relationship is:

- `origin` points to the current project repository;
- `template` points to the shared project template.

## Configure a project remote in the template

When propagating reusable improvements from a project back to the template, add that project
temporarily as a remote of the local template repository.

[macOS, Linux]

```bash
git remote add project <PROJECT_GIT_URL> ; \
git fetch project ; \
git remote -v
```

Use a temporary name that clearly identifies the source project instead of `project` when useful.

Remove the temporary remote after synchronization.

[macOS, Linux]

```bash
git remote remove project ; \
git remote prune origin
```

## Work on a synchronization branch

Do not mix synchronization work with unrelated feature development. Create a maintenance branch
from the target repository's current `main`.

[macOS, Linux]

```bash
git switch main ; \
git pull --ff-only origin main ; \
git switch -c maintenance/project-template-sync
```

This provides a reviewable boundary for synchronization changes and allows project-specific
adaptations to be committed separately from imported commits.

## Inspect differences before synchronizing

Fetch the source repository before examining its history.

[macOS, Linux]

```bash
git fetch template
```

or, when working in the template:

```bash
git fetch project
```

Repositories created from a GitHub template may have unrelated Git histories. Do not assume that
three-dot comparisons or `git merge-base` will work between them.

Compare repository states directly when necessary.

[macOS, Linux]

```bash
git diff --name-status main template/main
```

For synchronization in the opposite direction:

```bash
git diff --name-status main project/main
```

Use the result to identify only files whose changes are reusable.

## Inspect the history of selected files

Before cherry-picking, determine which commits produced the changes that need to be synchronized.

[macOS, Linux]

```bash
git log \
  --reverse \
  --format='%h | %an <%ae> | %ad | %s' \
  --date=short \
  <SOURCE_BRANCH> -- \
  <PATH_1> \
  <PATH_2>
```

`--reverse` is important when several dependent commits need to be transferred. Apply older
commits before newer commits.

Inspect the files changed by a candidate commit before applying it.

[macOS, Linux]

```bash
git show --stat <COMMIT_HASH>
```

For a more explicit file list:

```bash
git show --name-status --format=fuller <COMMIT_HASH>
```

Do not cherry-pick a commit blindly merely because it modifies one required file. Verify whether
the same commit also contains project-specific changes.

## Cherry-pick commits in chronological order

When several commits contribute to the desired final state, apply them from oldest to newest.

[macOS, Linux]

```bash
git cherry-pick <OLDEST_COMMIT_HASH>
git cherry-pick <NEXT_COMMIT_HASH>
git cherry-pick <NEWEST_COMMIT_HASH>
```

This reproduces the evolution of the source files and usually reduces conflicts compared with
applying only the latest large commit.

It also preserves attribution at the commit level.

After a successful cherry-pick, Git normally records:

- the original contributor as `Author`;
- the person performing the synchronization as `Committer`.

## Handle squash commits

A squash merge represents several source commits as one commit on `main`.

Before transferring a squash commit, inspect its metadata.

[macOS, Linux]

```bash
git show --no-patch --format=full <COMMIT_HASH>
```

Preserve any `Co-authored-by:` trailers contained in the commit message.

If earlier commits leading to the squash commit are also required, transfer the relevant earlier
commits first and apply the squash commit in its correct chronological position.

Do not reconstruct contributor attribution from memory. Use the Git history and commit metadata as
the source of truth.

## Handle merge commits

Do not automatically cherry-pick a merge commit with `-m`.

First inspect its parents.

[macOS, Linux]

```bash
git show \
  --no-patch \
  --format='commit: %H%nparents: %P%nauthor: %an <%ae>%nsubject: %s' \
  <MERGE_COMMIT_HASH>
```

Compare the merge result with each parent to determine what the merge actually introduced.

[macOS, Linux]

```bash
git diff --name-status <FIRST_PARENT> <MERGE_COMMIT_HASH> ; \
git diff --name-status <SECOND_PARENT> <MERGE_COMMIT_HASH>
```

If only selected changes from the merge belong in the target repository, extract those changes
rather than cherry-picking the complete merge.

For selected files:

```bash
git diff <BASE_COMMIT> <MERGE_COMMIT_HASH> -- \
  <PATH_1> \
  <PATH_2> \
| git apply
```

Commit the selected changes separately while preserving the appropriate authorship information
from the source history.

## Resolve conflicts

If a cherry-pick conflicts, inspect and resolve the affected files manually.

After resolving them:

[macOS, Linux]

```bash
git add <RESOLVED_PATHS> ; \
git cherry-pick --continue
```

If the resulting cherry-pick is empty because the target already contains the effective change:

```bash
git cherry-pick --skip
```

To abandon a normal cherry-pick in progress:

```bash
git cherry-pick --abort
```

Do not use destructive reset commands until unrelated local changes have been identified and
protected.

## Adapt imported changes to the target project

Keep the imported contributor commits as close to their source form as practical.

Target-specific adjustments, such as replacing a concrete project name with a template placeholder,
should preferably be made in a separate commit after the relevant source commits have been
transferred.

Example:

```bash
git add <MODIFIED_PATHS> ; \
git commit -m "Adapt synced improvements for project template"
```

This keeps contributor work distinguishable from subsequent template or project adaptation.

## Verify synchronization

Compare the selected files after transferring their history.

[macOS, Linux]

```bash
git diff --name-status HEAD <SOURCE_BRANCH> -- \
  <PATH_1> \
  <PATH_2>
```

An empty result means that the selected files have identical content. Target-specific adaptations
made afterward are expected to introduce intentional differences.

Review the transferred commit attribution before pushing.

[macOS, Linux]

```bash
git log \
  --format='%h | Author: %an <%ae> | Committer: %cn <%ce> | %s' \
  origin/main..HEAD
```

If commit signing is enabled, inspect the resulting commit object when required.

[macOS, Linux]

```bash
git cat-file commit HEAD
```

A signed commit object contains a `gpgsig` field. If DCO is required, also verify the applicable
`Signed-off-by:` trailers.

## Push and clean up

After verification, push the synchronization branch and use the repository's normal review and
merge process.

After synchronization from a temporary project remote into the template, remove that remote.

[macOS, Linux]

```bash
git remote remove project ; \
git remote -v
```

Keep permanent `template` remotes in derived projects when they are used regularly for template
updates.

## Rules for synchronization

Follow these rules whenever changes move between the template and a derived project:

1. Classify a change as generic or project-specific before transferring it.
2. Synchronize commits, not entire repository histories.
3. Preserve the original `Author` and existing co-author attribution.
4. Apply dependent commits in chronological order.
5. Inspect every candidate commit for unrelated files before cherry-picking it.
6. Treat squash and merge commits explicitly rather than assuming they behave like ordinary
   commits.
7. Keep target-specific adaptations in separate commits where practical.
8. Never invent commit hashes, file paths, authors, branch names, or repository state.
9. Verify the resulting history and file differences before pushing.
10. Prefer small, atomic generic commits so future synchronization remains inexpensive.

## Using an LLM to assist with synchronization

An LLM can help inspect Git output, determine commit order, identify mixed project/template
changes, and prepare the next command. Git output remains the source of truth.

For an interactive synchronization session, use a prompt such as:

> I need to synchronize selected reusable changes between a project created from a GitHub template
> and the template repository. The repositories have independent Git histories.
>
> Preserve the original authorship of every transferred change. Prefer cherry-picking original
> commits and apply dependent commits chronologically from oldest to newest. Do not invent commit
> hashes, paths, branch names, authors, or repository state.
>
> Give me only commands that can be derived from output I have already provided. When more
> information is required, give me the command to obtain it and stop so I can paste the result.
> Do not give several speculative future steps at once.
>
> Before cherry-picking a commit, check whether it contains files or changes outside the requested
> synchronization scope. Treat merge commits and squash commits explicitly. Do not merge the full
> repositories.

When starting from a known set of files, append:

> These are the files I want to synchronize:
>
> `<PASTE git diff --name-status OUTPUT HERE>`
>
> First give me the Git command that shows the relevant commits affecting these files in
> chronological order. Stop after that command.

For deciding whether a candidate commit is safe to transfer, use:

> Here is the Git history and the output of `git show --name-status` for the candidate commits.
> Determine which commits can be cherry-picked whole and which contain unrelated changes. Preserve
> authorship. Do not generate the cherry-pick command until the required commit contents and order
> are established.

For resolving a synchronization conflict, use:

> This cherry-pick produced the following Git output and `git status`. Explain what state the
> repository is currently in and give me only the next safe command or manual action. Assume I may
> have unrelated local changes unless the supplied Git output proves otherwise.
