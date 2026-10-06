# Installation research and decision

Researched primary documentation and implementation on 2 October 2026. Goal: install a-stack on a macOS work laptop with existing Python, without a Git clone or build toolchain, and preserve offline runtime/data boundaries. This compares documented behavior; other installers were not executed on the work laptop.

| Collection/tool | Documented installation pattern | Fit for a-stack |
| --- | --- | --- |
| OpenAI skills | Python installer defaults to downloading GitHub archives, selects individual skill folders, and can fall back to sparse Git. | Direct downloads and selective copies suit the requirement; our primary installer has no Git fallback. |
| Vercel skills CLI | `npx skills add` supports selected skills/agents, global or project scope, and copy or symlink installation. Direct archive URLs are supported; ordinary repo paths can use Git/auth fallbacks. | Useful optional distribution channel through a release ZIP, rather than promising that repository shorthand is always Git-free. |
| gstack | Shallow clone plus setup, with Git/Bun prerequisites and host-specific installation. Team mode adds automatic update checks. | Helpful host-selection and quick-start UX; unnecessary build dependencies and runtime update checks for two local skills. |
| Anthropic skills | Self-contained skill folders; Claude Code plugin marketplace registration and selection of a skill collection. | Confirms folder independence and native host discovery. A plugin is optional later; it should not be required for local file handoffs. |
| Vercel Knowledge Base skills | Downloadable `.skill` ZIP assets alongside source/CLI installation. | Strong precedent for downloadable, self-contained artifacts that need no checkout. |

Sources: [OpenAI installer guidance](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md), [OpenAI installer implementation](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/scripts/install-skill-from-github.py), [Vercel CLI](https://github.com/vercel-labs/skills/blob/main/README.md), [gstack quick start](https://github.com/garrytan/gstack/blob/main/README.md), [Anthropic skills](https://github.com/anthropics/skills/blob/main/README.md), [Vercel downloadable skills](https://github.com/vercel-labs/vercel-kb-skills/blob/main/README.md).

## Recommended route

Publish one executable Python ZIP application, `a-stack-install.pyz`. Download it from a versioned GitHub release, then run `python3 a-stack-install.pyz --agent codex` or `--agent claude-code`. A custom target remains supported. The downloaded file includes the installer, both skill entrypoints, runtime, schema, and reference. It installs copies into native discovery folders, using private temporary staging that is removed afterward. No source checkout, Git history, Node/Bun/npm, pip, account token, or network operation is needed to execute it.

The host-neutral core remains unchanged: both installed skills are independent and use one local data root. Agent flags only choose destination directories. Normal automatic skill discovery stays enabled; an installed host still needs terminal/Python access and permission to read the local store. Hosted model use has its own processing boundary.

Also publish a combined skill ZIP with all dependencies inside each folder. It can be transferred through an approved offline mechanism or supplied as a direct archive URL to tools such as Vercel's CLI. Source uses internal development symlinks; distributed skill ZIPs contain regular copied files so they do not depend on the checkout layout. The [Agent Skills specification](https://agentskills.io/specification) defines optional scripts/references as part of the skill directory.

## Updates and practical limits

Choose a fixed release version for predictable work installs. Publish SHA256SUMS and allow local verification. Checksums detect corruption/mismatch; hashes delivered by the same release host are not an independent publisher signature. Updates require downloading a selected new artifact and passing `--replace`; installed code can change while data stays local. There are no automatic update checks or downloads during handoff use.

Download and execution are separate steps, avoiding a shell pipe that executes a partly downloaded script. If the work laptop cannot reach GitHub, transfer the same installer file and checksums, then run entirely offline. Python 3.11+ and a compatible macOS/Linux filesystem remain prerequisites. This design is based on the user's confirmed macOS/Python environment; Windows support remains out of scope.

A plugin marketplace or package registry could be added once a target agent/ecosystem is chosen. Adding one now would introduce account/registry/toolchain assumptions without simplifying the confirmed work-laptop setup. The release ZIP offers ecosystem compatibility while keeping the primary install standard-library-only.

## Node-only decision — 6 October 2026

The user selected a Node-only runtime and renamed Relay to Handoff. This supersedes the Python installer recommendation above while preserving its download-first and self-contained-folder approach. JavaScript is executed directly by Node 22+; there is no TypeScript compiler at runtime. Node's built-in filesystem API does not expose openat or flock, so a small precompiled Node-API addon supplies the reviewed descriptor-relative primitives. Official [Node-API documentation](https://nodejs.org/api/n-api.html) describes its cross-version ABI and distributing precompiled binaries; see [filesystem APIs](https://nodejs.org/api/fs.html) for built-in operations. Release artifacts are platform/architecture-specific, with no compiler needed on the user's laptop.

Both direct Node installation and archive-based npx skills installation use the same skill/helper contents. Direct execution of the downloaded installer stays offline; using an external npm installer has that installer's network/telemetry boundary. Python artifacts are historical and no longer the supported path for the Node release.
