# AGENTS.md workflow block

Paste this at the top of the repository's AGENTS.md and replace each `<…>`.

```markdown
## Workflow

This repository follows the [a-stack engineering workflow](https://github.com/akhilvuputuri/a-stack/blob/workflow--v<VERSION>/plugins/workflow/CORE.md), pinned to `workflow--v<VERSION>`. Claude Code loads it through the `workflow@a-stack` plugin pinned in `.claude/settings.json`. Other agents should read the linked CORE.md at that tag before starting work. The bindings below supply this repository's specifics and win where they are more specific.

Non-negotiable even without the plugin:

- Fetch origin and read from `origin/<default branch>` before exploring or changing anything. Never reset or clean a shared or dirty checkout. Work on a branch or worktree.
- Every behavior change gets an independent reviewer that did not write it, with an explicit APPROVE or REQUEST CHANGES for the exact head SHA. Re-review after every fix.
- A task ends at verified delivery (exact deployed SHA and evidence) or a named blocker.
- Label claims as reported, tested, measured, hypothesis or deferred. Never invent results.
- Commit as the human developer's git identity, with no agent author or `Co-Authored-By` trailer. Keep secrets and private data out of the repository, PRs and logs.

### Workflow bindings

- **Checks:** `<install>`; `<test>`; `<lint/format>`; `<build>`. Do not run routinely: `<paid/slow commands or none>`.
- **Reviewer:** `<preferred model>`; accepted alternatives: `<environment → model>`. Bot review: `<Devin on every push after ready / none>`.
- **Merge authority:** `<user permits merging passing ordinary changes / ask first>`; style `<squash/merge>`.
- **Release:** `<what triggers deploy>`; verify an exact SHA with `<command>`. Operator-mediated changes: `<types>`, following `<runbook>`. Versioning: `<policy or none>`.
- **Records:** journal `<docs/journey or none>`; work index `<path>`; handover `<path>`; release notes `<path>`.
- **Diagnostics:** capabilities `<doctor command or none>`; logs `<command and access limits>`.
- **Exceptions:** `<scoped deviations or none>`.
```
