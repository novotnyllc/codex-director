---
name: director-refactor
description: Runs the Codex Director refactor lane for behavior-preserving code or documentation cleanup. Use when a Director worker brief explicitly invokes $codex-director:director-refactor for simplifying structure, removing duplication, clarifying ownership boundaries, or reorganizing implementation without intended behavior change.
metadata:
  short-description: Run behavior-preserving refactor
---

# Director Refactor

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Refactor Workflow](../codex-director/references/refactor-workflow.md).
3. Report activation: `workflow-skill-loaded:$codex-director:director-refactor`, selected workflow/playbook `director-refactor`, top-level control loop, behavior-preservation contract, helper/subagent lane plan, and evidence contract.
4. Identify the smallest safe boundary and baseline verification.
5. Refactor, verify unchanged behavior, run a review/self-check, and return concise evidence.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, planned RP-style helper profiles, and helper cleanup. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, behavior-preservation boundary, exact files/modules, leave-alone areas, sibling lanes, model/thinking/fork rationale, expected output, evidence standard, and cleanup expectation.
- Use `explore` helpers for call-site/test-gap/structure mapping, `engineer` helpers for clear mechanical refactor slices after the plan is known, `pair` helpers only for architectural ambiguity, and `design` helpers for bounded user-facing copy/layout polish.
- Prefer sequential `engineer` steering for dependent refactor items. Parallel helpers require zero file overlap, explicit sibling boundaries, and independent behavior-preservation checks.
- V2 evidence counts only after this worker spot-checks behavior claims, verifies tests or characterization evidence, and records `close_agent` or `close_blocked:<reason>`.

## Workflow

1. Activate: restate refactor goal, behavior-preservation boundary, selected workflow, top-level loop, helper policy, and verification contract.
2. Baseline: identify current behavior, tests, public contracts, call sites, and dirty worktree state. Run focused baseline checks when useful.
3. Plan: choose the smallest refactor boundary, expected mechanical changes, risk areas, rollback path, and verification commands.
4. Helper lane: for non-trivial refactors, use a helper/subagent lane for call-site mapping, risk review, test-gap search, or verification.
5. Edit: move, rename, simplify, or deduplicate without changing behavior. Keep public APIs, data shape, side effects, and user-visible behavior stable unless explicitly authorized.
6. Verify: rerun baseline checks and targeted tests. Add characterization checks only when low-risk and appropriate.
7. Review: compare before/after behavior assumptions, coverage, unintended surface changes, and migration risk.
8. Finish: return behavior-preservation evidence, validation, review verdict, changed files, commit status when authorized, and cleanup/archive state.

## Escalate Or Stop

Ask the Director to reroute if behavior changes become necessary, ownership crosses modules/repos, public contracts shift, migrations appear, or verification cannot establish safety. Stop for secrets, production data, destructive actions, or unclear authority.

## Required Invariants

- Preserve behavior unless the Director explicitly changes the scope.
- Keep edits scoped to the assigned ownership boundary; avoid opportunistic cleanup outside it.
- Use helper/subagent lanes for non-trivial refactors, or record a blocked helper capability.
- If tests are missing, add low-risk characterization or document the verification gap.
- Stop for risky public contracts, migrations, production data, or unclear ownership.
- Do not treat `wait_agent`, `list_agents`, or helper final-status notifications as behavior-preservation evidence.
- Treat final output as candidate evidence until Director readback and reconciliation.

## Output

Report changed files, behavior-preservation evidence, verification commands, review verdict, native helper surface, V2 helper paths/evidence/owner verification/cleanup when used, residual risk, commit status when authorized, and cleanup/archive state.
