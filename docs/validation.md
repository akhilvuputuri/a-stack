# Validation status

## ios-design reader theme scope — 13 October 2026

- **Change:** follow-up to the HIG pass, from the reviewer's optional suggestion. `content-apps.md` now names scoped ways to apply a reading theme's interface style:
  - SwiftUI `.environment(\.colorScheme, …)` with `.toolbarColorScheme(_:for:)`
  - `.preferredColorScheme` only inside a sheet's content
  - UIKit `overrideUserInterfaceStyle` on the reader's own view controller
- **Pitfall:** it warns that a window-wide `.preferredColorScheme` or root `overrideUserInterfaceStyle` restyles the whole app.
- **Checklist:** a new item requires the system style to return after leaving the reader.
- **Checks:**
  - `ApiProbe.swift` covers these APIs and typechecks against the iOS 26.2 simulator SDK.
  - `quick_validate.py` passes.
- **Not verified:** the scoping behaviour comes from Apple's API documentation and was not observed in a simulator.

## ios-design HIG pass — 13 October 2026

The first version drew on Apple's Liquid Glass overview and secondary sources, not the Human Interface Guidelines themselves. This pass read the HIG directly:
- **Source:** Apple serves the HIG as structured page data. All 173 pages were fetched into a scratch directory, outside the repository.
- **Coverage:** the 95 pages relevant to iOS and iPadOS were read. Subsections specific to macOS, tvOS, visionOS and watchOS were dropped. The core pages were read in full; minor control pages were read through their rule statements.

New references: `hig-foundations.md`, `hig-components.md`, `hig-writing.md`, and `hig-system.md`.
- They paraphrase the guidance, with only short example quotations, and link each section to its HIG page.
- Every linked page slug exists in the fetched set.
- The Dynamic Type table was transcribed from the HIG's typography specifications.

Corrections to earlier guidance:
- **Chevrons:** the HIG prescribes disclosure indicators for drill-in rows, so they are no longer described as optional.
- **Undo:** an Undo affordance should not auto-dismiss on a timer, because the HIG asks to minimize time-boxed UI.
- **Popovers:** they are discouraged in compact width, so iPhone typography controls use a medium-detent sheet.
- **Appearance:** app chrome should follow the system light/dark setting. The HIG discourages app-specific appearance settings; reading themes remain acceptable for the reading surface.
- **Principles:** Apple's current eight principles replace the older framing as the primary HIG summary.

Checks:
- `ApiProbe.swift` now also covers the following, and typechecks against the iOS 26.2 simulator SDK:
  - paging scroll behavior, presentation detents, drag indicator, compact adaptation
  - `dynamicTypeSize.isAccessibilitySize`, `requestReview`, `undoManager`
  - standard materials, `widgetAccentable`, `ContainerRelativeShape`, `SiriTipView`
  - `confirmationDialog`, `UIBarButtonItem.Style.prominent`
- `quick_validate.py` passes, internal reference links resolve, and `npm test` passes 36/36.
- Not done: no behavioral re-evaluation of the revised text, and no simulator rendering checks.
- Independent review of `374bb19` (separate Claude Opus 5.5 subagent): **REQUEST CHANGES**.
  - **What it checked:** about 70 claims against the fetched HIG text, all 33 cells of the Dynamic Type table, an 8-word overlap scan for copying, the probe, links, and tests.
  - **Blocking finding:** `hig-foundations.md` reintroduced Increase Contrast as a fallback, contradicting the default-settings contrast rule.
  - **Low findings:** paging overlap isn't provided by `.paging`; "don't" was overstated where the source says "reduce"; and minor wording issues.
  - **Status:** all fixed in the follow-up commit, which needs renewed review.
- Re-review of `0f69476`: **APPROVE**.
- Devin Review flags, read in the Devin app because they were not posted to GitHub:
  - **Contrast fallback:** already resolved.
  - **Theme conflict:** reading themes vs. chrome matching. A sepia page in Dark Mode couldn't satisfy both rules. Now the reader screen takes its interface style from the theme's luminance, and the rest of the app follows the system.
  - **Stale inventory:** an earlier entry here still said four references. Fixed.
  - Both fixes need renewed review.

## ios-design skill — 13 October 2026

`skills/ios-design` is an instruction-only skill (at that time, SKILL.md plus four references; the HIG pass above brought it to eight); it has no helper, runtime, or store access, and it is not part of the Handoff release installer. Install it by copying the folder. Its runtime environment is whatever agent loads it; only the checks below were performed.

- Frontmatter/naming: the skill-creator `quick_validate.py` passes for `ios-design`, `publish-handoff`, and `resume-handoff` (Python 3.13 with a pre-installed PyYAML).
- API names: `evals/ios-design/ApiProbe.swift` uses the iOS 26-specific SwiftUI APIs the references name (plus several older ones) and typechecks against the iOS 26.2 simulator SDK (Xcode on macOS 26.1). The probe caught an error copied from Apple's overview: `ToolbarContent.hidden(_:)` is unavailable on iOS, so the reference now recommends conditional toolbar content. Behavioral claims about iOS 26 rendering (row padding, scroll edge effects) come from Apple's "Adopting Liquid Glass" overview and were not observed in a simulator.
- Fixture: `evals/ios-design/EpisodeLibrary.swift` is synthetic, typechecks at an iOS 26 target, and fails at its stated iOS 17 target only on the intentionally ungated `glassEffect`.
- Behavioral evaluation: a separate Claude Opus 5.5 subagent loaded the skill and ran the `full-audit`, `narrow-change`, and `glass-everywhere` cases in isolated scratch Git workspaces. All include/exclude criteria were met on that earlier draft; the final text has not been re-evaluated behaviorally. The audit left its workspace unchanged, the narrow change was a one-line title edit, and the glass request produced an explanation with a native alternative and no edits. No simulator, VoiceOver, or screenshot checks were run. The evaluator's critique led to these changes: an explicit rule for requests that conflict with the principles, a narrower P0 definition with grouping, a shorter finding format, side-effect disclosure for narrow edits, a neutral (non-serif) text-style example, "verify before mirroring" wording for VoiceOver swipe actions, contrast required at default settings, a `scrollContentBackground` note for themed lists, and a typecheck/preview fallback when no runnable project exists. The `sepia-theme` and `screenshot-only` cases were not run.
- `npm run build:native` and `npm test` (36/36) pass locally on macOS arm64; no helper code changed.
- Independent review (separate Claude Opus 5.5 subagent) of `2ff7e8e`: REQUEST CHANGES. It found a probe-coverage overstatement, a missing "earlier draft" caveat, and a principles line contradicting the no-duplicate VoiceOver guidance. It also raised low-severity notes on web-view CSS (`viewport-fit=cover`, `font` shorthand order, prefixed hyphens), the large-text contrast cut-off, the swipe-edge convention, the Liquid Glass setting location, and a fixture comment that revealed a graded defect. The follow-up commit addresses all of them and needs renewed review.
- Re-review of `afc5cf2`: APPROVE, with one non-blocking wording nit (Undo or confirmation). Devin Review on `afc5cf2` flagged that "or bold" let small bold text pass at 3:1; the contrast rule now follows WCAG AA's 14 pt bold cut-off. That commit and the nit fix need renewed review.

## Current Node-only candidate — 6 October 2026

Handoff 0.1.2 now runs on Node 22+ with a bundled filesystem addon. The Python results below are retained historical evidence, not approval of the Node port. The current native build explicitly targets macOS 11+; Linux CI builds on Ubuntu 22.04 for a glibc 2.35 baseline. Older-OS loader execution and musl/Alpine support are not established.

The Node port has 36 grouped tests passing locally on macOS arm64 / Node 22.15.0. [CI run 37457918337](https://github.com/akhilvuputuri/a-stack/actions/runs/37457918337) passed all six jobs at `cc242d6fa9528062ceef602ade39b332be46c9ac`: macOS arm64, macOS Intel, and Linux, each on Node 22 and 24. The build-floor/documentation follow-up requires refreshed current-head CI and review; passing older-head checks do not approve it.

A separate GPT-6 Astra reviewer approved the native/installer/release scope of `cc242d6`, independently passing all 36 tests plus 1,000 native boundary/resource cycles with stable open-descriptor counts and an unchanged outside sentinel. It identified the implicit build-host macOS floor as a compatibility limitation; the follow-up sets `-mmacosx-version-min=11.0`, verified locally with Mach-O `LC_BUILD_VERSION minos 11.0`. Full implementation review remains pending on the final head.

An independent skill evaluation used the installed Node publishing and receiving helpers on synthetic mixed-topic context. It saved only the duplicate-reply investigation, retained rejected approaches and uncertainty, excluded unrelated content, and resumed for orientation without code/status/record mutation. No Python or network operations were used. Freshness remained unverifiable for unavailable code/logs.

An isolated `npx skills` installation attempt with npm version 1.5.18 did not support the direct localhost archive route described by repository main: it sought a well-known discovery endpoint and found no skills. The direct Node installer is tested; npx archive installation remains unverified and is not advertised as a working supported route. No registry package for a-stack was published.

Devin enrollment and public release publication remain pending owner confirmation of the prepared repository-specific GitHub App access. No runtime usage depends on Devin. Native OS-level egress isolation and actual host automatic skill discovery remain unverified.

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

## Independent code review and v0.1.1 candidate

On 2 October 2026 a separate Codex agent reviewed initial commit `2dee350252e1102a46beaa744776abdaee299b3a`, including the full helper, installer, packager, schema, skills, docs, and tests. Its model identifier was not exposed. It independently ran all 34 original tests and reproduced four defects using synthetic scratch data:

| Finding | Resolution in this candidate |
| --- | --- |
| P1: Git status ran a repository-configured clean/process filter | Replace working-tree Git status with index metadata and raw-byte blob comparisons; skip submodule working-tree checks with a recorded limitation. Regression checks inspect and resume-state comparison for both driver types. |
| P2: Code file leaves could be directories, then deleted on replacement | Require regular files at expected leaves; preserve and reject unexpected directories. Test all affected leaf locations. |
| P2: Linking could race publication and hide a successful record | Serialize store resolution/mutation with a private store lock. A draft prepared for an old identity is rejected intact after a link. Test a paused link against a competing publication. |
| P2: Mapping chains split previously linked projects | Resolve chains transitively and validate cycles. Test shared retrieval through a chain and rejection of a malformed cycle. |

An additional installation reviewer was unavailable after capacity errors; its preliminary source-path observations motivated rejection of source symlinks and symlinked ancestors in installation/packaging. These changes remain in the final re-review scope.

The first v0.1.1 candidate had 43 passing tests on Python 3.12.14 and 3.14.7. New setup checks execute the one-file Python installer with no Git on PATH and networking disabled by the Python tripwire, verify independent installed helpers, preserve published bytes during an update from a v0.1.0 marker, inspect regular self-contained ZIP contents and SHA256SUMS, reject symlinked source ancestors, and verify agent destination shortcuts. This tests installation without cloning or source checkout; actual work-laptop host discovery remains unverified.

AGENTS.md now requires an independent implementation review and exact-head verdict, plus CI and requested Devin review before merge/release. REVIEW.md defines the applicable boundaries; docs/development.md records the process. Current-head re-review, GitHub CI, and actual Devin enrollment/completion are pending for this candidate and must be recorded on its PR. Repository instruction files alone do not enable Devin's account-side integration.

The independent reviewer returned REQUEST CHANGES for candidate `88cf15cbb7c92879a2392874278cca9a79cb6ce7`. It independently passed all 43 tests and verified resolution of the installation deletion and both project-linking defects, but reproduced two remaining P1 filter boundaries: valid driver names containing `=` bypassed command-line overrides, and a driver added between enumeration and status escaped overrides. Environment key/value pairs addressed the first case; the final approach removes the enumeration/status check/use sequence entirely in favor of raw byte comparisons and metadata-only Git commands. Regression cases retain both triggers plus staged, deleted, untracked, and symlink changes. Final-head re-review is required; this history preserves the rejected candidate rather than treating passing tests as approval.

Review of follow-up `b96820cd6ff99addd385f90bdd2e8fa53424db81` independently passed 46 tests and confirmed both filter triggers were resolved. The reviewer still returned REQUEST CHANGES after reproducing lazy promisor fetching through a cached comparison and an escaping-parent swap during a raw read. The next candidate denies all Git transport protocols and lazy fetching, and holds no-follow directory descriptors through the tracked file open. Synthetic regressions use an inert remote-helper canary and prove the outside inode is not opened or incorrectly treated as clean. All 48 tests pass locally on Python 3.14.7; exact-head independent re-review remains required before merge/release.

The independent reviewer returned **APPROVE** for exact implementation head `f5563313d01c10b84fb2ec0d4ead2bc064297d26`, with no actionable findings remaining in its scope. It independently passed all 48 tests and retested permissive/inherited promisor configuration, parent swaps before traversal and final open, leaf symlink replacement, and the earlier equals-named filter. No remote canary ran, outside inodes were not opened, dirty paths stayed visible, unavailable metadata remained explicit, and records stayed unchanged. [Recorded review verdict](https://github.com/akhilvuputuri/a-stack/pull/1#issuecomment-5936803385).

[GitHub CI run 36898791472](https://github.com/akhilvuputuri/a-stack/actions/runs/36898791472) passed all four jobs at that exact implementation SHA: macOS/Linux with Python 3.11/3.14, including release-artifact builds. This supersedes the initial platform table's unverified Linux/minimum-Python status for helper execution. Automatic host skill discovery and native OS-level egress isolation remain unverified. This follow-up changes validation/README evidence only; current-head approval remains required on the PR.

Devin enrollment is a separate, pending account-side step. The existing GitHub App selected only Chief; adding a-stack would expand its write access to this repository and requires the owner's permission confirmation. The repository-specific change is prepared, not saved. No completed Devin review or public v0.1.1 release is claimed while that step is pending.

## Node-only Handoff port — 6 October 2026

Candidate 0.1.2 replaces the Python runtime, installer, tests and builder with JavaScript executed by Node 22+. The helper is now Handoff. The schema remains v1, existing project IDs/store layout remain compatible, and the legacy lock filename is retained for cross-version coordination. Recognized Python installations can update to the new code without reading runtime handoffs.

Node lacks openat/flock in its built-in filesystem API; the release bundles a small Node-API C addon for descriptor-relative no-follow traversal, atomic no-overwrite linking, directory reads and store locking. Development/CI compiles it with local headers and a C compiler; installed users need only the matching Node release artifact. No automatic compiler/header/dependency downloads are present.

The initial port passes 36 grouped Node tests on macOS arm64 / Node 22.15.0, including prior reviewed failure triggers, legacy-record compatibility, input/schema/evidence rejection, revision conflicts, mapping/locking, process interruption, private permissions, symlinks, raw inspection, Git filters and promisor prevention, installation preservation, and independent installed producer/receiver helpers. The standalone installer and usage ran with an empty PATH and a Node network tripwire: no Python, Git, compiler or source checkout was available through PATH. Test group counts differ from the Python suite and do not imply one-for-one test equivalence.

Native OS-level egress isolation, actual target-agent discovery and npx archive installation remain unverified. Node current-head independent review and CI are pending; previous Python approvals do not cover this port. Devin access/enrollment is still pending owner approval and is not a requirement for using the installed skills. Release publication remains pending those requested development review gates.
