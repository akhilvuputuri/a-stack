# a-stack

Akhil's small collection of reusable coding and AI workflow skills. Start with **Relay**, a local handoff workflow: save the context for one task, then pick it up in another local agent session.

| Skill | Use |
| --- | --- |
| `publish-handoff` | Select one topic, draft/save a local handoff, or publish an updated revision. |
| `resume-handoff` | Retrieve/list handoffs, recheck relevant state, and explain the next step. Implement when the user asks. |

Relay uses Python 3.11+ and only the standard library. Its tests and installed-helper checks run on macOS and Linux in CI; target-agent discovery still needs verification in your environment. Windows is not supported in v0.1. No pip install, TypeScript, npm, daemon, database server, MCP server, telemetry, or remote handoff storage is required. New skills can be added independently of Relay.

## Install on another laptop without Git

Download [a-stack-install.pyz](https://github.com/akhilvuputuri/a-stack/releases/download/v0.1.1/a-stack-install.pyz) from the v0.1.1 release, then run:

```sh
python3 a-stack-install.pyz --agent codex
# Or:
python3 a-stack-install.pyz --agent claude-code
```

The file contains both skills and all their runtime files. It installs user-scoped copies and cleans up temporary staging. No clone, Git history, pip, npm, or build is needed. Python 3.11+ must already be available. The downloaded installer runs with networking disabled, so you can transfer the same file to a work laptop that cannot reach GitHub.

Optional terminal download:

```sh
curl -fL --output a-stack-install.pyz https://github.com/akhilvuputuri/a-stack/releases/download/v0.1.1/a-stack-install.pyz
python3 a-stack-install.pyz --agent codex
```

The release also contains SHA256SUMS for local verification (`shasum -a 256 a-stack-install.pyz`), self-contained skill ZIPs for archive-based installers, and an optional source archive. For an explicit code update, download the selected release and rerun with `--replace`. Your handoff data is preserved. [Installation research and tradeoffs](docs/installation-research.md) explain the choice.

## Custom folders and local source

Use the skill-discovery directory supported by your chosen agent. The installer requires an explicit target and can install either skill independently. Each installed skill includes its own Relay runtime, schema, and reference; it has no dependency on a sibling skill or on this source checkout.

```sh
python3 /path/to/a-stack/tools/install.py --target /path/to/agent/skills
# Or just one:
python3 /path/to/a-stack/tools/install.py \
  --target /path/to/agent/skills --skill publish-handoff
```

For example, current Codex documentation lists `~/.agents/skills` for user-scoped local skills. Other agents may use different locations or invocation syntax; choose the target they document. Agent compatibility must be verified separately. [Official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills)

```sh
python3 /path/to/a-stack/tools/install.py --target "$HOME/.agents/skills"
```

The source skills link to shared runtime/reference files for development. Installation copies those files into self-contained skill directories. For a code-only update of a recognized v0.1 installation, repeat the installer with `--replace`. Unknown versions and unexpected file types are rejected rather than silently migrated or removed. The installer never opens your runtime handoff data.

## Local data

By default handoffs live in `~/.local/share/a-stack`, outside both this repo and application repos. Choose a private local filesystem location, especially at work:

```sh
export ASTACK_DATA_DIR=/local/private/a-stack
```

The helper creates user-only directories/files and rejects unsafe paths or public store permissions. Avoid cloud-synced folders; the tool cannot detect every sync product. Store project identity is based on canonical local roots/Git common directories. Worktrees share a project; separate clones do not unless explicitly linked.

## Try it

With the skills installed, use natural language:

- “Publish a handoff for the retry bug only.”
- “Draft a handoff for the duplicate reply investigation.”
- “Update handoff H with today's findings.”
- “List handoffs for this project.”
- “Resume handoff H.”
- “Resume handoff H and implement the fix.”

The publishing agent returns a stable handoff ID, unique revision ID, and local path. Another local agent with access to the same data root can retrieve the record without copying JSON manually. Host-specific slash aliases are optional; no universal slash command is assumed.

“Publish” means **save locally**. An issue URL is optional text metadata. A handoff records context and references; it does not copy code, reset a checkout, or prove the recorded findings are current. Competing updates remain visible and require a choice or explicit reconciliation.

The helper adds no network operations. A cloud-backed host agent may still send read context to its model provider under its own configuration. Fully offline model processing requires a suitable local agent/model. Containers need an explicit store mount; cloud-hosted agents without local filesystem access cannot use this release.

## Develop and package

```sh
cd /path/to/a-stack
python3 -m unittest discover -s tests -v
python3 tools/relay.py --help
python3 tools/package.py --output /path/to/a-stack-source-0.1.1.tar.gz
python3 tools/build_release.py --output-dir /path/to/release-artifacts
```

Packaging uses an explicit generic-source allowlist and never opens the handoff store. Transfer the package to a work machine through your permitted mechanism, extract it, and run the same local installer with networking disabled. Python must already be available; nothing is downloaded automatically.

The repository contains only synthetic test/evaluation content. Real handoffs must stay outside the repo, releases, examples, tests, and diagnostics. The authoritative format is [schema/handoff.schema.json](schema/handoff.schema.json). Command details, record fields, storage guarantees, and limitations are in [docs/handoff.md](docs/handoff.md). Actual checks and compatibility are in [docs/validation.md](docs/validation.md).

No GitHub publishing, remote sync, automatic updates, background transcript capture, autonomous dispatch, or code transfer is included in this initial release.

Repository development follows [the independent review and Devin workflow](docs/development.md). Local handoff operations remain separate from GitHub development/release work.
