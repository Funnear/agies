# Git Branching, Pull Requests & Code Review

## 1. Branching Model

The repository uses a controlled branch structure:

-   `main` --- stable integration branch. Only the project owner (Faniia)
    approves and merges PRs into `main`.
-   `release/<version>` --- branch for preparing a specific release.
-   `feature/<issue-number>-<short-name>` --- contributor feature work
    linked to a GitHub issue.
-   `bugfix/<issue-number>-<short-name>` --- bug fixes linked to a
    GitHub issue.

Each contributor works in their own feature or bugfix branch. Every
branch should correspond to a GitHub Issue.

Release numbering and release milestones are defined in [Releases &
Versioning](releases-and-versioning.md).

## 2. Creating a Work Branch

Start from the branch you are contributing to and update it first:

``` bash
git switch main
git pull origin main
```

For work targeting a release:

``` bash
git switch release/<version>
git pull origin release/<version>
```

Create a branch associated with the issue:

``` bash
git switch -c feature/123-add-baseline
```

or:

``` bash
git switch -c bugfix/124-fix-evaluation
```

## 3. Commits

Keep commits focused and descriptive.

``` bash
git status
git add <files>
git commit -m "Add performance evaluation baseline"
```

Before opening a PR, make sure the branch is up to date with its target
branch:

``` bash
git fetch origin
git rebase origin/<target-branch>
```

Resolve conflicts if necessary, then run the project's required checks.

## 4. Pull Requests

A PR is required for changes to be merged into a shared branch.

A contributor should:

1.  Create a branch linked to a GitHub Issue.
2.  Implement the change.
3.  Run the required local checks.
4.  Push the branch.
5.  Open a PR against the appropriate target branch.
6.  Link the GitHub Issue in the PR.
7.  Address review comments.
8.  Wait for the required approval.

Push a new branch:

``` bash
git push -u origin feature/123-add-baseline
```

For release preparation, PRs should target the relevant
`release/<version>` branch. Release-branch PRs may be reviewed by any
project-team member; one approval is sufficient.

Only the project owner approves PRs targeting `main`.

## 5. Reviewer Checklist

The reviewer should verify:

-   [ ] PR is linked to the correct GitHub Issue.
-   [ ] The change matches the issue and PR description.
-   [ ] Scope is focused; unrelated changes are excluded.
-   [ ] Code is understandable and maintainable.
-   [ ] Existing functionality is not unnecessarily broken.
-   [ ] Relevant tests or smoke tests pass.
-   [ ] No obvious configuration, dependency, data, or security issues
    were introduced.
-   [ ] Documentation is updated when required.
-   [ ] The branch is suitable for merging into its target branch.

The reviewer does not need to repeat automated linting or formatting
checks when those are already enforced by the repository's pre-commit
hooks.

## 6. Required Checks Before a PR

The repository's pre-commit hook already handles linting and autofixes.

The project may also enforce smoke and other automated tests through Git
hooks. These checks must pass before a PR is opened.

If a hook modifies files automatically, review and commit those changes
before pushing.

## 7. Keeping Branches in Sync

Regularly update long-running branches with their target branch:

``` bash
git fetch origin
git rebase origin/<target-branch>
```

After rebasing a previously pushed personal branch:

``` bash
git push --force-with-lease
```

Use `--force-with-lease`, not `--force`.

## 8. Merging

The normal flow is:

``` text
GitHub Issue
     ↓
feature/bugfix branch
     ↓
Pull Request
     ↓
review
     ↓
release/<version>
     ↓
release
     ↓
main
```

Changes should not be committed directly to `main`.

The project owner performs the final approval and merge into `main`.
