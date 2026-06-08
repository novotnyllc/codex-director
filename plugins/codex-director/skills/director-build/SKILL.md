---
name: director-build
description: Runs the Codex Director build lane for bounded implementation packets. Use when a Director worker brief explicitly invokes $codex-director:director-build for code, docs, configuration, tests, commits, or other implementation work that one worker can plan, edit, verify, and report.
metadata:
  short-description: Run bounded implementation lane
---

# Director Build

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Build Workflow](../codex-director/references/build-workflow.md).
3. Report activation: `workflow-skill-loaded:$codex-director:director-build`, selected workflow/playbook `director-build`, top-level control loop, scope, model/thinking rationale, helper/subagent lane plan, and evidence contract.
4. Gather only the context needed for the bounded change.
5. Plan, edit, verify, run the required review/self-check, and return concise evidence.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, planned RP-style helper profiles, and helper cleanup. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, goal, exact scope, leave-alone files/modules, sibling lanes, plan/artifact paths, model/thinking/fork rationale, expected output, evidence standard, and cleanup expectation.
- Use `explore` helpers for context/test mapping, `engineer` helpers for clear bounded sub-edits after the plan is known, `pair` helpers for complex implementation reasoning, and `design` helpers only for bounded UX/copy/design critique.
- For parallel helpers, require disjoint files/modules and sibling-awareness. For sequential helpers, use `followup_task` only inside the same bounded implementation decision path.
- V2 evidence counts only after this worker reads the helper output, spot-checks material claims, summarizes verified evidence into final build evidence, and records `close_agent` or `close_blocked:<reason>`.

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

Ask the Director to reroute to `$codex-director:director-orchestrate` or `$codex-director:director-dynamic-workflow` if implementation splits into independent lanes, crosses repos, needs approval gates, touches production/external writes, or requires long-lived monitoring. Stop for secrets, destructive operations, unclear commit authority, or ownership ambiguity.

## Required Invariants

- Stay inside the assigned repo/path, done criteria, commit authority, and constraints.
- Use orchestration as the top-level control loop for non-trivial build work unless the brief records a direct-leaf exception.
- Non-trivial work needs a real helper/subagent lane or a clear blocked helper capability. Direct leaf is allowed only with separate tiny, mechanical, and low-risk rationale.
- If the task grows into multiple independent lanes, risky writes, cross-repo work, or packetization, stop and ask the Director to reroute to `$codex-director:director-orchestrate` or `$codex-director:director-dynamic-workflow`.
- Do not create nested top-level Codex workers unless the Director explicitly delegates that authority.
- Do not treat `wait_agent`, `list_agents`, or helper final-status notifications as implementation evidence.
- Treat final output as candidate evidence until the Director reads the worker thread and reconciles it.

## Output

Report changed files, commands/tests, review verdict, commit status when authorized, native helper surface, V2 helper paths/evidence/owner verification/cleanup when used, unresolved risks, cleanup/archive state, and exact blockers.
