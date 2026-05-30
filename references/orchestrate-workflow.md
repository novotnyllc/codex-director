# Orchestrate Workflow

Use when work has multiple items, dependencies, parallel lanes, substantial ambiguity, or needs coordination across Codex worker threads and worker-internal delegates.

## Principle

The orchestrator owns the plan, ledger, sequencing, review gates, and reconciliation. Implementation and deep context gathering belong to bounded workers. Do not fire-and-forget a swarm; verify each completed item before dependent work continues.

If a `codex-dynamic-workflows` run exists for the task, treat its plan, state, packets, approval gates, integration policy, and results as the task source of truth. Use this orchestration workflow to execute and monitor packets, not to create a competing top-level plan.

## Phase 0: Workspace And Ledger

1. Verify project scope and local instruction files.
2. Check git status in each repo that may be touched.
3. Decide whether this task needs `codex-dynamic-workflows` task orchestration.
4. Decide main checkout vs worktree per workstream.
5. Create or update the active work ledger:
   - task
   - owner thread
   - repo/path
   - status
   - next action
   - blockers
   - done criteria
   - branch/worktree

If dynamic workflow mode is active, mirror this state into `.workflow/<slug>/state.json` and packet/result files.

## Phase 1: Contextualize

Translate the raw request into project nouns:

- owning repo/path
- modules and files likely involved
- affected workflows
- constraints and risk areas
- relevant instructions and skills

Use only 1-2 direct navigation calls before delegating deeper context. If still ambiguous, dispatch a narrow research/explore worker with one question.

## Phase 2: Research Before Planning

Run research lanes for unknowns:

- repo seams and ownership
- prior decisions or similar work
- external facts
- test/verification conventions
- data/auth/security risk areas

Synthesize findings into planning constraints.

## Phase 3: Decompose

Break the work into up to 5 items. Prefer 2-3.

Each item needs:

- Goal.
- Done when.
- Key files/modules.
- Dependencies.
- Size.
- Review gate.
- Evidence required.
- Git/worktree handling.

If the work is naturally one item, do not add orchestration ceremony. Dispatch a build/review/investigate workflow directly.

## Phase 4: Plan Review

Before implementation, run an adversarial plan review:

- Are items correctly bounded?
- Are dependencies accurate?
- Is parallelism safe?
- Are research gaps still open?
- Are tests/checks defined?
- Are branches/worktrees and commit boundaries clear?

Fix the plan before dispatch.

## Phase 5: Dispatch

Default: one fresh Codex worker thread per independent item.

Use one continuing worker when:

- items are tightly coupled
- many tiny sequential steps share context
- the same implementation decisions must carry forward

Every worker brief must include:

- project scope and repo/path
- exact item responsibility
- sibling work and areas to avoid
- done criteria
- research/plan context
- required skills/context workflow
- plan review and adversarial review gate
- evidence and verbosity limits
- git/worktree/commit expectations

For parallel workers, explicitly name siblings:

```text
Another worker thread is working on <area>. Avoid modifying <files/modules>. If you find a dependency or conflict, stop and report.
```

## Phase 6: Monitor

Poll or read workers regularly.

Check:

- activation report completed
- correct instructions and skills used
- no silent scope expansion
- plan followed
- verification running
- evidence concise and sufficient
- blockers surfaced early

Do not duplicate in-flight work. Prepare next briefs, review completed output, or reconcile branches while workers run.

## Phase 7: Verify Each Item

For each completed worker:

1. Read its summary and evidence.
2. Spot-check key files/artifacts when needed.
3. Confirm tests/checks.
4. Run or request adversarial review.
5. Mark item complete only when done criteria are met.
6. Commit or confirm logical commit.
7. Update the ledger.

If gaps exist, steer the same worker to fix them before starting dependent work.

## Phase 8: Reconcile

When items are complete:

- Merge/cherry-pick/PR worktree output into the canonical repo/branch according to project practice.
- Resolve conflicts deliberately.
- Run final verification.
- Run final adversarial review if multiple items interacted.
- Clean up completed worktrees and stale branches when safe.
- Archive completed worker threads after evidence is recorded.

## Final Rollup

Report:

- completed items
- branch/commit hashes
- tests/checks
- review verdicts
- reconciliation status
- blockers or deferred work
- suggested next action
