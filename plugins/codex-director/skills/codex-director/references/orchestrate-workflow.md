# Orchestrate Workflow

Use when work has multiple items, dependencies, parallel lanes, substantial ambiguity, or needs coordination across Codex worker threads and worker-internal delegates.

## Principle

The orchestrator owns the plan, ledger, sequencing, review gates, and reconciliation. Implementation and deep context gathering belong to bounded workers. Do not fire-and-forget a swarm; verify each completed item before dependent work continues.

If a `codex-dynamic-workflows` run exists for the task, treat its plan, packets, approval gates, integration policy, and results as the task source of truth. Use this orchestration workflow to execute and monitor packets, not to create a competing top-level plan.

## Phase 0: Workspace And Ledger

1. Verify project scope and local instruction files.
2. Check git status in each repo that may be touched.
3. Decide whether this task needs `codex-dynamic-workflows` task orchestration.
4. Decide main checkout vs worktree per workstream.
5. Use [Latest Codex runtime tooling](runtime-adapters.md): `codex_app` worker threads with resolved project targets own worker lifecycle; worker-internal sub-agents and context engines are helper layers only.
6. Discover/load applicable Codex skills for orchestration and record which skills each worker must consider.
7. Create or update the active work ledger:
   - task id
   - task
   - shape
   - Codex thread/project tooling
   - worker thread id/title
   - owner thread
   - repo/path
   - status
   - next action
   - blockers
   - done criteria
   - branch/worktree
   - model/thinking
   - required skills/workflows
   - commit authority
   - evidence required
   - last poll/stale threshold

Escalate to `.workflow/<slug>/` once the task has multiple worker handles, worktrees, approvals, integration order, durable review/oracle artifacts, or stale/cancel state that must survive turns. Use `plan.md`, `orchestration.md`, packet files, result files, and `final-report.md` for durable task artifacts while the Director ledger tracks worker state.

Codex lifecycle examples:

```text
`codex_app` thread tools: create worker thread when authorized -> send bounded brief -> poll with `read_thread` -> steer with `send_message_to_thread` -> archive with `set_thread_archived`.
Worker callback signal: when explicitly authorized and exposed in the worker runtime, worker sends one Director-thread callback for final/blocker/needs-user/oracle-request/handoff.
Heartbeat monitor: after dispatch, schedule or update a watchdog Director thread heartbeat instead of keeping the Director turn open solely to poll.
Worker-internal sub-agents: spawn bounded helper -> wait/poll according to that helper's concrete tool contract -> roll up evidence into owning worker.
```

Do not proceed until the ledger records worker handles for all project work.

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

When a context engine is available, use it to produce the initial plan. Save a shared read-only artifact only when workers or reviewers need a stable path.

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

Default: one fresh Codex worker thread per independent item when the active `codex_app` contract authorizes worker creation for the Director scope.

Use one continuing worker when:

- items are tightly coupled
- many tiny sequential steps share context
- the same implementation decisions must carry forward

Every worker brief must include:

- project scope and repo/path
- exact item responsibility
- starting prompt and required skills/workflow references
- exact model or inherited profile
- thinking level plus rationale
- sibling work and areas to avoid
- done criteria
- research/plan context
- Codex skills loaded/required/skipped
- Director workflow/playbook
- context/oracle/review tools
- worker helper/context policy: sub-agents, context scouts, model/function selection helpers, or none plus why
- oracle request policy: workers return Oracle Request Packets to the Director unless explicitly delegated oracle-runner authority
- Browser Pro suitability: no/local lane enough/yes if available/yes but sensitive approval needed/pro-only requested
- plan review and adversarial review gate
- evidence and verbosity limits
- git/worktree expectations
- commit authority

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
Model: latest main id, inherited latest-main default, or `gpt-5.3-codex-spark` for a Spark-fit lane only
Thinking plus rationale:
Codex skills to consider:
Required skills/workflows:
Required workflow:
Research/context required:
Worker helper/context policy:
Goal policy:
Git/worktree:
Commit authority:
Verification:
Review gate:
Oracle request policy:
Browser Pro suitability:
Evidence format:
Verbosity limit: visible update gate; final evidence or blocker/decision only; no poll/wait/rerun narration
Stop and report if:
```

For `codex_app` worker threads, there is no blocking wait operation; poll with `codex_app.read_thread`, grant callback authority when safe and exposed, then stop the Director turn or schedule/update a watchdog heartbeat when workers are still active. Use low/medium thinking only for routine polling and steering sent to worker/helper threads, high for substantive implementation/review steering, and xhigh for risky or final worker decisions. Any continuation, callback, or heartbeat that targets the Director thread itself must stay `xhigh`. Do not send a final completion rollup while worker handles are running or waiting for input. Keep active status and next check-in plans in the ledger unless a visible blocker, decision, ownership handoff, stale/cancel/archive state, or final evidence packet is ready.

## Phase 6: Monitor

Poll or read workers regularly, but quietly. Do not hold the Director turn open for long waits. Use one short polling burst only when completion is likely within about a minute; otherwise use the resumable monitoring cadence from [Latest Codex runtime tooling](runtime-adapters.md).

Check:

- activation report completed
- correct instructions and skills used
- no silent scope expansion
- plan followed
- verification running
- evidence concise and sufficient
- blockers surfaced early

Do not duplicate in-flight work. Prepare next briefs, update ledger state, and dispatch review, verification, integration, or cleanup workers as needed.

If a worker asks for scope or authority:

1. Compare the question to the plan and ledger.
2. Answer only the worker's technical need; do not forward user meta-commentary.
3. Update the ledger if the answer changes scope, branch, worktree, or done criteria.
4. If the answer would change the user's requested outcome, pause for user input.

If a worker silently broadens scope, steer once with the original boundary. If it continues, request stop through the exposed thread contract, record `cancel_requested` or `stale`, archive only after capturing the last readable state, and re-dispatch a clean brief when authorized.

## Phase 7: Verify Each Item

For each completed worker:

1. Read its summary and evidence.
2. Compare claimed evidence to the done criteria.
3. Dispatch a verification or review worker when file/artifact inspection is needed.
4. Confirm tests/checks from worker evidence.
5. Run or request adversarial review.
6. Mark item complete only when done criteria are met.
7. Confirm authorized commit/PR evidence or dispatch an integration worker.
8. Update the ledger.

If gaps exist, steer the same worker to fix them before starting dependent work.

Update the plan, ledger, packet file, or result artifact immediately after each accepted item. Marking a worker done in chat is not enough; the next worker needs an artifact or ledger checkpoint it can trust.

## Phase 8: Reconcile

When items are complete:

- Dispatch or steer an integration worker to merge/cherry-pick/PR worktree output into the canonical repo/branch according to project practice.
- Ensure conflicts are resolved deliberately by the owning integration worker.
- Dispatch final verification.
- Run final adversarial review if multiple items interacted.
- Dispatch cleanup for completed worktrees and stale branches when safe.
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

- Archive or clean up completed worker threads/sessions according to the latest-Codex thread tooling contract.
- Delete stale scratch/context artifacts that no worker or review still needs.
- Keep durable artifacts: plans, orchestration notes, packet/result records, final reports, commits, review reports.
- Cancel stale workers before final status.
- Remove temporary worktrees only through an authorized cleanup worker after their branch/commit/PR is recoverable and no conflict resolution is in progress.

## Anti-Patterns

- Fire-and-forget worker swarms.
- Parallel workers touching overlapping files without sibling warnings.
- Treating a worker summary as verified evidence.
- Proceeding to dependent work before item done criteria are met.
- Letting dynamic workflow artifacts and Director ledger diverge.
- Hiding conflicts, skipped verification, or stale worktrees in the final rollup.
