# Maintaining a-stack

Keep this repository a small collection of reusable, independent skills. Relay is the local handoff helper; new skills need not depend on it.

Use Python 3.11+ standard library only for Relay. Runtime handoffs, drafts, and work context belong outside this repository and application checkouts. Examples and tests must be synthetic. Packaging and installation use explicit source allowlists and never read the runtime store.

The schema is authoritative. Keep the dependency-free validator, renderer, skills, and command documentation consistent with it. Preserve local-only behavior, immutable revisions, explicit conflicts, project isolation, and the boundary between evidence and executable authority.

Run `python3 -m unittest discover -s tests -v` for helper changes. Validate changed skills with the available skill validator. Document actual tested environments; do not infer another agent's compatibility from local helper tests.
