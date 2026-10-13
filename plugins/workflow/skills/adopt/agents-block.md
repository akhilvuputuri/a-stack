# AGENTS.md workflow block

Paste this at the top of the repository's AGENTS.md and replace each `<…>`.

```markdown
## Workflow

This repository follows the [a-stack engineering workflow](https://github.com/akhilvuputuri/a-stack/blob/<REF>/plugins/workflow/CORE.md), pinned to marketplace ref `<REF>` (normally `workflow--v<VERSION>`; see the adopt skill when several a-stack plugins share the ref). Claude Code loads it through the `workflow@a-stack` plugin pinned in `.claude/settings.json`. Other agents should read the linked CORE.md at that tag before starting work. The bindings below supply this repository's specifics and win where they are more specific.

Non-negotiable even without the plugin:

- Fetch origin and read from `origin/<default branch>` before exploring or changing anything, and again whenever you cannot establish that the last fetch is still current. Never reset or clean a shared or dirty checkout. Work on a branch or worktree.
- Every change gets an independent reviewer that did not write it (bindings may allow a focused review for docs-only changes), with an explicit APPROVE or REQUEST CHANGES for the exact head SHA. Re-review after every fix.
- A task ends at verified delivery (exact deployed SHA and evidence) or a named blocker.
- Label claims as reported, tested, measured, hypothesis or deferred. Never invent results. A supplied memory or context item is not proof the model used it.
- Commit as the human developer's git identity, with no agent author or `Co-Authored-By` trailer. If the identity is unset or shows an agent, stop and ask; never set one yourself. Keep secrets and private data out of the repository, PRs and logs.

### Workflow bindings

- **Checks:** `<install>`; `<test>`; `<lint/format>`; `<build>`. Do not run routinely: `<paid/slow commands or none>`.
- **Reviewer:** `<preferred model>`; accepted alternatives: `<environment → model>`. Bot review: `<Devin on every push after ready / none>`.
- **Merge authority:** `<user permits merging passing ordinary changes / ask first>`; style `<squash/merge>`.
- **Release:** `<what triggers deploy>`; verify an exact SHA with `<command>`. Operator-mediated changes: `<types>`, following `<runbook>`. Versioning: `<policy or none>`.
- **Records:** journal `<docs/journey or none>`; work index `<path>`; handover `<path>`; release notes `<path>`.
- **Diagnostics:** capabilities `<doctor command or none>`; logs `<command and access limits>`.
- **Exceptions:** `<scoped deviations or none>`.
```
