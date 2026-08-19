# Contributor Identity, Attribution, and Citation

This guide defines the recommended identity, commit-signing, attribution, and citation setup
for contributors to open-source AI and machine-learning projects. Complete the applicable steps
before contributing to a release intended for persistent citation or research use.

## 1. Register an ORCID iD

Register an ORCID iD:

<https://orcid.org/register>

Registration is free and does not require a university, employer, or institutional
affiliation. After registration, verify your email address and complete the profile fields
relevant to your work.

Registration guide:

<https://support.orcid.org/hc/en-us/articles/360006897454-How-do-I-register-for-an-ORCID-iD>

ORCID provides a persistent contributor identifier. It does not cryptographically sign
source-code contributions.

## 2. Connect ORCID to Development Profiles

### GitHub

GitHub supports authenticated ORCID integration. Open **GitHub Settings > Public profile >
ORCID iD > Connect your ORCID iD**, authenticate with ORCID, and authorize the connection.

After connection, GitHub can display the authenticated ORCID iD on your public profile.

GitHub profile documentation:

<https://docs.github.com/en/account-and-profile/tutorials/personalize-your-profile>

### Kaggle

Kaggle does not currently provide native ORCID account integration. Where useful, add your
ORCID URL to your public profile or the descriptive documentation associated with your work.

If a Kaggle dataset or notebook must become a persistent, independently citable research
artifact, archive an appropriate version through a research repository such as Zenodo or OSF
and cross-reference the records.

## 3. Sign Git Commits

Git author metadata is not cryptographic proof of authorship. Contributors should sign
commits using SSH or GPG so that supported Git hosting platforms can verify that a commit was
signed using a key associated with the contributor.

The identity layers serve different purposes:

- Git `user.name` and `user.email` identify the commit author.
- SSH or GPG signatures provide cryptographic provenance for the commit.
- GitHub associates registered signing keys with the contributor's GitHub account.
- ORCID provides a persistent researcher or contributor identifier.

GitHub supports GPG, SSH, and S/MIME commit signatures:

<https://docs.github.com/en/authentication/managing-commit-signature-verification>

### SSH Signing

SSH signing requires Git 2.34 or later.

Check the installed Git version:

```bash
git --version
```

Check for an existing SSH key:

```bash
ls -la ~/.ssh
```

If necessary, create an Ed25519 key:

```bash
ssh-keygen -t ed25519 -C "YOUR_GITHUB_EMAIL"
```

Unless you require a custom location, accept the default path. This normally creates
`~/.ssh/id_ed25519` as the private key and `~/.ssh/id_ed25519.pub` as the public key.

Keep `id_ed25519` private. Never commit, publish, or share the private key.

Display the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

In GitHub, open **Settings > SSH and GPG keys > New SSH key**, select **Signing Key**, and add
the public key.

If the same SSH key is also used for GitHub authentication, GitHub requires it to be added
separately as an **Authentication Key** and as a **Signing Key**.

#### Load the SSH Key

Start the SSH agent if required:

```bash
eval "$(ssh-agent -s)"
```

On macOS, add the private key to `ssh-agent` and store its passphrase in Keychain:

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

If the private key has a passphrase, enter the passphrase created when the SSH key was
generated. This is not the GitHub account password.

On Linux, add the key to `ssh-agent`:

```bash
ssh-add ~/.ssh/id_ed25519
```

Verify that the key is loaded:

```bash
ssh-add -l
```

#### Configure the SSH Client

On macOS, create or edit the SSH configuration:

```bash
nano ~/.ssh/config
```

Add:

```text
Host github.com
    HostName github.com
    User git
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/id_ed25519
```

On Linux, omit the macOS-specific `UseKeychain` option:

```text
Host github.com
    HostName github.com
    User git
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519
```

Protect the SSH configuration:

```bash
chmod 600 ~/.ssh/config
```

Test GitHub SSH authentication:

```bash
ssh -T git@github.com
```

On the first connection, SSH may ask whether the GitHub host fingerprint should be trusted.
Verify the fingerprint against GitHub's published fingerprints before accepting it:

<https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints>

A successful authentication returns a message similar to:

```text
Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

#### Configure Git to Sign Commits with SSH

Configure SSH as the Git signing format, select the public signing key, and enable automatic
commit signing:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Check the configured Git identity:

```bash
git config --global user.name
git config --global user.email
```

Set the values if required:

```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

The email used for Git commits should be associated with the contributor's GitHub account if
GitHub attribution and signature verification are required.

#### Check the Repository Remote

SSH commit signing and SSH repository authentication are separate mechanisms. A repository
may use SSH-signed commits while its remote still uses HTTPS.

Check the current remote:

```bash
git remote -v
```

An SSH remote has the following form:

```text
origin  git@github.com:ORG/REPOSITORY.git (fetch)
origin  git@github.com:ORG/REPOSITORY.git (push)
```

If the remote instead uses HTTPS:

```text
origin  https://github.com/ORG/REPOSITORY.git (fetch)
origin  https://github.com/ORG/REPOSITORY.git (push)
```

switch `origin` to SSH:

```bash
git remote set-url origin git@github.com:ORG/REPOSITORY.git
```

Verify the change:

```bash
git remote -v
```

Test repository access without changing repository contents:

```bash
git fetch
```

#### Create and Verify a Signed Commit

Create commits normally:

```bash
git add .
git commit -m "Describe the change"
```

Because `commit.gpgsign` is enabled, Git signs new commits automatically.

Alternatively, explicitly request a signature:

```bash
git commit -S -m "Describe the change"
```

Check that SSH signing is enabled:

```bash
git config --global gpg.format
git config --global user.signingkey
git config --global commit.gpgsign
```

Expected values should correspond to:

```text
ssh
~/.ssh/id_ed25519.pub
true
```

Inspect whether the commit contains a cryptographic signature:

```bash
git cat-file commit HEAD
```

A signed commit contains a `gpgsig` field. The field name is retained by Git for different
signature formats, including SSH signatures.

Push the signed commit:

```bash
git push
```

Open the commit on GitHub and verify that it displays **Verified**. This confirms that GitHub
recognizes the signature and associates its signing key with the contributor account.

Existing commits created before commit signing was enabled do not become signed automatically.

Official instructions:

<https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key>

### GPG Signing

Use GPG instead of SSH when the contributor or project already uses an OpenPGP-based signing
workflow.

Generate or identify a GPG key:

```bash
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long
```

Configure the selected key:

```bash
git config --global --unset gpg.format
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true
```

Export the public key:

```bash
gpg --armor --export YOUR_GPG_KEY_ID
```

Add the exported public key under **GitHub Settings > SSH and GPG keys > New GPG key**.

Create signed commits normally or use `-S` explicitly:

```bash
git commit -S -m "Describe the change"
```

Official instructions:

<https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account>

Do not publish the GPG private key.

## 4. Sign Off Commits with a DCO

The Developer Certificate of Origin (DCO) is a lightweight declaration that a contributor
wrote, or otherwise has the right to submit, the contribution under the project's license. A
contributor affirms it per-commit by adding a `Signed-off-by` trailer to the commit message.
It is not a cryptographic signature.

DCO text:

<https://developercertificate.org/>

**Rule:** every commit submitted to the project must contain a DCO `Signed-off-by` trailer.

### Sign Off a Commit

Add the trailer with `-s` (or `--signoff`):

```bash
git commit -s -m "Add classifier evaluation"
```

Git derives the trailer from `user.name` and `user.email`.

### Combine DCO Sign-Off with SSH Signing

A DCO sign-off and an SSH or GPG commit signature are independent mechanisms. `-s` alone
should be sufficient together with automatic commit signing (see
[Configure Git to Sign Commits with SSH](#configure-git-to-sign-commits-with-ssh)), since Git
then signs every commit while `-s` adds the sign-off trailer.

If a commit is not signed automatically, request both explicitly:

```bash
git commit -s -S -m "Add classifier evaluation"
```

`-s` adds the `Signed-off-by` trailer; `-S` requests the cryptographic signature.

### Verify a DCO Sign-Off

Inspect the sign-off trailer:

```bash
git show --format=full HEAD
```

```text
commit 0123456789abcdef
Author: Jane Doe <jane@example.com>
Commit: Jane Doe <jane@example.com>

    Add classifier evaluation

    Signed-off-by: Jane Doe <jane@example.com>
```

Inspect the cryptographic signature separately:

```bash
git cat-file commit HEAD
```

### DCO Enforcement

DCO sign-off is enforced on pull requests across this group of projects. A pull request
containing a commit without a `Signed-off-by` trailer fails the DCO check and cannot be
merged.

### Fix a Missing Sign-Off

For the most recent commit:

```bash
git commit --amend --signoff --no-edit
git push --force-with-lease
```

For multiple commits missing DCO sign-offs, interactive rebase can amend each affected
commit. The exact procedure depends on whether those commits have already been shared.

## 5. Add Citation Metadata

Repositories intended to produce citable software should contain a `CITATION.cff` file in the
repository root.

Use Citation File Format 1.2.0 and include ORCID IDs for authors where available.

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "My ML Project"
authors:
  - family-names: Doe
    given-names: Jane
    orcid: "https://orcid.org/0000-0000-0000-0000"
  - family-names: Example
    given-names: Alice
    orcid: "https://orcid.org/0000-0000-0000-0001"
repository-code: "https://github.com/ORG/PROJECT"
```

Replace all example identifiers and repository values with actual project metadata.

GitHub recognizes `CITATION.cff` and can expose a **Cite this repository** interface. Zenodo
can also consume CFF metadata when describing archived software.

CFF specification:

<https://citation-file-format.github.io/>

GitHub citation documentation:

<https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files>

## 6. Prepare a Project for Zenodo

Zenodo can archive software repositories and assign persistent Digital Object Identifiers
\(DOIs\) to releases.

Before enabling automated GitHub archiving, the project should have:

- a public GitHub repository;
- an explicit open-source license;
- accurate repository metadata;
- a valid `CITATION.cff`;
- identified creators and contributors;
- a versioning convention;
- a stable release suitable for citation;
- a GitHub Release corresponding to that version.

For a framework and an independently delivered reference application, decide whether they are
separate citable artifacts. If they have separate repositories, release cycles, version
numbers, or independent reuse value, they should generally be archived as separate software
records rather than represented as one indistinguishable artifact.

A Python, npm, Maven, NuGet, or other package-registry publication is not required merely to
obtain a Zenodo software DOI. The relevant unit is a versioned software release.

## 7. Archive Releases with Zenodo

Connect your ORCID and GitHub accounts to Zenodo:

<https://zenodo.org/>

Enable the required GitHub repository in Zenodo. Once enabled, new GitHub releases can be
ingested and archived by Zenodo.

Zenodo GitHub integration documentation:

<https://help.zenodo.org/docs/github/>

Before publishing the resulting Zenodo record, verify:

- software title;
- version;
- release date;
- license;
- creators;
- contributor roles where applicable;
- ORCID iDs;
- repository URL;
- description and keywords.

Publish the record to obtain a DOI. Use the DOI when citing the released software version in
papers, datasets, documentation, presentations, and derivative research outputs.

Do not treat the DOI as a replacement for Git history. The DOI identifies the released
artifact; signed commits preserve provenance at the individual Git-object level.

## 8. Record AI and ML Artifacts

For projects that publish models or datasets separately from the source-code release,
maintain artifact-specific documentation.

For Hugging Face models, use a Model Card to document the developers, model version, source
repository, license, base model where applicable, training data, evaluation, limitations, and
preferred citation.

Hugging Face Model Card documentation:

<https://huggingface.co/docs/hub/en/model-cards>

Do not assume that an arbitrary `orcid:` field in Hugging Face Model Card YAML is standardized
metadata. Where ORCID attribution is required, include the contributor's ORCID URL in an
appropriate human-readable creator, author, citation, or project documentation field unless
the platform specification explicitly introduces a dedicated ORCID field.

If the project later produces an arXiv paper, JOSS paper, conference paper, dataset
publication, or other scholarly output, include contributor ORCID iDs in the publication
workflow where supported.

## 9. Contributor Checklist

- [ ] Register an ORCID iD and verify the associated email address.
- [ ] Connect the ORCID iD to GitHub.
- [ ] Add the ORCID URL to other contributor profiles where native integration is unavailable
      and where doing so is useful.
- [ ] Configure Git `user.name` and `user.email` correctly.
- [ ] Keep an appropriate email address associated with both the contributor identity and
      relevant research profiles where possible.
- [ ] Create or select an SSH or GPG signing key.
- [ ] Register the public signing key with GitHub.
- [ ] Add the SSH key to `ssh-agent`.
- [ ] On macOS, store the SSH key passphrase in Keychain where appropriate.
- [ ] Configure `~/.ssh/config` for GitHub SSH authentication.
- [ ] Verify GitHub SSH authentication with `ssh -T git@github.com`.
- [ ] Check whether the repository `origin` uses SSH.
- [ ] Change an HTTPS `origin` to SSH where SSH repository authentication is required.
- [ ] Configure automatic SSH or GPG commit signing.
- [ ] Never publish or commit private signing keys.
- [ ] Create a signed commit and verify that it contains a signature.
- [ ] Verify that the pushed commit displays **Verified** on GitHub.
- [ ] Add a DCO `Signed-off-by` trailer to every commit using `git commit -s`.
- [ ] If a commit is not signed automatically, use `git commit -s -S` to add both the
      sign-off trailer and the cryptographic signature.
- [ ] Fix any commit missing a DCO sign-off before opening or updating a pull request.
- [ ] Add the contributor and ORCID iD to `CITATION.cff` when the contributor qualifies for
      project authorship.
- [ ] Record other material contributions using the project's contributor metadata policy.
- [ ] Create a versioned release before archival.
- [ ] Archive citable software releases with Zenodo or another suitable research repository.
- [ ] Verify creator, contributor, ORCID, version, license, and repository metadata before
      publishing the archival record.
- [ ] Use the resulting DOI when citing a specific released software artifact.
- [ ] Add ORCID iDs to papers and other scholarly publications where supported.
- [ ] Document separately published ML models and datasets using the metadata mechanisms
      provided by their hosting platform.

## 10. Result

After completing this setup, a contributor has a persistent ORCID identity, an authenticated
link between ORCID and GitHub, SSH-authenticated repository access where configured,
cryptographically signed and DCO-signed-off Git contributions, machine-readable project
citation metadata, and a path to DOI-backed software releases.

These mechanisms address different attribution layers rather than replacing one another.
ORCID identifies the contributor across projects and institutions; SSH authentication
establishes access to GitHub repositories; signed commits establish cryptographic provenance;
the DCO `Signed-off-by` trailer, enforced on pull requests, certifies the contributor's right
to submit each commit under the project's license; `CITATION.cff` records project-level
authorship and citation metadata; and DOI-backed releases create persistent, citable research
artifacts suitable for software papers, academic publications, datasets, model releases,
funding records, and long-term OSS attribution.
