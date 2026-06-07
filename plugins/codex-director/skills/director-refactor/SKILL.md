---
name: director-refactor
description: Runs the Codex Director refactor lane for behavior-preserving code or documentation cleanup. Use when a Director worker brief explicitly invokes $director-refactor for simplifying structure, removing duplication, clarifying ownership boundaries, or reorganizing implementation without intended behavior change.
---

# Director Refactor

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Refactor Workflow](../codex-director/references/refactor-workflow.md).
3. Report activation: selected workflow/playbook `director-refactor`, top-level control loop, behavior-preservation contract, helper/subagent lane plan, and evidence contract.
4. Identify the smallest safe boundary and baseline verification.
5. Refactor, verify unchanged behavior, run a review/self-check, and return concise evidence.

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
- Treat final output as candidate evidence until Director readback and reconciliation.

## Output

Report changed files, behavior-preservation evidence, verification commands, review verdict, residual risk, commit status when authorized, and cleanup/archive state.
