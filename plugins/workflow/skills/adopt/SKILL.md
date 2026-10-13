---
name: adopt
description: Set up a repository to follow the a-stack engineering workflow — pin the workflow plugin in project settings, add the AGENTS.md workflow block with repository bindings, and slim duplicated generic rules. Use when the user asks to apply, install or adopt a-stack workflows in a repo, or to upgrade a repo's pinned workflow version.
---

# Adopt the a-stack workflow in a repository

The workflow has two layers. The generic rules come from the pinned plugin. The repository's AGENTS.md supplies **bindings**: its concrete commands, paths, reviewer and release process, and any exceptions. Keep domain, architecture and product rules in the repository.

Do this as an ordinary reviewed change: preflight, a branch, a PR, independent review and a journal entry if the repository keeps one.

## 1. Pin the plugin for Claude Code

Merge these keys into the repository's committed `.claude/settings.json`, keeping any existing keys:

```json
{
  "extraKnownMarketplaces": {
    "a-stack": { "source": { "source": "github", "repo": "akhilvuputuri/a-stack", "ref": "workflow--v<VERSION>" } }
  },
  "enabledPlugins": { "workflow@a-stack": true }
}
```

Use the latest released `workflow--v<VERSION>` tag (`git ls-remote --tags https://github.com/akhilvuputuri/a-stack 'workflow--v*'`). Pinning means every contributor and session uses the same reviewed rules. Upgrading is a deliberate PR that changes the `ref`.

The marketplace has one `ref` for all a-stack plugins, and a tag carries every plugin as of its commit. If the repository already pins an a-stack `ref`, for example `ios-design--v<x>`:

- **Keep it** when it is newer and already contains the workflow version you want. Check `.claude-plugin/marketplace.json` at that ref.
- **Otherwise move to the newer tag** after confirming that it still contains the other plugins' versions you rely on. Never silently downgrade another plugin.
- **Pin only tags.** Pin only a tag whose plugin versions are all released (tagged). An untagged version can still change under the same version number, and Claude Code won't reinstall it.

Whichever ref you pin, write that actual ref in the AGENTS.md block, so that the CORE.md link matches what Claude Code loads.

The plugin's SessionStart hook loads the core rules into every Claude Code session, and its skills load when a task matches them.

## 2. Add the workflow block to AGENTS.md

Put [the AGENTS.md block](agents-block.md) at the top of AGENTS.md, with the tag and the bindings filled in. It repeats the non-negotiable rules inline so that agents without the plugin (Codex, Devin and others that read only AGENTS.md) still follow them, and it links the pinned `CORE.md` for the full text.

If the repository has a CLAUDE.md, it should say "Read and follow AGENTS.md", or import it with `@AGENTS.md`, and not restate the rules.

## 3. Fill in the bindings honestly

For each binding, write the repository's real value or `none`. Don't invent commands. Ask the user about any of these you can't determine from the repository:

- **Checks:** install, test, lint, format and build commands, and any paid or slow commands that must not run routinely.
- **Reviewer:** the preferred model, any accepted alternative per environment, and any bot reviews (such as Devin) with their expected cadence.
- **Merge authority:** whether the user permits merging passing ordinary changes, and the merge style.
- **Release:** what triggers a deploy, how to verify an exact SHA, the operator-mediated change types and their runbook, and the versioning and tag policy.
- **Records:** the journal path, the work index, the handover and the release notes file.
- **Diagnostics:** the doctor and capability command, and the log and diagnostics commands with their access limits.
- **Exceptions:** any deliberately different rule, with its scope. For example, an automated pipeline whose configured reviewer is accepted.

## 4. Remove duplication

Where the repository's AGENTS.md or docs restate generic rules now covered by `CORE.md` and the skills (freshness, review loop, release discipline, evidence labels, journal rules, commit identity), replace them with the block and keep only repository-specific content. Keep anything stricter than the generic rule as an explicit binding or exception. Never drop a stricter rule silently.

Record in the PR what was moved, what stayed and why.

## 5. Optional scaffolding

If the repository wants a journal and doesn't have one, create it with the `journal` skill's templates. If it has no REVIEW.md, either point reviewers at the plugin's review contract, or add a REVIEW.md that holds only domain-specific failure cases and defers to the contract for everything else.
