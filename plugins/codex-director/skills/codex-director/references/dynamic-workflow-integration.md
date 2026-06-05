# Dynamic Workflow Integration

Use when a project director thread needs task-level orchestration for a complex task.

## Relationship

The director thread owns the project portfolio: routing, prioritization, Codex worker thread lifecycle, cross-task coordination, worktree/commit policy, reconciliation decisions, worker check-ins, child-thread readback, helper/direct-leaf acceptance, cleanup/archive state, and final user-facing status. Workers perform project work and repo-changing operations.

The `codex-dynamic-workflows` skill owns the orchestration protocol for one complex task: success criteria, approvals, packets, Codex worker-thread packet work, integration, verification, reusable recipes, and the run artifact. In this reference, `packet` means a concrete work-item file under `.workflow/<slug>/packets/`:

```text
.workflow/<slug>/
|-- plan.md
|-- orchestration.md
|-- packets/
|-- results/
`-- final-report.md
```

Call into `codex-dynamic-workflows` when the Director triage decides a task needs explicit task-level orchestration: packetization, Codex worker-thread staffing, integration, approval tracking, verification tracking, or reusable workflow artifacts.

For the full relationship between Director, dynamic workflow artifacts, self-contained workflow playbooks, Codex worker threads, and oracle/review lanes, see [Execution mode stack](execution-mode-stack.md).

Short version: dynamic workflow owns complex-task orchestration; workflow playbooks define the phases; optional tools may implement those phases; the Director remains the portfolio-level coordinator.

## When To Invoke

Check dynamic workflow mode before selecting build or orchestrate for every non-trivial task.

Invoke it when any hard trigger is true:

- The user explicitly asks for a dynamic workflow, swarm, packets, delegated workers, or Claude Code-style orchestration.
- The task needs explicit approval checkpoints, packet tracking, integration tracking, or a reusable recipe.
- The task spans multiple repos, worktrees, service boundaries, or independently mergeable workstreams.
- Risk and breadth are both present, such as migrations plus code changes, production data plus implementation, or external writes plus verification.

Also invoke it when at least two soft signals are true:

- The task has independent research, implementation, review, migration, QA, docs, or design tracks.
- A success contract would reduce drift.
- Risk is present: destructive edits, external writes, deploys, secrets, production data, billing, user accounts, migrations, or broad repo-wide changes.
- Verification benefits from a separate pass from implementation.
- The workflow could become a reusable recipe.
- Delegation would materially improve speed, coverage, review independence, risk control, context management, or token economy even if the user did not ask for it by name.

Do not invoke it for small single-thread tasks. Start one Codex worker thread with the build, review, or investigate workflow instead.

## Deterministic Durable State Escalation

Escalate from in-thread Director ledger state to `.workflow/<slug>/` artifacts when any of these are true:

- More than one worker handle exists.
- The task spans turns, interruptions, or resumptions.
- Callback/watchdog monitoring must survive beyond the current Director turn.
- Stale, cancel, archive, or blocked state matters.
- Review/oracle outputs must be preserved.
- Worktrees, approvals, packet dependencies, integration order, or multiple deliverables exist.
- Production/external writes, schema/data/migrations, deploy/rollback/remediation, multi-repo work, or high-risk multi-lane work is in scope.

A single short worker can remain in the visible Director transcript only if the transcript explicitly records the worker handle, `read_cursor` or `last_turn_seen`, terminal signal, readback status, captured final report, evidence reconciliation, helper/direct-leaf acceptance, acceptance status, and cleanup/archive state. Any worker expected to finish after the Director stops must have recoverable transcript state or `.workflow/<slug>/` artifacts.

## Director Mapping

- Director active goal -> `.workflow/<slug>/plan.md`
- Director worker thread brief -> packet file under `packets/`
- Codex worker thread output -> candidate evidence until Director readback/reconciliation; accepted output -> result file under `results/`
- Director ledger checkpoint -> Director ledger, with packet/result evidence reflected in workflow artifacts
- Director sequencing rules -> `orchestration.md`
- Director final status -> `final-report.md`

The Director creates real Codex worker threads for packets that benefit from isolation. The dynamic workflow packet plan defines what each worker owns. Packets too small for their own thread are combined with neighboring packets or handled by steering an existing worker; packet work is never executed in the Director thread.

A packet result is not durable accepted output merely because a worker callback arrived or an artifact exists. Worker outputs become `results/` only after the Director reads the child thread with `codex_app.read_thread`, captures the terminal child report, reconciles done criteria, review/oracle status, helper/direct-leaf acceptance, and records cleanup/archive state. Before that, store them as candidate evidence in the ledger, orchestration notes, or scratch/candidate artifacts.

Workers should use the matching self-contained workflow and thinking policy inside their packet:

- investigate/research workflow for research or diagnosis packets; use low/medium for narrow scouts and high for synthesis that affects the plan
- deep plan workflow for planning packets; use high by default and xhigh for high-risk architecture/security/data plans
- build workflow for implementation packets; use latest-main/high by default, `gpt-5.3-codex-spark` only for mechanical or very contained low-risk code, and latest-main/xhigh for risky architecture/security/data/production/cross-repo changes
- orchestration workflow for packet-internal decomposition; use latest-main/high for decomposition/integration and medium/`gpt-5.3-codex-spark` for packet drafting/status
- review workflow for review packets; use latest-main/high by default and latest-main/xhigh for risky final verdicts or conflicting evidence
- refactor workflow for behavior-preserving cleanup packets; use latest-main/high by default, `gpt-5.3-codex-spark` only for narrow mechanical refactors, latest-main/xhigh for public contract or ownership-boundary changes
- optimize workflow for performance packets; use medium/`gpt-5.3-codex-spark` for measurement, latest-main/high for optimization code, and latest-main/xhigh for concurrency/data/production-risk changes

Do not let a worker's local workflow overwrite the top-level `.workflow/` task artifacts. It may produce subplans and local scratch artifacts, but packet status and integration records belong to the parent workflow. A local worker report can update packet status only through the Director readback and reconciliation sequence.

## Recursive Use

Dynamic workflow can recurse, but ownership must stay explicit:

- The parent Director owns the top-level `.workflow/<slug>/` task artifact.
- Each top-level packet is owned by one Codex worker thread.
- A worker may create nested workflow artifacts or native sub-agents only for packet-internal subwork.
- Nested helpers report to the owning worker; the owning worker returns candidate packet evidence, and the Director promotes accepted output under the parent `results/` only after readback and reconciliation.
- A nested workflow must not redefine parent success criteria, approvals, packet ownership, or integration policy.

## Setup

Dynamic workflow mode is selected by the trigger rules above. Use the installed `codex-dynamic-workflows` skill for the orchestration protocol, but never hard-code a user-local skill path. Resolve helper scripts relative to the installed skill directory. Create the artifact tree manually when no helper script is packaged.

Before creating packet briefs, record:

- Codex skills loaded for Director-level routing
- Codex skills each packet worker must consider
- model and thinking level plus rationale per packet
- commit authority per packet
- `codex_app` thread handle requirements
- stale/cancel policy
- worker callback signal policy
- readback fields: `read_cursor` or `last_turn_seen`, terminal signal, `readback_status`, terminal report path, `final_report_captured`, and `evidence_reconciled`
- helper/direct-leaf policy and acceptance fields per packet worker
- cleanup/archive state per packet worker
- heartbeat/wake cadence for active packet workers
- evidence and artifact retention policy

Minimum artifact tree:

```text
.workflow/<slug>/
|-- plan.md
|-- orchestration.md
|-- packets/
|-- results/
`-- final-report.md
```

`plan.md` must define success criteria, constraints, approval gates, verification, and packet list. The Director ledger must track packet status, owner, branch/worktree, blockers, verification, accepted/rejected decisions, callback policy, terminal signal, readback status, captured final report path, helper/direct-leaf acceptance, cleanup/archive state, next wake time, monitor interval, and heartbeat/automation id when used. `orchestration.md` must define sequencing, parallelism, and signal-first resumable monitoring rules.

Keep the run directory in a project-appropriate local location. Do not put sensitive raw data, bulky transcripts, credentials, invite links, tokens, or raw private data in workflow artifacts. Store large/sensitive evidence outside the repo or in ignored local scratch artifacts, then reference only redacted summaries.

## Packet Shape

Each packet should include:

```text
Packet ID:
Objective:
Context:
Files / sources:
Ownership:
Do:
Do not:
Expected output:
Verification:
Evidence required:
Helper/subagent lanes required:
Direct-leaf exception rationale: not-applicable | tiny:<why>; mechanical:<why>; low-risk:<why>
Readback/acceptance fields: terminal signal, readback status, final report captured, evidence reconciled, helper policy accepted, acceptance status, cleanup/archive state
Verbosity limit: visible update gate; final evidence or blocker/decision only; no poll/wait/rerun narration
Git/worktree:
```

Packets should be disjoint where possible. For code-edit packets, avoid overlapping files/modules unless the Director deliberately serializes them.

## Integration

After packets finish, synthesize:

```text
Accepted:
Rejected:
Conflicts:
Decisions:
Final changes:
Remaining risks:
Verification still needed:
```

If packets disagree, inspect authoritative sources before choosing. Do not integrate or choose from packet outputs that are still `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, missing helper/direct-leaf acceptance, or missing cleanup/archive state.

If a collection helper is available from an installed dynamic-workflow skill, use it as a convenience only after confirming it reads the current artifact shape. Otherwise synthesize results manually from `results/` and worker evidence.

## Completion Audit

Before marking the task complete:

1. Verify workflow artifacts exist and are non-empty.
2. Confirm every packet worker has terminal signal state and child-thread readback recorded: `readback_complete` with a captured terminal report, or a blocking state such as `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, `blocked`, or `stale`.
3. Confirm accepted packet outputs were promoted to `results/` only after Director readback and evidence reconciliation.
4. Confirm helper/subagent lanes were accepted for non-trivial workers, or direct-leaf tiny/mechanical/low-risk rationale was accepted.
5. Confirm review/oracle status is recorded and must-fix findings are resolved or explicitly accepted.
6. Confirm cleanup/archive state is recorded for every packet, review, oracle, verification, stale, superseded, and cleanup worker.
7. Confirm packet outputs are integrated.
8. Confirm approval-gated work had approval.
9. Confirm verification evidence satisfies success criteria.
10. Confirm any worker Codex Goals were audited against their verification surfaces.
11. Confirm commits/worktrees reconciled into the canonical repo/branch.
12. Confirm final report captures accepted/rejected results, conflicts, remaining risks, cleanup/archive state, and next actions.

If any required worker remains `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, missing helper/direct-leaf acceptance, or missing cleanup/archive state, the dynamic workflow is not complete.

If a verification helper is available from an installed dynamic-workflow skill, use it as a convenience only. The Director still owns the completion decision and must audit the evidence directly.

## Reusable Recipes

If a run produces a useful repeatable pattern, save a concise recipe in a project-appropriate location. Include trigger, plan shape, packet list, verification checklist, and known risks. Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.
