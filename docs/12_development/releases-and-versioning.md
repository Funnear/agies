# Releases & Versioning

## 1. Release Flow

Releases are created from `main`.

Each release has a dedicated branch:

``` text
main
 └── release/<version>
       ├── feature/<issue>-<name>
       └── bugfix/<issue>-<name>
```

Contributors work in feature or bugfix branches associated with GitHub
Issues. Their PRs target the relevant release branch.

For branching and review rules, see [Git Branching, Pull Requests & Code
Review](git-branching-and-code-review.md).

## 2. Version Numbering

Use Semantic Versioning:

``` text
MAJOR.MINOR.PATCH
```

For example:

``` text
0.1.0
0.2.0
1.0.0
```

For this project, the **minor version represents the next project
milestone**, while the patch version represents corrections or small
maintenance changes within that milestone.

### Planned milestones

| Version | Milestone |
| --- | --- |
| `0.1.0` | Hackathon submission review: shortlisted-candidate submission with the performance-evaluation baseline |
| `0.2.0` | Hackathon-ready scope: all functionality required immediately before the event |
| `1.0.0` | Hackathon result: first major release containing the completed hackathon work, if shortlisted |

The exact version may be adjusted if the project scope changes, but the
milestone meaning should remain explicit in the release notes.

## 3. Patch Releases

Patch releases are for fixes or small changes that do not represent a
new milestone.

Example:

``` text
0.1.0 → 0.1.1
```

Use a patch release for:

- bug fixes
- small corrections
- non-functional maintenance
- fixes required after a milestone release

A patch release should not introduce a new project milestone.

## 4. Release Branches

Create a release branch when work for a milestone is ready to be
organized and stabilized:

``` bash
git switch main; \
git pull origin main; \
git switch -c release/0.1.0; \
git push -u origin release/0.1.0
```

Feature and bugfix branches for that milestone branch from the release
branch.

Once the release is ready, merge the release branch into `main` through
a PR.

Only the project owner approves and merges the PR into `main`.

## 5. Release Preparation

Before a release is merged:

- required feature and bugfix PRs are merged into the release branch;
- required automated checks pass;
- the milestone's performance evaluation is completed where
    applicable;
- release documentation and notes are updated;
- the release version is finalized.

The release PR may be reviewed by any project-team member. One approval
is sufficient.

## 6. Tagging a Release

After the release is merged into `main`, create a Git tag:

``` bash
git switch main; \
git pull origin main; \
git tag -a v0.1.0 -m "Release v0.1.0"; \
git push origin v0.1.0
```

For a later release:

``` bash
git tag -a v0.2.0 -m "Release v0.2.0"; \
git push origin v0.2.0
```

Tags provide immutable references to released versions.

## 7. Release Notes

Each release should briefly record:

- milestone achieved;
- major features;
- important bug fixes;
- performance-evaluation results when applicable;
- known limitations, if relevant.

Keep release notes focused on what changed in that version; detailed
branching and review rules belong in [Git Branching, Pull Requests &
Code Review](git-branching-and-code-review.md).
