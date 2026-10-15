---
name: ship
description: Merge an approved PR and carry it through release to verified delivery — exact-head merge, release watch by exact SHA, version/tag and release record, final report. Use when a PR has current-head independent approval and passing checks, or when asked to merge, release, deploy or "ship" a change.
---

# Ship: merge → release → verify → record

A task ends with verified delivery or a specific recorded blocker. "After merge I'll watch it" is incomplete unless you actually watch it, or leave an explicit blocked handover.

## Preconditions

All of these must hold for the **current** PR head:

- An independent APPROVE for this exact SHA (see `independent-review`).
- Required checks pass. Any requested bot review, such as Devin, is complete and its findings are dispositioned.
- Main has been fetched just now. Relevant upstream changes are incorporated and affected checks rerun. If incorporating them changed the head materially, it needs a delta review.
- Merging is authorized, either by a standing authorization in the repository bindings or by the user for this task. Never merge a deferred branch or another agent's unfinished work as a shortcut.
- Operator-mediated changes (migrations, infrastructure, secrets) have their procedure ready, and the PR says so.

## Merge the exact head

```sh
gh pr merge <N> --squash --match-head-commit <FULL_HEAD_SHA>   # merge style per bindings
gh pr view <N> --json mergeCommit -q .mergeCommit.oid
```

Never use an admin bypass, weaken branch protection or switch to alternative APIs to get around a refusal. If the merge fails, report the exact error. If you lack merge rights, leave the PR ready and say clearly that it needs merging.

## Release and verify

- Follow the repository's bound release path. Watch the runs that this merge SHA triggered, for example with `gh run list --commit <SHA>` and then `gh run watch <ID> --exit-status`. Match each run to its SHA and time before trusting it.
- Use the repository's release-status or receipt check for the **exact merge SHA**. Pending is not success, and an authentication error is a failure.
- If a release was superseded by a newer main, verify that the newer main contains the change and check that commit's evidence instead.
- If the release was refused because the runtime was busy, retry when it is idle. Never cancel user work to force it.
- If the release was refused because an operator change is pending, run or hand off the reviewed operator procedure promptly. Until it runs, later releases may be blocked for everyone.
- Health at startup is not functional acceptance. Name the behavioral checks that remain.

## Version, tag and release record

When the repository versions its releases, follow its policy (for example, patch-only increments unless the owner changes the policy). Check the published tags just before choosing a number, because parallel sessions take numbers too. Bump the version files in the PR before merging, without creating a local tag (for example `npm version patch --no-git-tag-version`).

Tags are immutable and go only on verified shipped commits. Don't tag documentation-only commits, failed candidates or checkpoints. Never move or reuse a tag to disguise a failed release. Publish against the explicit verified SHA, never the moving branch head:

```sh
gh release create vX.Y.Z --target <FULL_DEPLOYED_SHA> --title "vX.Y.Z — <title>" --notes-file <notes.md>
```

A GitHub Release records a shipped milestone. It is not evidence that production still runs that version.

Release note template:

```
## Released vX.Y.Z — <short title>
<PR link> — <what changed for users/operators>. Exact-head review (<reviewer/model>), <checks>.
Release <run link> verified <full deployed SHA>; <health/diagnostics evidence>. Remaining: <limits or acceptance checks>.
```

## Close the records

Update the journal entry (see `journal`) with its release closure, the work index and handover status, and the release notes. If verification was unavailable, record the exact boundary and next step instead of a release claim.

## Final report to the user

PR, reviewed head, merge SHA, deployed SHA and its evidence, checks, what remains unverified, and any blockers. Each item is labeled as measured, tested or pending.
