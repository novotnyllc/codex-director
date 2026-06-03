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
5. Choose the runtime adapter from [Runtime adapters](runtime-adapters.md): native Codex worker threads, Agent Mode, another delegation runner, or simulated packet passes.
6. Create or update the active work ledger:
   - task
   - owner thread
   - repo/path
   - status
   - next action
   - blockers
   - done criteria
   - branch/worktree

If dynamic workflow mode is active, mirror this state into `.workflow/<slug>/state.json` and packet/result files.

Adapter examples:

```text
Native thread tools: create worker thread -> send bounded brief -> read/poll -> steer -> archive.
Agent Mode: start detached session -> wait/poll session IDs -> steer or respond -> cleanup session.
Fallback: create packet note -> run simulated pass serially -> write result note -> integrate.
```

Do not proceed until the ledger records worker handles or explicitly says `simulated`.

## Phase 1: Contextualize

Translate the raw request into project nouns:

- owning repo/path
- modules and files likely involved
- affected workflows
- constraints and risk areas
- relevant instructions and skills

Use only 1-2 direct navigation calls before delegating deeper context. If still ambiguous, dispatch a narrow research/explore worker with one question.

Good contextualized task:

```text
Raw: "make this installable"
Contextualized: "Fix the plugin marketplace/install surface in README, marketplace.json, plugin.json, and validation commands for codex-director."
```

When a context engine is available, use it to produce or export the initial plan. Treat the export or plan file as a shared read-only document for workers and a living checklist for the Director.

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

For each item, decide fresh worker vs steering:

- Fresh worker: default for independent items, review lanes, research scouts, and anything that benefits from clean context.
- Steering one worker: tightly coupled sequential items, many tiny steps, or continuation of implementation decisions already made in that worker.
- Parallel workers: only when file/module ownership is disjoint or explicitly serialized by the Director.

Do not create five items because five is allowed. Over-decomposition increases coordination cost and conflict risk.

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

Dispatch brief template:

```text
Project scope:
Repo/path:
Plan or workflow artifact:
Your item:
Done when:
Leave alone:
Sibling work:
Required workflow:
Research/context required:
Goal policy:
Git/worktree authority:
Verification:
Review gate:
Evidence format:
Verbosity limit:
Stop and report if:
```

If using an adapter with wait/poll semantics, start parallel workers detached, then wait for the first completed/blocked worker and loop over remaining handles. Do not end a Director turn while worker handles are running or waiting for input.

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

If a worker asks for scope or authority:

1. Compare the question to the plan and ledger.
2. Answer only the worker's technical need; do not forward user meta-commentary.
3. Update the ledger if the answer changes scope, branch, worktree, or done criteria.
4. If the answer would change the user's requested outcome, pause for user input.

If a worker silently broadens scope, steer once with the original boundary. If it continues, cancel/archive that worker and re-dispatch a clean brief.

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

Update the plan, ledger, or `.workflow/<slug>/state.json` immediately after each accepted item. Marking a worker done in chat is not enough; the next worker needs an artifact or ledger state it can trust.

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

## Housekeeping

After evidence is captured:

- Archive or clean up completed worker threads/sessions according to the runtime adapter.
- Delete stale prompt/context exports that no worker or review still needs.
- Keep durable artifacts: plans, workflow state, final reports, commits, review reports.
- Cancel stale workers before final status.
- Remove temporary worktrees only after their branch/commit/PR is recoverable and no conflict resolution is in progress.

## Anti-Patterns

- Fire-and-forget worker swarms.
- Parallel workers touching overlapping files without sibling warnings.
- Treating a worker summary as verified evidence.
- Proceeding to dependent work before item done criteria are met.
- Letting dynamic workflow artifacts and Director ledger diverge.
- Hiding conflicts, skipped verification, or stale worktrees in the final rollup.
