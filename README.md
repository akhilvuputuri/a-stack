# skills

Akhil's lean collection of coding and AI workflow skills for coding agents.

## Install

Any agent (Claude Code, Codex, Cursor, Copilot, Gemini and [70+ more](https://github.com/vercel-labs/skills#supported-agents)):

```sh
npx skills add akhilvuputuri/skills
```

This installs the instruction skills from `ios-design` and `workflow`. Add `--list` to browse, `--skill <name>` to pick, `-g` for every project, and `-a <agent>` to choose agents. For a reviewed release instead of the default branch, use a tag URL such as `npx skills add https://github.com/akhilvuputuri/skills/tree/workflow--v0.1.2`.

**Claude Code:** the plugin is recommended, because only the Claude plugin adds the workflow's always-on core rules (a SessionStart hook). The Codex plugin deliberately ships no hooks.

```sh
claude plugin marketplace add akhilvuputuri/skills
claude plugin install workflow@skills
claude plugin install ios-design@skills
```

If you added this marketplace under its former name, `a-stack`, remove it first with `claude plugin marketplace remove a-stack`; installed `<plugin>@a-stack` plugins go with it.

**Codex** (CLI plugin marketplace):

```sh
codex plugin marketplace add akhilvuputuri/skills
codex plugin add workflow@skills
codex plugin add ios-design@skills
```

**Handoff** needs a compiled helper per platform, so it installs only through the [release installer](#install-without-cloning). `npx skills` hides it.

| Plugin | Skills | Use |
| --- | --- | --- |
| `workflow` | `preflight`, `independent-review`, `ship`, `journal`, `incident`, `experiment`, `adopt` | Akhil's engineering workflow for coding agents, plus always-on core rules in Claude Code |
| `ios-design` | `ios-design` | Audit or refine native iPhone/iPad interfaces using a source-linked digest of Apple's Human Interface Guidelines: Liquid Glass, Dynamic Type, accessibility, components, writing, app icons, and reading/offline-first patterns |
| Handoff (release installer) | `publish-handoff`, `resume-handoff` | Save the context for one task, then resume it in another local agent session |

## Engineering workflow for every repository

`plugins/workflow` centralises the development workflow that grew up in chief-agent, so other repositories can apply it without copying it.

- **Core rules** ([`CORE.md`](plugins/workflow/CORE.md)) cover fresh-state preflight, capability checks, independent exact-head review, verified delivery, evidence labels, records and hygiene. In Claude Code, a SessionStart hook loads them into every session, including after `/clear` and compaction. Other agents get the condensed rules from the repository's AGENTS.md block.
- **Skills** load when a task reaches their stage:

  | Skill | Use |
  | --- | --- |
  | `preflight` | Fetch and read from `origin/main`, use a worktree, record capabilities, classify the deployment shape |
  | `independent-review` | Reviewer prompt template, review contract, verdict recording |
  | `ship` | Exact-head merge, release watch by SHA, versioning, tags, release notes |
  | `journal` | Journal entry and index templates, evidence rules, release closure |
  | `incident` | Sources of truth, first pass, follow the failing stage, close the loop |
  | `experiment` | Frozen baseline, one mechanism at a time, honest reporting |
  | `adopt` | Set up a repository: pin the plugin, add the AGENTS.md block, fill in bindings |

To adopt it in a repository, ask an agent to "adopt the skills workflow in this repo". The `adopt` skill:

- pins `workflow@skills` in `.claude/settings.json`;
- puts [the workflow block](plugins/workflow/skills/adopt/agents-block.md) at the top of AGENTS.md. The block links `CORE.md` at the pinned tag, repeats the non-negotiable rules, and holds the repository's **bindings**: check commands, reviewer, merge authority, release verification, record paths and exceptions.

## Pinning a repository to a release

Commit this to the repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "skills": { "source": { "source": "github", "repo": "akhilvuputuri/skills", "ref": "workflow--v0.1.2" } }
  },
  "enabledPlugins": { "workflow@skills": true, "ios-design@skills": true }
}
```

For Codex, each contributor runs `codex plugin marketplace add akhilvuputuri/skills@workflow--v0.1.2` and then `codex plugin add workflow@skills` once. The repository's `.codex/config.toml` then keeps the plugin enabled in that trusted project. Enabling it there does not install it.

```toml
[plugins."workflow@skills"]
enabled = true
```

The marketplace has one `ref`, and a tag carries every plugin as of its commit. Current releases are `workflow--v0.1.2` and `ios-design--v0.1.2`, both on the same commit. Pin only a tag at which every plugin version you use is itself tagged. The `adopt` skill handles an existing pin without downgrading other plugins.

### Releasing a plugin

Claude Code and Codex install a new copy only when a plugin's `version` changes.

- Every change to a plugin's folder under `plugins/` bumps its `version` in `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json` and its `.codex-plugin/plugin.json`. It also records the folder's digest for that version in `.claude-plugin/releases.json`.
- The reviewed merge commit is tagged `<plugin>--v<version>`, following Claude Code's convention, as soon as it merges. Released digests are immutable.
- `tests/marketplace.test.cjs` fails if a plugin changes without a new version, if the Codex and Claude manifests disagree, or if the README's pinned tags don't match the versions.

**Node 22+ is the only runtime requirement.** Release artifacts bundle a small Node-API filesystem addon to retain directory-relative reads, atomic writes, and store locking on macOS/Linux. No Python, compiler, dependency installation, daemon, MCP server, or model service is needed to use an installed skill. Windows is unsupported in this version. Git is optional for local code metadata; no Git is required to install or use discussion-only handoffs.

Use the matching platform/architecture artifact. macOS binaries target macOS 11+; Linux builds use glibc 2.35+ (Ubuntu 22.04 baseline). Alpine/musl builds are not supplied. CI verifies current macOS/Linux runners; minimum-OS loader execution is not independently verified.

## Install without cloning

This is the Handoff installer. Download the installer matching your laptop from the release: `handoff-install-darwin-arm64.cjs` for an Apple Silicon Mac, or `handoff-install-darwin-x64.cjs` for an Intel Mac. Linux artifacts use the corresponding architecture name. Check `node -p 'process.platform + "-" + process.arch'` if unsure. Release publication is pending review; prepared artifacts are not yet a public release.

```sh
node handoff-install-darwin-arm64.cjs --agent codex
# Or:
node handoff-install-darwin-arm64.cjs --agent claude-code
```

The single downloaded file includes both skills, the helper, schema, reference, and matching compiled addon. It installs independent copies into `~/.agents/skills` for Codex or `~/.claude/skills` for Claude Code. A custom destination is supported with `--target /path/to/agent/skills`. Install just one with `--skill publish-handoff` or `--skill resume-handoff`. Restart/start a fresh agent session if discovery does not refresh. Host invocation/discovery and filesystem permissions still need to be verified in your chosen agent.

The downloaded installer runs offline. Transfer it and its release checksum file to a work laptop through your approved mechanism; no source checkout or Git history travels with it. Updates are explicit: download a chosen new version and rerun with `--replace`. Recognized Python-era installations can be upgraded to Node without modifying stored handoffs. Unknown layouts/versions and unexpected file types are rejected to preserve local files. The installer never reads runtime records.

## Optional npx installation of Handoff

`npx skills add akhilvuputuri/skills` hides the Handoff skills (`metadata.internal`), because a repository copy has no compiled addon. Forced with `INSTALL_INTERNAL_SKILLS=1`, the copied helper reports that the filesystem addon is unavailable. The self-contained release ZIP below does include the addon, but its skills carry the same flag, so `npx skills` needs `INSTALL_INTERNAL_SKILLS=1` for that route too.

Self-contained, platform-specific Handoff skill ZIPs are also built. Vercel's `skills` CLI supports direct archive URLs, agent selection, and copy mode. Once published and validated, a ZIP can be installed using:

```sh
INSTALL_INTERNAL_SKILLS=1 npx skills add RELEASE_ZIP_URL --global --agent codex --copy
```

This route is an external installer, not a second implementation of Handoff. It may download npm packages/use its own telemetry or update behavior during setup; use the downloaded Node installer for an offline installation. The direct ZIP path avoids relying on a Git repository clone. **End-to-end npx archive installation is not yet verified.** Do not install the same skill through both routes in the same scope. [Skills CLI documentation](https://github.com/vercel-labs/skills#installation-methods).

An isolated trial with the npm-published `skills` 1.5.18 treated a direct localhost ZIP URL as a well-known discovery endpoint and found no skills. Repository main documents archive support, but that trial did not establish it for the published version. The direct Node installer is the verified install path; do not assume a future archive command works until tested against the chosen installer release.

## Use

After installation, talk to your coding agent:

- “Publish a handoff for the login bug only.”
- “Draft a handoff for the duplicate reply investigation.”
- “Update handoff H with today's findings.”
- “List handoffs for this project.”
- “Resume handoff H.”
- “Resume H and implement the fix.”

The agent handles JSON and helper commands. Publishing returns a handoff ID, revision ID, and local path. Another local agent with access to the same store can resume by ID; code and patches are not transferred. “Publish” means save locally; issue URLs are inert metadata. Competing successors remain visible instead of choosing by timestamp.

## Data and offline boundary

Default store: `~/.local/share/handoff`, outside source/application checkouts. Override with `HANDOFF_DATA_DIR` or `--data-dir`. Stores from before the rename keep working: `ASTACK_DATA_DIR` is still read when `HANDOFF_DATA_DIR` is unset, and an existing `~/.local/share/a-stack` is used while `~/.local/share/handoff` does not exist. To migrate, move the directory to the new path. Choose a genuinely local private directory rather than a cloud-synced folder. Store directories/files have user-only permissions. Worktrees share identity; separate clones remain isolated unless explicitly linked. Existing schema-v1 records and project IDs remain compatible with the former Python helper. The legacy `.relay.lock` filename is retained solely for store compatibility; the tool is called Handoff.

The helper makes no network calls. Local Git metadata reads deny transport protocols and lazy fetching. A cloud-backed agent can still send read context to its configured model provider; fully offline model processing requires a local agent/model. Containers require a store mount, and hosted agents without local filesystem access cannot use this store.

## Develop

Development requires Node 22+, a C compiler, and locally available Node headers. Compiled Node-API artifacts work across supported Node versions on the same platform/architecture. Building never downloads headers or dependencies. If the header location is unusual, set `HANDOFF_NODE_HEADERS` to the directory containing `node_api.h`.

```sh
npm run build:native
npm test
node tools/build-release.cjs --output-dir /path/to/artifacts
node tools/install.cjs --target /path/to/test-agent/skills
```

There are no npm dependencies or install scripts. The release builder emits a standalone installer, a self-contained skill ZIP, and SHA256 checksums for the build platform. Checksums detect mismatch/corruption; hashes from the same release host are not an independent publisher signature.

[Record schema](schema/handoff.schema.json), [command/storage reference](docs/handoff.md), [validation evidence](docs/validation.md), [installation research](docs/installation-research.md), and [development/review workflow](docs/development.md). `ios-design` evaluation cases and an SDK API probe live in [evals/ios-design](evals/ios-design).

Devin and independent review concern development of this repo; they are not dependencies for using the installed skills. Runtime handoffs, real work context, credentials, and scratch review data must never enter source, releases, tests, or diagnostics.
