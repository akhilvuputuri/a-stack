---
name: adopt
description: Set up a repository to follow the akhilvuputuri/skills engineering workflow — pin the workflow plugin in project settings, add the AGENTS.md workflow block with repository bindings, and slim duplicated generic rules. Use when the user asks to apply, install or adopt the skills workflow in a repo, to upgrade a repo's pinned workflow version, or to move a repo off the former a-stack marketplace.
---

# Adopt the skills workflow in a repository

The workflow has two layers. The generic rules come from the pinned plugin. The repository's AGENTS.md supplies **bindings**: its concrete commands, paths, reviewer and release process, and any exceptions. Keep domain, architecture and product rules in the repository.

Do this as an ordinary reviewed change: preflight, a branch, a PR, independent review and a journal entry if the repository keeps one.

## 1. Pin the plugin for Claude Code

Merge these keys into the repository's committed `.claude/settings.json`, keeping any existing keys:

```json
{
  "enabledPlugins": {
    "skills@skills": true
  },
  "extraKnownMarketplaces": {
    "skills": {
      "source": {
        "source": "github",
        "repo": "akhilvuputuri/skills",
        "ref": "skills--v<VERSION>"
      }
    }
  }
}
```

When a Claude Code plugin command changes `.claude/settings.json`, it rewrites the whole file in its own key order and 2-space formatting. Commit the file in that form, for example by committing what `claude plugin marketplace add … --scope project` writes, so that later commands leave it unchanged. With only these two keys, that is the form shown above. With other keys, let Claude Code write the file once and commit the result.

Use the latest released `skills--v<VERSION>` tag (`git ls-remote --tags https://github.com/akhilvuputuri/skills 'skills--v*'`). Pinning means every contributor and session uses the same reviewed rules. Upgrading is a deliberate PR that changes the `ref`.

The plugin carries the workflow skills and `ios-design` together, so one ref covers everything. **Pin only release tags.** A branch or untagged commit can change under the same version number, and Claude Code won't reinstall it. Never move a pin to an older tag.

**Moving off the 0.1.x plugins.** Up to 0.1.x the marketplace shipped two plugins, `workflow@skills` and `ios-design@skills`. From `skills--v0.2.0` it ships one, `skills@skills`. In a repository that pins the old plugins, in one PR: set the `ref` to the new tag; replace `workflow@skills` and `ios-design@skills` in `enabledPlugins` and `.codex/config.toml` with `skills@skills`; and update the AGENTS.md block's link, ref and plugin name. Each contributor then switches their own install. **In Claude Code**, the old plugins show as disabled after the pull, at project scope:
  1. Run `claude plugin uninstall <plugin>@skills --scope project` for each old plugin, using the scope `claude plugin list` shows.
  2. Restart Claude Code in the folder.
  3. If `skills@skills` is still not enabled, run `claude plugin marketplace add akhilvuputuri/skills@<REF> --scope project` and `claude plugin install skills@skills --scope project`. `claude plugin marketplace update` does not move a marketplace to a new ref.
  4. Never run `claude plugin marketplace remove skills` in a pinned repository: it deletes the pin from `.claude/settings.json`.

**In Codex**, `codex plugin remove` each old plugin, then `codex plugin marketplace remove skills`, add it again at the new ref and `codex plugin add skills@skills`.

**Moving off the former `a-stack` name.** The repository and its marketplace were renamed from `akhilvuputuri/a-stack` (marketplace `a-stack`) to `akhilvuputuri/skills` (marketplace `skills`), starting with the `workflow--v0.1.2` and `ios-design--v0.1.2` tags. Older tags still declare the `a-stack` marketplace, so the new name needs a new tag. In a repository that pins `a-stack`, in one PR: rename the `a-stack` key in `extraKnownMarketplaces` to `skills` and point it at `akhilvuputuri/skills` and the new tag; replace every `<plugin>@a-stack` in `enabledPlugins` and `.codex/config.toml` with `skills@skills` (from `skills--v0.2.0`); and update the AGENTS.md block's link, ref and plugin names. Each contributor then switches their own registration: in Claude Code, `claude plugin marketplace remove a-stack` (adding the same source again does not register the new name while the old one exists); in Codex, `codex plugin remove <plugin>@a-stack` for each old plugin, then `codex plugin marketplace remove a-stack`, `codex plugin marketplace add akhilvuputuri/skills@<REF>` and `codex plugin add skills@skills`. Removing only the Codex marketplace leaves its plugins enabled, so every skill loads twice; `codex plugin remove <plugin>@a-stack` still works after the marketplace is gone.

Whichever ref you pin, write that actual ref in the AGENTS.md block, so that the CORE.md link matches what Claude Code loads.

The plugin's SessionStart hook loads the core rules into every Claude Code session, and its skills load when a task matches them.

For Codex, also commit `.codex/config.toml` with `[plugins."skills@skills"]` and `enabled = true`. Each contributor runs `codex plugin marketplace add akhilvuputuri/skills@<REF>` and then `codex plugin add skills@skills` once. Enabling a plugin in project config does not install it. Codex has no project-level marketplace pin, and the Codex plugin ships no hooks, so the AGENTS.md block below carries the rules for Codex. For other agents, `npx skills add https://github.com/akhilvuputuri/skills/tree/<REF>` installs the skills.

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
