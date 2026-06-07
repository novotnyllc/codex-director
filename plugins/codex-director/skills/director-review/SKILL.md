---
name: director-review
description: Runs the Codex Director review lane for adversarial plan, code, branch, PR, or worker-output review. Use when a Director worker brief explicitly invokes $director-review for independent critique, acceptance gates, must-fix findings, or verification of worker evidence.
---

# Director Review

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions, the review scope, and the owning Director brief.
2. Load [Review Workflow](../codex-director/references/review-workflow.md).
3. Report activation: `workflow-skill-loaded:$director-review`, selected workflow/playbook `director-review`, top-level control loop, review target, severity standard, and evidence contract.
4. Inspect only the approved files/artifacts/diffs/evidence.
5. Return findings first, ordered by severity, with file/line references when applicable.

## Workflow

1. Activate: restate review target, scope, selected workflow, top-level loop, severity standard, evidence sources, and out-of-scope areas.
2. Establish baseline: identify the diff, files, plan, worker evidence, tests, logs, or artifacts that are authoritative for the verdict.
3. Inspect risk areas: correctness, regressions, missing tests, security/privacy/data handling, auth/permissions, migrations, concurrency, error handling, observability, and user-facing behavior as relevant.
4. Verify claims: run allowed read-only checks or inspect outputs. Do not accept summaries without source evidence.
5. Use review helpers: for broad or risky reviews, use a helper/subagent lane for targeted file review, test-gap analysis, security pass, or evidence cross-check.
6. Decide findings: include only actionable issues. Each finding needs severity, file/line when possible, impact, and what would fix or prove it.
7. Verdict: return `FAIL` for must-fix issues, `PASS_WITH_RISKS` for accepted gaps/residual risk, or `PASS` when no actionable issues remain.
8. Finish: list evidence inspected, checks run or blocked, open questions, and cleanup/archive state.

## Finding Format

Lead with findings. Use concise severity labels such as `[P1]`, `[P2]`, or `[P3]`. Include a file/line reference for code findings when available. Put summary and residual risk after findings.

## Required Invariants

- Review independently; do not patch unless the Director explicitly grants fix authority.
- Verify claims against source, diff, tests, logs, or artifacts rather than worker summary text alone.
- Use helper/subagent review lanes for non-trivial or broad review, or record a blocked helper capability.
- Treat callback/final text as a wake signal for Director readback, not acceptance.
- Stop for secrets, production data, destructive actions, or scope expansion.
- Keep output concise: findings, evidence, required fixes, residual risk, and test gaps.

## Output

Return `PASS`, `PASS_WITH_RISKS`, or `FAIL`, then findings by severity, evidence inspected, verification performed, unresolved questions, and cleanup/archive state.
