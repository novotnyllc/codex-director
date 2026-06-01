# Dynamic Workflow Integration

Use when a project chief-of-staff thread needs task-level orchestration for a complex task.

## Relationship

The chief-of-staff thread owns the project portfolio: routing, prioritization, Codex worker thread lifecycle, cross-task coordination, worktrees, commits, reconciliation, and final user-facing status.

The `codex-dynamic-workflows` skill owns the orchestration protocol for one complex task: success criteria, approvals, packets, simulated or real subagent work, integration, verification, reusable recipes, and the run artifact:

```text
.workflow/<slug>/
|-- plan.md
|-- state.json
|-- orchestration.md
|-- packets/
|-- results/
`-- final-report.md
```

Call into `codex-dynamic-workflows` when the CoS triage decides a task needs explicit task-level orchestration: packetization, integration, approval tracking, verification state, reusable workflow artifacts, or simulated subagent passes.

For the full relationship between CoS, dynamic workflow artifacts, RepoPrompt workflows, Codex worker threads, and oracle/review lanes, see [Execution mode stack](execution-mode-stack.md).

Short version: dynamic workflow owns complex-task orchestration; RepoPrompt workflows are preferred context/execution engines when available; the CoS remains the portfolio-level coordinator.

## When To Invoke

Invoke dynamic workflow mode when at least two are true:

- The task has independent research, implementation, review, migration, QA, docs, or design tracks.
- A success contract would reduce drift.
- Risk is present: destructive edits, external writes, deploys, secrets, production data, billing, user accounts, migrations, or broad repo-wide changes.
- Verification benefits from a separate pass from implementation.
- The workflow could become a reusable recipe.
- The user explicitly asks for a dynamic workflow, swarm, packets, subagents, or Claude Code-style orchestration.
- Delegation would materially improve speed, coverage, review independence, risk control, context management, or token economy even if the user did not ask for it by name.

Do not invoke it for small direct tasks. Use the build/review/investigate workflows directly.

## CoS Mapping

- CoS active goal -> `.workflow/<slug>/plan.md`
- CoS worker thread brief -> packet file under `packets/`
- Codex worker thread output -> result file under `results/`
- CoS ledger snapshot -> `state.json`
- CoS sequencing rules -> `orchestration.md`
- CoS final status -> `final-report.md`

The CoS may still create real Codex worker threads for packets, but the dynamic workflow packet plan defines what each worker owns. If no subagent/thread runner is appropriate, dynamic workflow's simulated packet pattern keeps isolated passes and result notes separate until integration.

If RepoPrompt is available, workers should use the matching RP workflow inside their packet when it fits:

- `rp-investigate` for research/diagnosis packets
- `rp-deep-plan` for planning packets
- `rp-build` for implementation packets
- `rp-orchestrate` for packet-internal decomposition
- `rp-review` for review packets
- `rp-refactor` for behavior-preserving cleanup packets
- `rp-optimize` for performance packets

Do not let a worker's RP workflow overwrite the `.workflow/` task source of truth. It may produce subplans and exports, but packet status and integration decisions belong in the dynamic workflow artifact.

## Setup

If the `codex-dynamic-workflows` skill is installed, invoke it or use its scripts:

```bash
python3 /Users/claire/.agents/skills/codex-dynamic-workflows/scripts/new_workflow.py "Task title"
```

Keep the run directory in a project-appropriate local location. Do not put sensitive raw data or bulky transcripts into workflow artifacts.

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

Packets should be disjoint where possible. For code-edit packets, avoid overlapping files/modules unless the CoS deliberately serializes them.

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

Use the dynamic workflow `collect_results.py` helper when useful:

```bash
python3 /Users/claire/.agents/skills/codex-dynamic-workflows/scripts/collect_results.py .workflow/<slug>
```

If packets disagree, inspect authoritative sources before choosing.

## Completion Audit

Before marking the task complete:

1. Verify workflow artifacts exist and are non-empty.
2. Confirm packet outputs are integrated.
3. Confirm approval-gated work had approval.
4. Confirm verification evidence satisfies success criteria.
5. Confirm any worker Codex Goals were audited against their verification surfaces.
6. Confirm commits/worktrees reconciled into the canonical repo/branch.
7. Confirm final report captures accepted/rejected results, conflicts, remaining risks, and next actions.

Use the dynamic workflow verification helper when useful:

```bash
python3 /Users/claire/.agents/skills/codex-dynamic-workflows/scripts/verify_workflow.py .workflow/<slug>
```

## Reusable Recipes

If a run produces a useful repeatable pattern, save a concise recipe in a project-appropriate location. Include trigger, plan shape, packet list, verification checklist, and known risks. Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.
