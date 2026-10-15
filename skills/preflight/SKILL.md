---
name: preflight
description: Establish fresh repository state and actual session capabilities before exploring, planning, implementing or answering "does X exist?". Use at the start of any task in a repository, after an idle period or context handoff, when switching features, or when another session may have merged work.
---

# Preflight: fresh state and real capabilities

The aim is to base every recommendation and change on integrated main as it is now, and to know what this session can actually do before promising anything.

## 1. Freshness

```sh
git status --short --branch
git fetch origin
git rev-parse origin/main          # use the repository's default branch
```

- Record the SHA. Read AGENTS.md, the work index (for example `docs/current-work.md`), the handover and the relevant source **from that ref**: `git show origin/main:<path>`, or a new worktree (`git worktree add <dir> origin/main`). Do not read them from the current checkout, which may be another branch or stale.
- In zsh, quote the ref: `git show "${SHA}:path"` or `git cat-file -p "${SHA}:path"`. An unquoted `$SHA:s…` is parsed as a substitution modifier.
- If the local branch is behind or diverged, say so briefly. Do not fix it by resetting, cleaning or pulling into a dirty checkout.
- If the fetch fails, report it, give the last known SHA and treat any capability assessment as unverified.

Before calling something missing, check it on `origin/main` and in open PRs (`gh pr list`). A feature may exist on main or be in flight in another session.

## 2. Workspace for changes

- New work goes on a new branch from the fetched default branch, in its own worktree when the checkout is dirty or shared.
- Parallel sessions can switch the branch of a shared checkout under you. Run `git branch --show-current` immediately before every commit, and re-fetch before writing any release or deployment claim.
- Version numbers, journal numbers and tags can be taken by other sessions. Check main and the published tags right before choosing one.

## 3. Capabilities

Record what you verified, using read-only evidence only:

| Capability | Read-only evidence |
| --- | --- |
| GitHub identity and repository access | `gh auth status`, `gh repo view` |
| CI/Actions read | `gh run list --limit 3` |
| Merge / workflow dispatch | Only documented permissions or the actual requested action. Never probe with a mutating call. |
| Production logs or diagnostics | The repository's binding command (for example a doctor script) |
| Commit identity | `git config user.name`, `git config user.email`. Must be the human developer, not an agent. |

If the repository binds a doctor command (for example `npm run doctor:cloud`), run it. Report missing capabilities now, with the operation and redacted error, not after implementing.

## 4. Deployment shape

Before writing code, classify the change:

- **Ordinary:** application code and docs that ship through the normal merge → checks → release path.
- **Operator-mediated:** database migrations, Compose or infrastructure, host scripts, secrets, OAuth consent, permissions. These follow the repository's reviewed operator procedure. Put that prerequisite in the PR before merging, and never remove a deployment guard to make a release pass.

## 5. Report

Before proceeding, state briefly: the main SHA used, branch-only work you are building on, the latest verified release if relevant, verified and missing capabilities, and the deployment shape.
