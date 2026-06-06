# Orchestrate Workflow

Use when work has multiple items, dependencies, parallel lanes, substantial ambiguity, or needs coordination across Codex worker threads and worker-internal delegates.

## Principle

The orchestrator owns the plan, ledger, sequencing, review gates, and reconciliation. Implementation and deep context gathering belong to bounded workers. Do not fire-and-forget a swarm; verify each completed item before dependent work continues.

Most Director-created worker threads should themselves run this orchestration workflow as the top-level control loop for their bounded assignment. Inside that worker, build, review, investigate, refactor, optimize, Browser oracle, and context-engine passes are phase playbooks or helper lanes. A direct single-playbook worker is an exception for tiny, mechanical, low-risk, or genuinely single-lane work and must record why orchestration is unnecessary.

For Director-created workers, “completed” means terminal signal -> `pending-readback` -> `codex_app.read_thread` child-thread readback -> terminal report captured -> evidence/helper/direct-leaf reconciliation -> cleanup/archive state recorded -> explicit acceptance state. Callback payloads, expected finals, stale summaries, and worker claims are only wake signals.

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
   - callback policy and terminal signal
   - `read_cursor` or `last_turn_seen`
   - `readback_status`, `final_report_captured`, and `evidence_reconciled`
   - `helper_policy_accepted` and direct-leaf rationale if claimed
   - `acceptance_status`
   - cleanup/archive state
   - last poll/stale threshold

Escalate to `.workflow/<slug>/` once the task has multiple worker handles, spans turns or interruptions, uses callback/watchdog monitoring that must survive the current turn, has worktrees, approvals, integration order, durable review/oracle artifacts, stale/cancel/archive/blocked state, multiple deliverables, or packet dependencies. Use `plan.md`, `orchestration.md`, packet files, result files, and `final-report.md` for durable task artifacts while the Director ledger tracks worker state.

Codex lifecycle examples:

```text
`codex_app` thread tools: create worker thread when authorized -> send bounded brief -> poll with `read_thread` -> capture terminal child report -> reconcile evidence/helper policy -> steer with `send_message_to_thread` if gaps remain -> archive with `set_thread_archived` after evidence is recorded.
Worker callback signal: when explicitly authorized and exposed in the worker runtime, worker sends one Director-thread callback for final/blocker/needs-user/oracle-request/handoff; the callback only marks `terminal_signal` and `pending-readback` until the Director reads the child thread.
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

If the work is naturally one item but still non-trivial, keep one owning worker and have that worker run a lightweight orchestration loop: plan, use helper/context lanes, execute the phase playbook, verify, review, and report evidence. Dispatch a direct build/review/investigate workflow only when the task is tiny, mechanical, low-risk, or genuinely single-lane and the brief records that rationale.

For each item, decide fresh worker vs steering:

- Fresh worker: default for independent items, review lanes, research scouts, and anything that benefits from clean context.
- Steering one worker: tightly coupled sequential items, many tiny steps, or continuation of implementation decisions already made in that worker.
- Do not reuse an existing worker for a different material task. Stop/archive or mark the old worker stale/superseded first, then create a fresh worker when the assignment changes.
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
- top-level worker control loop, defaulting to orchestration for non-trivial work
- exact model or inherited profile
- thinking level plus rationale
- sibling work and areas to avoid
- done criteria
- research/plan context
- Codex skills loaded/required/skipped
- Director workflow/playbook
- context/oracle/review tools
- worker helper/context policy: mandatory real helper/subagent lanes for non-trivial work, blocked helper capability if unavailable, or direct-leaf only with separate tiny/mechanical/low-risk rationale
- oracle request policy: workers return Oracle Request Packets to the Director unless explicitly delegated oracle-runner authority
- Browser Pro suitability: no/local lane enough/yes if available/yes but sensitive approval needed/pro-only requested
- plan review and adversarial review gate
- evidence and verbosity limits
- git/worktree expectations
- commit authority derived from the user's request

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
Top-level worker control loop:
Research/context required:
Worker helper/context policy:
Helper/subagent lanes required:
Direct-leaf exception rationale: not-applicable | tiny:<why>; mechanical:<why>; low-risk:<why>
Goal policy:
Git/worktree:
Commit authority: derived from the user's request; ask only if genuinely unclear
Verification:
Review gate:
Oracle request policy:
Browser Pro suitability:
Evidence format:
Verbosity limit: visible update gate; final evidence or blocker/decision only; no poll/wait/rerun narration
Nested worker authority: none unless explicitly delegated by the Director
Stop and report if:
```

For `codex_app` worker threads, there is no blocking wait operation; poll with `codex_app.read_thread`, grant callback authority when safe and exposed, then stop the Director turn or schedule/update a watchdog heartbeat when workers are still active. Use low/medium thinking only for routine polling and steering sent to worker/helper threads, high for substantive implementation/review steering, and xhigh for risky or final worker decisions. Any continuation, callback, or heartbeat that targets the Director thread itself must stay `xhigh`. Do not send a final completion rollup while worker handles are running, waiting for input, stale without a recorded stale verdict, missing terminal evidence, `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, missing helper/direct-leaf acceptance, or missing cleanup/archive state. Keep active status and next check-in plans in the ledger unless a visible blocker, decision, ownership handoff, stale/cancel/archive state, or final evidence packet is ready.

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

If a worker silently broadens scope, steer once with the original boundary. If it continues, request stop through the exposed thread contract, record `cancel_requested` or `stale`, archive only after capturing the last readable state, and re-dispatch a clean brief when authorized. If archive tooling is unavailable, record `archive_blocked:<reason>` and do not claim cleanup.

## Phase 7: Verify Each Item

For each terminal-signaled worker:

1. Mark the item `pending-readback`; treat callbacks, expected finals, stale summaries, and worker claims only as wake signals.
2. Read the child thread with `codex_app.read_thread` using `read_cursor` or `last_turn_seen` when available.
3. Capture the terminal child report from the thread itself, update `readback_status`, and record `final_report_captured`.
4. Compare claimed evidence to the done criteria.
5. Reconcile review/oracle status, helper/subagent lanes, or direct-leaf tiny/mechanical/low-risk rationale.
6. Dispatch a verification or review worker when file/artifact inspection is needed.
7. Confirm tests/checks from worker evidence.
8. Run or request adversarial review.
9. Confirm authorized commit/PR evidence or dispatch an integration worker.
10. Record cleanup/archive state: `archive_ready`, `archived`, `archive_blocked:<reason>`, `cleanup_worker_needed`, or `cleanup_done`.
11. Mark item accepted only when done criteria, evidence reconciliation, review/oracle status, helper/direct-leaf policy, and cleanup/archive state are present; otherwise mark `insufficient-evidence`, `blocked`, or `stale`.
12. Update the ledger and workflow artifact.

If gaps exist, steer the same worker to fix them before starting dependent work. Do not start dependent work from an item that is `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, missing helper/direct-leaf acceptance, or missing cleanup/archive state.

Update the plan, ledger, packet file, or result artifact immediately after each accepted item. Marking a worker done in chat is not enough; the next worker needs an artifact or ledger checkpoint it can trust.

## Phase 8: Reconcile

When items are accepted:

- Confirm every required result came from a child-thread terminal report that was read back and reconciled, not only from callback payloads or artifact presence.
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

Do not return partial deployment, readiness, or implementation verdicts before terminal worker evidence is captured through child-thread readback. Block final rollup while any worker is `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, missing helper/direct-leaf acceptance, or missing cleanup/archive state. If evidence is missing, say `pending-readback`, `readback_blocked:<reason>`, `stale`, or `insufficient-evidence` and name the missing evidence.

## Housekeeping

After evidence is captured:

- Archive or clean up completed worker threads/sessions according to the latest-Codex thread tooling contract.
- Delete stale scratch/context artifacts that no worker or review still needs.
- Keep durable artifacts: plans, orchestration notes, packet/result records, final reports, commits, review reports.
- Cancel stale workers before final status.
- Record `archive_ready`, `archived`, or `archive_blocked:<reason>` separately from evidence acceptance for every Director-owned worker.
- Remove temporary worktrees only through an authorized cleanup worker after their branch/commit/PR is recoverable and no conflict resolution is in progress.

## Anti-Patterns

- Fire-and-forget worker swarms.
- Parallel workers touching overlapping files without sibling warnings.
- Treating a worker summary as verified evidence.
- Proceeding to dependent work before item done criteria are met.
- Letting dynamic workflow artifacts and Director ledger diverge.
- Hiding conflicts, skipped verification, or stale worktrees in the final rollup.
- Reusing a worker thread for a different material task.
- Performing inline repo edits, pushes, deploys, or corrective execution in the Director thread because a worker stalled.
- Letting a delegated worker create nested top-level Codex workers without explicit Director authority.
- Claiming cleanup when archive is unavailable instead of recording `archive_blocked:<reason>`.
- Marking an item complete from callback payload, expected final, stale summary, or artifact presence without child-thread readback.
- Rolling up final status while any worker lacks evidence reconciliation, helper/direct-leaf acceptance, or cleanup/archive state.
