# Development and review

Keep a-stack lean and host-neutral. Work records belong outside source. Source development can use Git; installing on another laptop requires only the released Python installer or self-contained skill archives.

1. Check local status and the current upstream base; preserve unrelated work. Use a branch for changes. Read AGENTS.md, REVIEW.md, the relevant source, and record contract.
2. Implement the requested behavior and meaningful regression checks. Run `python3 -m unittest discover -s tests -v`; validate changed skill frontmatter. Build/test release artifacts when installation or packaging changes.
3. Commit a reviewable checkpoint and open a PR. State the concrete behavior, tests, and limits. CI runs the standard-library suite on macOS and Linux with supported Python versions.
4. Have a separate agent review the exact base/head diff. It must inspect source, independently check material failure cases, and report APPROVE or REQUEST CHANGES, the reviewed SHA, actual model when known, checks, and limitations. The implementation agent addresses findings; the reviewer rechecks the new head.
5. Wait for Devin Review on the ready PR and each updated head. Inspect bugs/security findings and investigate relevant flags. Fix confirmed issues and request another review if auto-review did not run. Manual trigger: post exactly `/devin review` on the open PR when the existing Devin GitHub App covers the repo. Verify a completed result for the actual head; posting the command is not completion.
6. Merge only after current-head independent approval, passing CI, and the requested Devin review is complete. If access or review is unavailable, keep the PR open and identify that boundary. Update validation evidence. A release is a separate step: publish artifacts built from the reviewed, merged source and verify their checksums/install behavior.

Devin automatic review is an account-side repository enrollment, not a GitHub Actions script. REVIEW.md is in its default instruction discovery path. The desired cadence matches Chief: every push after the PR is ready. Setting up review does not authorize enabling auto-fix, changing billing limits, or extending permissions to unrelated repositories. See [Devin's official review documentation](https://docs.devin.ai/work-with-devin/devin-review).

No deployment server, background service, or application release machinery is needed. Release `a-stack-install.pyz`, the self-contained skill ZIP, optional source archive, and SHA256SUMS. Build with `python3 tools/build_release.py --output-dir /path/to/artifacts`. Do not include runtime handoffs, scratch review artifacts, or credentials.
