---
name: director-build
description: Runs the Codex Director build lane for bounded implementation packets. Use when a Director worker brief explicitly invokes $director-build for code, docs, configuration, tests, commits, or other implementation work that one worker can plan, edit, verify, and report.
---

# Director Build

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Build Workflow](../codex-director/references/build-workflow.md).
3. Report activation: `workflow-skill-loaded:$director-build`, selected workflow/playbook `director-build`, top-level control loop, scope, model/thinking rationale, helper/subagent lane plan, and evidence contract.
4. Gather only the context needed for the bounded change.
5. Plan, edit, verify, run the required review/self-check, and return concise evidence.

## Workflow

1. Activate: restate the assigned outcome, repo/path, files likely involved, constraints, selected workflow, top-level loop, commit authority, helper policy, and done criteria.
2. Baseline: read local instructions, check git status, identify existing patterns, and run or inspect the narrowest relevant baseline when useful.
3. Plan: outline the implementation steps, verification commands, review gate, rollback/recovery notes when relevant, and any files to avoid.
4. Helper lane: for non-trivial work, use a real helper/subagent lane for context mapping, implementation sketch, risky-area review, or verification. If unavailable, record `blocked:<reason>` before proceeding.
5. Implement: make the smallest scoped edits that satisfy the done criteria. Preserve unrelated dirty changes and local style.
6. Verify: run focused tests/checks and any required smoke or static validation. If validation cannot run, capture the exact blocker and residual risk.
7. Review: perform an adversarial self-check or delegated review against correctness, scope, tests, security/data risk, and user-facing behavior.
8. Finish: record changed files, validation evidence, review verdict, commit status when authorized, unresolved risks, and cleanup/archive state.

## Escalate Or Stop

Ask the Director to reroute to `$director-orchestrate` or `$director-dynamic-workflow` if implementation splits into independent lanes, crosses repos, needs approval gates, touches production/external writes, or requires long-lived monitoring. Stop for secrets, destructive operations, unclear commit authority, or ownership ambiguity.

## Required Invariants

- Stay inside the assigned repo/path, done criteria, commit authority, and constraints.
- Use orchestration as the top-level control loop for non-trivial build work unless the brief records a direct-leaf exception.
- Non-trivial work needs a real helper/subagent lane or a clear blocked helper capability. Direct leaf is allowed only with separate tiny, mechanical, and low-risk rationale.
- If the task grows into multiple independent lanes, risky writes, cross-repo work, or packetization, stop and ask the Director to reroute to `$director-orchestrate` or `$director-dynamic-workflow`.
- Do not create nested top-level Codex workers unless the Director explicitly delegates that authority.
- Treat final output as candidate evidence until the Director reads the worker thread and reconciles it.

## Output

Report changed files, commands/tests, review verdict, commit status when authorized, unresolved risks, cleanup/archive state, and exact blockers.
