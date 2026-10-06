# a-stack

Akhil's lean collection of coding and AI workflow skills. Start with **Handoff**: save the context for one task, then resume it in another local agent session.

| Skill | Use |
| --- | --- |
| `publish-handoff` | Select one topic, draft/save a local handoff, or publish an updated revision. |
| `resume-handoff` | Retrieve/list handoffs, check relevant current state, and explain the next step. Implement when the user asks. |

**Node 22+ is the only runtime requirement.** Release artifacts bundle a small Node-API filesystem addon to retain directory-relative reads, atomic writes, and store locking on macOS/Linux. No Python, compiler, dependency installation, daemon, MCP server, or model service is needed to use an installed skill. Windows is unsupported in this version. Git is optional for local code metadata; no Git is required to install or use discussion-only handoffs.

Use the matching platform/architecture artifact. macOS binaries target macOS 11+; Linux builds use glibc 2.35+ (Ubuntu 22.04 baseline). Alpine/musl builds are not supplied. CI verifies current macOS/Linux runners; minimum-OS loader execution is not independently verified.

## Install without cloning

Download the installer matching your laptop from the release: `a-stack-install-darwin-arm64.cjs` for an Apple Silicon Mac, or `a-stack-install-darwin-x64.cjs` for an Intel Mac. Linux artifacts use the corresponding architecture name. Check `node -p 'process.platform + "-" + process.arch'` if unsure. Release publication is pending review; prepared artifacts are not yet a public release.

```sh
node a-stack-install-darwin-arm64.cjs --agent codex
# Or:
node a-stack-install-darwin-arm64.cjs --agent claude-code
```

The single downloaded file includes both skills, the helper, schema, reference, and matching compiled addon. It installs independent copies into `~/.agents/skills` for Codex or `~/.claude/skills` for Claude Code. A custom destination is supported with `--target /path/to/agent/skills`. Install just one with `--skill publish-handoff` or `--skill resume-handoff`. Restart/start a fresh agent session if discovery does not refresh. Host invocation/discovery and filesystem permissions still need to be verified in your chosen agent.

The downloaded installer runs offline. Transfer it and its release checksum file to a work laptop through your approved mechanism; no source checkout or Git history travels with it. Updates are explicit: download a chosen new version and rerun with `--replace`. Recognized Python-era installations can be upgraded to Node without modifying stored handoffs. Unknown layouts/versions and unexpected file types are rejected to preserve local files. The installer never reads runtime records.

## Optional npx installation

Self-contained, platform-specific skill ZIPs are also built. Vercel's `skills` CLI supports direct archive URLs, agent selection, and copy mode. Once published and validated, a ZIP can be installed using:

```sh
npx skills add RELEASE_ZIP_URL --global --agent codex --copy
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

Default store: `~/.local/share/a-stack`, outside source/application checkouts. Override with `ASTACK_DATA_DIR` or `--data-dir`. Choose a genuinely local private directory rather than a cloud-synced folder. Store directories/files have user-only permissions. Worktrees share identity; separate clones remain isolated unless explicitly linked. Existing schema-v1 records and project IDs remain compatible with the former Python helper. The legacy `.relay.lock` filename is retained solely for store compatibility; the tool is called Handoff.

The helper makes no network calls. Local Git metadata reads deny transport protocols and lazy fetching. A cloud-backed agent can still send read context to its configured model provider; fully offline model processing requires a local agent/model. Containers require a store mount, and hosted agents without local filesystem access cannot use this store.

## Develop

Development requires Node 22+, a C compiler, and locally available Node headers. Compiled Node-API artifacts work across supported Node versions on the same platform/architecture. Building never downloads headers or dependencies. If the header location is unusual, set `ASTACK_NODE_HEADERS` to the directory containing `node_api.h`.

```sh
npm run build:native
npm test
node tools/build-release.cjs --output-dir /path/to/artifacts
node tools/install.cjs --target /path/to/test-agent/skills
```

There are no npm dependencies or install scripts. The release builder emits a standalone installer, a self-contained skill ZIP, and SHA256 checksums for the build platform. Checksums detect mismatch/corruption; hashes from the same release host are not an independent publisher signature.

[Record schema](schema/handoff.schema.json), [command/storage reference](docs/handoff.md), [validation evidence](docs/validation.md), [installation research](docs/installation-research.md), and [development/review workflow](docs/development.md).

Devin and independent review concern development of this repo; they are not dependencies for using the installed skills. Runtime handoffs, real work context, credentials, and scratch review data must never enter source, releases, tests, or diagnostics.
