# Validation status

Checked on 2 October 2026 (Asia/Singapore), using macOS 26.1. All data used for these checks is synthetic. No real work handoffs are in this repository or its bundle.

## Deterministic helper checks

34 tests pass on Python 3.12.14 and 3.14.7:

```sh
python3 -m unittest discover -s tests -v
```

Coverage includes schema/evidence validation, unknown schema rejection, malformed JSON, duplicate keys, private permissions, traversal and symlink rejection, store/source separation, interrupted writes and retries, concurrent same-ID writes, competing successors and explicit reconciliation, missing predecessors, cycles and long revision chains, project isolation, worktree sharing, explicit clone mappings, Git environment/fsmonitor defenses, relevant dirty-state inspection, changed commits, draft/list separation, read-only export, preserved inputs and prior successful writes after failures, code-only updates, preservation of unexpected installation files, allowlisted packaging, and independently installed producer/receiver helpers in fresh processes.

Each child Python helper process runs with a test-only audit hook that rejects all `socket.*` operations and records any attempt. A canary test confirms the hook blocks network use. Actual helper operations produced no Python socket attempts, including operations storing issue URLs as metadata. Git commands are local metadata reads; fsmonitor execution is explicitly tested as disabled. Local-clone setup in tests uses filesystem paths only.

OS-level network denial could not be independently enabled in this host: `sandbox-exec` returned `sandbox_apply: Operation not permitted`. Python socket isolation is verified; native-process network isolation/attempt capture is not verified here. Re-run the suite in a host/container with egress disabled before claiming the PRD's full OS-level offline release gate. No extra network mechanism or permissions were added to bypass that limitation.

Both skill folders pass the bundled skill-creator `quick_validate.py` frontmatter/naming/scaffold validator. Its YAML dependency came from an already cached development library; Relay and its installer remain standard-library-only.

## Behavioral checks

An independent agent used the installed publishing skill on the synthetic three-topic conversation. It saved only the duplicate-reply task, retained the later rejection of the in-memory flag, marked retry/restart behavior uncertain, recorded missing raw logs/code and no tests, and generated no implementation. It used the installed resume skill to retrieve the record, report unverifiable freshness, and leave stored bytes unchanged.

That first pass named excluded topic titles in a scope boundary. The publishing instruction was tightened to describe selected scope in the record and keep excluded title acknowledgments in the receipt. The independent follow-up exercised six isolated cases with the updated installed skills:

| Case | Observed result |
| --- | --- |
| Selected duplicate-reply task | One scoped record; excluded topic titles remained outside the record; correction, uncertainty, constraints, and next action retained. |
| Conversational “issue 2” | Calendar topic selected; no GitHub number assumption. |
| Draft only | Rendered private draft; published list empty. |
| Two selected topics | Two distinct handoffs, each with isolated topic context. |
| Repository-qualified issue reference | `example/repo#42` retained literally as metadata; no external retrieval. |
| Ambiguous selection among three topics | One focused clarification proposed; no published record. |

The follow-up produced five handoffs across isolated case stores, with distinct project IDs. Resume retrieved the selected record and preserved record/status/project bytes. The evaluator reported no further deviations, no implementation, no invented acceptance criteria or test passes, and no network calls. These are qualitative agent evaluations of designated facts and exclusions, not assertions that future models will always select context correctly.

A separate receiving agent, given only the handoff ID, project path, data root, and installed resume skill, retrieved the same record without seeing the original conversation or another evaluation report. It recovered the selected goal, constraints, rejected approach, uncertainty, and next action. It made no code/store changes. This demonstrates a handoff between two local agent contexts with shared filesystem access; it does not establish compatibility with different agent products.

## Compatibility

| Environment | Skill loading | Terminal/runtime | Data access | Result |
| --- | --- | --- | --- | --- |
| Local Codex agent evaluation | Installed skill loaded explicitly by path | Python helper commands | Shared private local store | Publish and fresh-session resume demonstrated |
| Python 3.12.14, macOS 26.1 | Not an agent host | Complete deterministic suite | Temporary local stores | 34/34 pass |
| Python 3.14.7, macOS 26.1 | Not an agent host | Complete deterministic suite | Temporary local stores | 34/34 pass |
| Codex automatic skill discovery/UI invocation | Not exercised | Available locally | Not installed globally by this build | Unverified |
| Other local coding agents | Not exercised | Depends on host | Requires shared store access | Unverified |
| Python 3.11 / Linux | Not exercised | Intended minimum/runtime platform | Requires compatible POSIX filesystem | Unverified |
| Windows | Not supported | POSIX filesystem primitives required | — | Unsupported in 0.1 |
| Hosted agent without local filesystem access | — | — | Cannot access this store | Unsupported |

The extracted offline bundle installs both skills without dependency downloads. A separately installed publishing helper creates a record and a separately installed receiving helper reads it in another process. Updating a recognized installation preserves every runtime JSON file byte-for-byte. The bundle contains generic source and synthetic checks only, and uses an explicit allowlist.

The complete 34-test suite also passed from an extracted bundle with the Python network tripwire enabled in the parent test process and helper child processes. The parent reported no unexpected Python network attempts.

Pending broader validation: actual target-agent discovery/permissions, the remaining behavioral fixtures (including implementation against changed code and hostile stored instructions at the agent level), Linux/minimum-Python testing, and native-process egress isolation. Helper-level hostile-text non-execution and changed-state detection are covered. This build is a tested local MVP, not a claim that every PRD deployment environment/release gate has been exercised.
