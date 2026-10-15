---
name: incident
description: Investigate a reported failure or production incident with an evidence-first method — establish sources of truth, find the failing stage, separate facts from hypotheses, reproduce with a sanitized regression and close the loop. Use when something "didn't work", a user reports wrong behavior, a release misbehaves, or logs show errors.
---

# Incident investigation

The goal is a diagnosis that the evidence supports, a focused regression, and a fix that ships. A plausible story is not the goal. The repository bindings name its log and diagnostics commands and its troubleshooting runbook. Read that runbook first if it exists.

## Sources of truth, in order

1. **Integrated code:** the default branch on GitHub. A branch, PR, candidate or package version is not what is deployed.
2. **What is running:** the exact commit's successful release receipt or run, plus current diagnostics showing it is still the running SHA. Startup health doesn't prove an integration works.
3. **What happened:** the system's own records (runs, events, tool calls, approvals, stored messages and logs). A model's reply or a screenshot alone doesn't prove that an action or external write succeeded.
4. **Docs:** the work index and journal. Historical reports stay historical. If the evidence conflicts with the docs, record the discrepancy and update the docs after verifying.

## First pass

1. Record the report: approximate time with timezone, the requested action, the observed result, and what the user saw or clicked. Keep private details in the authorized task, never in an issue or PR.
2. Run preflight: fetch main, identify the deployed SHA and its evidence, and check which diagnostic capabilities this session actually has.
3. Read the sanitized logs or diagnostics through the bound command, starting with errors in the incident window. A missing log line is not proof of success.
4. Match timestamps and run or request IDs before attributing a failure to the reported request.
5. If a read is denied or unavailable, say which read and what therefore remains unknown. Never turn an unverified explanation into a diagnosis.

## Follow the failing stage

Walk the path: input → routing → validation and authorization → model or tool decision → external call → persistence → delivery. Find the first stage whose recorded output differs from what was expected. Then classify the failure: the provider contract, our validation, an assumption that was never true, a state race, or the model's choice given the context it saw.

For an external integration, verify the provider's official contract before blaming either side. A denied or failed read does not by itself establish the cause.

## Close the loop

- Reproduce the failure as a focused, sanitized regression that fails before the fix and passes after it.
- Implement the smallest root-cause fix. Recovery logic that repeats a side effect is a decision about side effects, so treat it as one.
- Run the independent review, ship, and record a journal entry with the observation, diagnosis, change, tests, review, exact release evidence and live acceptance limits. Update the work index and the domain runbook.
- If access or consent is missing, document the concrete blocker and the next safe check. Do not mark it fixed.

Never put API keys, tokens, raw private content or full production traces in Git, PRs, CI output or an agent prompt. Use structural metadata and anonymized fixtures.
