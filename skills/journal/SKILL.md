---
name: journal
description: Write or update the engineering journal entry for a meaningful change, incident, integration, architectural decision or experiment, and close it with release evidence. Use in the same PR as any such change, after a release to record its closure, or when setting up a journal in a repository.
---

# Engineering journal

The journal connects implementations, incidents, experiments and releases into a dated record of how decisions evolved. A fix that passes its own checks can expose the next failure, so keep that sequence visible. The repository bindings give the journal path (default `docs/journey/`).

## When to write

Write an entry in the **same PR** as every meaningful application change, integration, incident, architectural decision or experiment. Small related changes can be dated follow-ups in an existing entry. Every technical improvement must be recallable later: what changed, how it works, what was measured, what review found.

Alongside the entry, update in the same PR:

- the relevant design doc or runbook section (link to it, don't duplicate it)
- the work index or handover status (for example `docs/current-work.md`)
- the journal index

## Entry

Copy [the template](template.md) to `<journal>/NN-short-slug.md`.

- Choose `NN` by checking the highest number **on freshly fetched main and in open PRs**, because parallel sessions take numbers. Never renumber existing files.
- Title the entry with a concrete engineering question, for example "Why can a durable task still forget its scope?".
- Add a row to the index (`<journal>/README.md`), ordered by **work date**, not entry number. If the journal doesn't exist yet, create `<journal>/README.md` from [the index template](index-template.md) and copy [the entry template](template.md) to `<journal>/TEMPLATE.md`, which the index links to.

## Evidence rules

- Label every claim as **reported** (user or operator said), **tested** (synthetic or regression test), **measured** (observed with numbers), **hypothesis** or **deferred**.
- A measurement states its date or window, collection method, sample size, units, model and configuration, workload, and any missing accounting.
- Don't infer savings from storage or token counts, quality from passing tests, production acceptance from startup health, or cause from chronology.
- Keep failed checks, negative results and each review round (date or SHA, finding, correction, final exact-head verdict).
- Never copy private conversations, production traces, user records, credentials or personal motivations. Store sanitized aggregates and link to safe inspection procedures.

## Release closure

When review or deployment status changes, append a dated `### Release closure — YYYY-MM-DD` section. It records the PR, the approved head, the merged and deployed SHA, the successful release run, health or diagnostics evidence, and the version or tag when there is one. Record operator migration or install verification separately when it was required. Then update the entry's Status line and the index row.

A merge, CI success or a prepared version alone does not establish a release. If verification is unavailable, record the exact boundary and next step instead.

## Cumulative lessons (optional)

For a long-running area such as an agent harness, the repository may keep a cumulative lessons guide next to the journal. Append a dated case in the same PR covering the trigger, baseline, observation, hypothesis, intervention, counterexample or review correction, outcome, and the next small test that could falsify the benefit. Distinguish an implemented mechanism, a passing regression, a verified deployment and a demonstrated real-task benefit.
