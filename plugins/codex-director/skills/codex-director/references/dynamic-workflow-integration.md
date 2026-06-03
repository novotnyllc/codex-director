# Dynamic Workflow Integration

Use when a project director thread needs task-level orchestration for a complex task.

## Relationship

The director thread owns the project portfolio: routing, prioritization, Codex worker thread lifecycle, cross-task coordination, worktree/commit policy, reconciliation decisions, worker check-ins, and final user-facing status. Workers perform project work and repo-changing operations.

The `codex-dynamic-workflows` skill owns the orchestration protocol for one complex task: success criteria, approvals, packets, Codex worker-thread packet work, integration, verification, reusable recipes, and the run artifact:

```text
.workflow/<slug>/
|-- plan.md
|-- state.json
|-- orchestration.md
|-- packets/
|-- results/
`-- final-report.md
```

Call into `codex-dynamic-workflows` when the Director triage decides a task needs explicit task-level orchestration: packetization, Codex worker-thread staffing, integration, approval tracking, verification state, or reusable workflow artifacts.

For the full relationship between Director, dynamic workflow artifacts, self-contained workflow playbooks, Codex worker threads, and oracle/review lanes, see [Execution mode stack](execution-mode-stack.md).

Short version: dynamic workflow owns complex-task orchestration; workflow playbooks define the phases; optional tools may implement those phases; the Director remains the portfolio-level coordinator.

## When To Invoke

Check dynamic workflow mode before selecting build or orchestrate for every non-trivial task.

Invoke it when any hard trigger is true:

- The user explicitly asks for a dynamic workflow, swarm, packets, delegated workers, or Claude Code-style orchestration.
- The task needs explicit approval checkpoints, packet state, integration state, or a reusable recipe.
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

## Director Mapping

- Director active goal -> `.workflow/<slug>/plan.md`
- Director worker thread brief -> packet file under `packets/`
- Codex worker thread output -> result file under `results/`
- Director ledger snapshot -> `state.json`
- Director sequencing rules -> `orchestration.md`
- Director final status -> `final-report.md`

The Director creates real Codex worker threads for packets that benefit from isolation. The dynamic workflow packet plan defines what each worker owns. Packets too small for their own thread are combined with neighboring packets or handled by steering an existing worker; packet work is never executed in the Director thread.

Workers should use the matching self-contained workflow inside their packet:

- investigate/research workflow for research or diagnosis packets
- deep plan workflow for planning packets
- build workflow for implementation packets
- orchestration workflow for packet-internal decomposition
- review workflow for review packets
- refactor workflow for behavior-preserving cleanup packets
- optimize workflow for performance packets

Do not let a worker's local workflow overwrite the `.workflow/` task source of truth. It may produce subplans and exports, but packet status and integration decisions belong in the dynamic workflow artifact.

## Recursive Use

Dynamic workflow can recurse, but ownership must stay explicit:

- The parent Director owns the top-level `.workflow/<slug>/` task artifact.
- Each top-level packet is owned by one Codex worker thread.
- A worker may create nested workflow artifacts or native sub-agents only for packet-internal subwork.
- Nested helpers report to the owning worker; the owning worker writes the packet result under the parent `results/`.
- A nested workflow must not redefine parent success criteria, approvals, packet ownership, or integration policy.

## Setup

Dynamic workflow mode is selected by the trigger rules above. Use the installed `codex-dynamic-workflows` skill for the orchestration protocol, but never hard-code a user-local skill path. Resolve helper scripts relative to the installed skill directory. Create the artifact tree manually when no helper script is packaged.

Before creating packet briefs, record:

- Codex skills loaded for Director-level routing
- Codex skills each packet worker must consider
- model and thinking level per packet
- commit authority per packet
- native thread handle requirements
- stale/cancel policy
- evidence and artifact retention policy

Minimum artifact tree:

```text
.workflow/<slug>/
|-- plan.md
|-- state.json
|-- orchestration.md
|-- packets/
|-- results/
`-- final-report.md
```

`plan.md` must define success criteria, constraints, approval gates, verification, and packet list. `state.json` must track packet status, owner, branch/worktree, blockers, verification, and accepted/rejected decisions. `orchestration.md` must define sequencing and parallelism rules.

Keep the run directory in a project-appropriate local location. Do not put sensitive raw data, bulky transcripts, credentials, invite links, tokens, or raw private exports into workflow artifacts.

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
Verbosity limit:
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

If packets disagree, inspect authoritative sources before choosing.

If a collection helper is available from an installed dynamic-workflow skill, use it as a convenience only after confirming it reads the current artifact shape. Otherwise synthesize results manually from `results/` and worker evidence.

## Completion Audit

Before marking the task complete:

1. Verify workflow artifacts exist and are non-empty.
2. Confirm packet outputs are integrated.
3. Confirm approval-gated work had approval.
4. Confirm verification evidence satisfies success criteria.
5. Confirm any worker Codex Goals were audited against their verification surfaces.
6. Confirm commits/worktrees reconciled into the canonical repo/branch.
7. Confirm final report captures accepted/rejected results, conflicts, remaining risks, and next actions.

If a verification helper is available from an installed dynamic-workflow skill, use it as a convenience only. The Director still owns the completion decision and must audit the evidence directly.

## Reusable Recipes

If a run produces a useful repeatable pattern, save a concise recipe in a project-appropriate location. Include trigger, plan shape, packet list, verification checklist, and known risks. Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.
