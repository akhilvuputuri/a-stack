# Development and review

Keep a-stack lean and host-neutral. Handoff runtime records belong outside source. Users install a platform release with Node only; developers build the bundled filesystem addon using a C compiler and local Node headers.

1. Check local status and the current upstream base; preserve unrelated work. Use a branch. Read AGENTS.md, REVIEW.md, relevant source, and the record contract.
2. Implement behavior and meaningful regression checks. Run `npm run build:native` and `npm test`; validate changed skill frontmatter. Build/test released artifacts when setup changes. No automatic header/package downloads.
3. Commit a checkpoint and open a PR. Explain resulting behavior, tests, and limits. CI builds/tests on macOS/Linux, Node 22/24, and publishes per-platform artifacts for inspection.
4. A separate agent reviews the exact base/head diff, including addon/native calls when affected. Require APPROVE or REQUEST CHANGES with actual checks, concrete findings, and limitations. Fix findings and obtain renewed review at each material head.
5. Wait for Devin Review on the ready PR and updated heads; investigate current-head findings. The existing GitHub App must cover the repo. Manual trigger: `/devin review`. Posting a trigger/enrollment is not completed review.
6. Merge only after current-head independent approval, passing CI, and the requested Devin review. If integration is unavailable, leave the PR open with the boundary. Release publication is separate: build artifacts from the reviewed merged source and verify checksums/install behavior.

REVIEW.md is Devin's default instruction discovery filename. Desired auto-review cadence matches Chief: every push after readiness. Do not enable automatic code edits, change billing settings, or expand unrelated repository access. [Official Devin review docs](https://docs.devin.ai/work-with-devin/devin-review).

Release `a-stack-install-PLATFORM-ARCH.cjs`, `a-stack-skills-VERSION-PLATFORM-ARCH.zip`, and `SHA256SUMS-PLATFORM-ARCH`. CI artifacts are candidates, not a published release. Source skill helper references are development symlinks; the release folders contain actual helper/schema/addon copies. Tests use synthetic data only. No runtime store content is packaged.
