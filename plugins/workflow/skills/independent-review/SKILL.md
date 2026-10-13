---
name: independent-review
description: Run the required independent review loop on a PR — brief a fresh reviewer agent on the exact head SHA, obtain an explicit APPROVE or REQUEST CHANGES, fix findings and re-review each new head. Use after implementing any feature, fix or behavior change, before merging. Also use when acting as the reviewer.
---

# Independent review loop

Review is a bounded claim about one exact commit, made by an agent that did not write it. CI, Devin Review and other bots supplement this review and never replace it.

## Before requesting review

1. The implementation and relevant regression tests are complete, and the repository's checks pass locally. Record which ones ran.
2. The branch is pushed and a PR is open. The PR describes the behavior, the validation, the limits and any deployment prerequisites.
3. Record the base SHA and the **full head SHA** (`git rev-parse HEAD` after pushing).

## Spawning the reviewer

- Use a fresh agent that did not author the change, on the strongest model available. The repository bindings name the preferred model; if it is unavailable, use the strongest available one and disclose the fallback. Select the model explicitly when the tool allows it.
- Always run the reviewer in the foreground. Never background it: a backgrounded reviewer can stall until the watchdog kills it. Its own commands must also run in the foreground, as the prompt template requires.
- Fill in [the reviewer prompt](reviewer-prompt.md). Never include the verdict you expect, and never paste secrets or private data into it.
- Point the reviewer at the repository's REVIEW.md when one exists. Otherwise point it at [the review contract](review-contract.md).
- Report the checks you already ran so the reviewer does not repeat the whole suite. It should run targeted checks that could falsify the change.

## Handling the verdict

- **REQUEST CHANGES:** fix each confirmed finding, adding a regression test where it is warranted. Rerun the affected checks and push. Then ask for review of the **new head**: resume the same reviewer for a delta review when you can (for example with SendMessage), otherwise brief a fresh one. Include the previous findings and how each was resolved.
- **Disagreement:** argue with evidence such as a reproduction, a source citation or a test, not by assertion. If the disagreement stands, leave it unresolved and visible, and do not merge over it.
- **APPROVE:** valid only for the exact SHA reviewed. Any later material push needs another review.
- **Reviewer stalled or unavailable:** say so, leave the PR open and ready for review, and do not self-approve.

## Recording

Post or add to the PR (and to the repository's validation or journal record, if it keeps one):

```
Independent review — <reviewer/model>, <date>
Reviewed head: <full SHA> (base <SHA>)
Checks run by reviewer: <list>
Findings: <each with disposition: fixed in <SHA> / disputed with evidence / deferred with reason>
Verdict: APPROVE | REQUEST CHANGES
Limits: <what was not verified>
```

Keep earlier REQUEST CHANGES rounds in the record. Approval of the final head does not erase them.

## Review bots

When the repository uses Devin Review or a similar bot, wait for its result on the current head. Read its findings, fix confirmed defects and note the disposition of each one. A trigger comment or enrollment is not a completed review.

## When you are the reviewer

Follow [the review contract](review-contract.md) and do not implement fixes yourself. End with the recording block above.
