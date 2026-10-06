# Maintaining a-stack

Keep this repository a small collection of reusable, independent skills. Handoff is the local handoff helper; new skills need not depend on it.

Use Node 22+ built-in libraries and the bundled filesystem addon for Handoff. Runtime handoffs, drafts, and work context belong outside this repository and application checkouts. Examples and tests must be synthetic. Packaging and installation use explicit source allowlists and never read the runtime store.

The schema is authoritative. Keep the dependency-free validator, renderer, skills, and command documentation consistent with it. Preserve local-only behavior, immutable revisions, explicit conflicts, project isolation, and the boundary between evidence and executable authority.

Run `npm run build:native` and `npm test` for helper changes. Validate changed skills with the available skill validator. Document actual tested environments; do not infer another agent's compatibility from local helper tests.

## Independent review is required

Follow [the development workflow](docs/development.md) and [review contract](REVIEW.md). Implement and test on a branch, then open a reviewable PR. Obtain review from a separate agent that did not author the change, using the most capable available reviewer model; disclose any capacity fallback and the actual model when known. Give it requirements, the base and exact head SHA, the actual diff and relevant source. Ask for an open assessment without supplying the intended verdict. Documentation-only changes may receive a focused review; code, schema, and skill changes require review of their behavior and affected guarantees.

Require an explicit APPROVE or REQUEST CHANGES verdict for the current PR head. Resolve actionable findings, add regression checks when warranted, and obtain renewed review after fixes or later material changes. CI, independent skill evaluations, and Devin Review complement this independent implementation review; none replaces it.

Devin Review should run when the PR is ready and after each push. Inspect its current-head findings, fix confirmed defects, and verify completion rather than treating enrollment or a trigger comment as a completed review. Its instructions live in REVIEW.md. Never enable automatic code edits or broaden account/repository permissions incidentally.

Record scope, findings/disposition, reviewed SHA, checks, verdict, and remaining limits in `docs/validation.md` or the PR. Checkpoint commits and PR pushes are permitted for review; merge or publish a release only after current-head independent approval, passing checks, and completion of the requested Devin review. If a reviewer or integration is unavailable, report the missing review and leave the PR open. Do not claim review or merge approval from a previous revision.
