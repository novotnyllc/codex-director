---
name: director-review
description: Runs the Codex Director review lane for adversarial plan, code, branch, PR, or worker-output review. Use when a Director worker brief explicitly invokes $codex-director:director-review for independent critique, acceptance gates, must-fix findings, or verification of worker evidence.
metadata:
  short-description: Run independent review gate
---

# Director Review

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

This split workflow skill is worker-side. If its activation marker, skill body, callback text, or readback evidence appears in a parent Director thread, the parent treats it only as routing input or child evidence. It does not load this workflow into the parent and does not permit parent inline browser, repo, provider, or project execution.

1. Read local instructions, the review scope, and the owning Director brief.
2. Load [Review Workflow](../codex-director/references/review-workflow.md).
3. Report activation: `workflow-skill-loaded:$codex-director:director-review`, selected workflow/playbook `director-review`, top-level control loop, review target, user-outcome fit, severity standard, and evidence contract.
4. Inspect only the approved files/artifacts/diffs/evidence.
5. Return findings first, ordered by severity, with file/line references when applicable.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, planned RP-style helper profiles, and helper cleanup. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, confirmed review scope, exact files/artifacts/diff to inspect, out-of-scope areas, severity standard, model/thinking/fork rationale, expected output, evidence standard, and cleanup expectation.
- Use `explore` helpers for targeted file/test/security evidence checks, `design` helpers for bounded UX/copy/design critique, and `pair` helpers only for complex cross-cutting review hypotheses.
- Do not let helpers decide the verdict for you. They produce candidate findings; this review worker verifies source evidence, deduplicates, assigns severity, and owns the final verdict.
- V2 helper output is review input only after this worker spot-checks findings against source evidence and records `close_agent` or `close_blocked:<reason>`.

## Workflow

1. Activate: restate review target, scope, selected workflow, top-level loop, severity standard, evidence sources, and out-of-scope areas.
2. Establish baseline: identify the diff, files, plan, worker evidence, tests, logs, or artifacts that are authoritative for the verdict.
3. Inspect risk areas: correctness, regressions, missing tests, security/privacy/data handling, auth/permissions, migrations, concurrency, error handling, observability, and user-facing behavior as relevant.
4. Verify claims: run allowed read-only checks or inspect outputs. Do not accept summaries without source evidence. Distinguish final user-outcome evidence from prerequisite checkpoints.
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
- Do not treat `wait_agent`, `list_agents`, or helper final-status notifications as review findings.
- Treat callback/final text as a wake signal for Director readback, not acceptance.
- Treat a redirect check, provider save, deploy health check, DB checkpoint, test pass, or worker diagnosis as checkpoint evidence unless it directly matches the user's final verification surface.
- When reviewing incident output, fail the acceptance path if diagnosis, provider mutation, code patch, direct deploy/alias work, browser proof, security review, and durable git/PR follow-up were collapsed without a recorded tiny/mechanical/low-risk exception.
- Stop for secrets, production data, destructive actions, or scope expansion.
- Keep output concise: findings, evidence, required fixes, residual risk, and test gaps.

## Output

Return `PASS`, `PASS_WITH_RISKS`, or `FAIL`, then findings by severity, evidence inspected, verification performed, native helper surface, V2 helper paths/evidence/owner verification/cleanup when used, unresolved questions, and cleanup/archive state.
