---
name: experiment
description: Run a controlled engineering experiment or evaluation — freeze a baseline, change one mechanism, compare on identical fixtures and graders, and report results without overclaiming. Use when testing whether a change improves agent behavior, quality, cost, latency or reliability, or when designing evals and benchmarks.
---

# Controlled experiments

Use this before claiming that a change "improves" anything. Paid model runs and paid infrastructure need a specific request from the user. This skill never authorizes them.

## Method

1. **Constrain the question.** Name the failure, the single mechanism you will change, the metric, and what result would falsify the benefit. Keep the scope small, and broaden only after a clean comparison.
2. **Freeze a baseline before changing code.** Record the exact source SHA or image, fixtures, grader version, model and provider, effort, allocations and context settings. Fingerprint the fixtures and grader. If the runner changes too, review its diff as well.
3. **Make deterministic checks first.** Cover identity, scope, coverage, authorization and format. Humans judge whether the reasoning is supported and useful. Keep these two kinds of review separate.
4. **Run in isolation.** Use a fresh database or workspace with controlled tools. Never place test prompts in production history, where they can later be mistaken for user instructions.
5. **Change one mechanism and repeat** the same scenarios with the same graders. Hold the models fixed for harness trials and the harness fixed for model trials.
6. **Inspect full traces** of both failures and successes. Fix integration bugs that a trace exposes, and record that they were found that way. Never change expected answers to make a candidate pass.
7. **Run held-out variations** before making broader reliability claims.

## Reporting

- One stochastic run is one run. A few repeated trials are diagnostic, not statistical proof. Report the counts, not "works now".
- Keep infrastructure failures, timeouts and invalid outputs in the denominator.
- Include a table of trial, per-case result, calls or tokens, and interpretation. Correctness that uses up the whole budget is still a failed user outcome.
- Report regressions and mixed results as prominently as improvements.
- Don't compare runs with mismatched fixtures as if they were controlled.
- Record everything in the journal (see `journal`) with labels for measured, tested and hypothesis.

## Stopping

If the work expands beyond the planned scope, checkpoint it. Write down what was completed, the caveats, the unresolved issues and a narrow resumption path, then ship a smaller verified piece rather than an unbounded candidate.
