---
name: director-dynamic-workflow
description: Runs the Codex Director dynamic workflow bridge for complex task-level packetization and durable orchestration artifacts. Use when a Director brief explicitly invokes $director-dynamic-workflow for approvals, packets, multi-repo or multi-worker work, risky writes, integration tracking, or resumable .workflow state.
---

# Director Dynamic Workflow

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Dynamic Workflow Integration](../codex-director/references/dynamic-workflow-integration.md).
3. Load `$codex-dynamic-workflows` when available and the task needs its artifact protocol.
4. Report activation: selected workflow/playbook `director-dynamic-workflow`, top-level control loop, artifact path, approvals, helper/subagent lane plan, and evidence contract.
5. Create or update `.workflow/<slug>/` artifacts only inside the approved project scope.

## Workflow

1. Activate: restate complex task, selected workflow, top-level loop, artifact root, approvals, worker/monitor expectations, and evidence contract.
2. Confirm trigger: identify hard or soft triggers for dynamic workflow: packets, approvals, multi-repo/multi-worker work, high risk, integration tracking, long-lived monitors, or reusable recipe.
3. Create state: establish `.workflow/<slug>/plan.md`, `orchestration.md`, `packets/`, `results/`, and `final-report.md` when durable state is warranted.
4. Plan packets: each packet needs objective, owner, repo/path, workflow skill, files/sources, do/do-not, verification, helper policy, direct-leaf rationale, and readback/acceptance fields.
5. Sequence: define dependencies, parallel safety, approval gates, monitor cadence, stale/cancel policy, and integration order.
6. Staff or checkpoint: dispatch authorized packet workers, record active pending worktree/thread handles, or return coordinator-only packet briefs with an explicit dispatch/blocker/approval state.
7. Reconcile results: promote worker output to `results/` only after child-thread readback, evidence reconciliation, review/oracle status, helper/direct-leaf acceptance, and cleanup/archive state.
8. Integrate: resolve conflicts, update orchestration state, verify success criteria, and produce `final-report.md`.
9. Complete audit: confirm no active handle, pending readback, insufficient evidence, unmonitored pending worktree, or coordinator-only recommendation remains unresolved.

## Artifact Minimum

`plan.md` defines success criteria, constraints, approvals, verification, and packets. `orchestration.md` defines sequencing, monitors, state transitions, and integration. Packet files define work ownership. Result files hold accepted evidence only. `final-report.md` captures final status, risks, and next actions.

## Required Invariants

- Dynamic workflow owns one complex task, not the whole project portfolio.
- Packet work is never executed in the parent Director thread. A coordinator-only worker may draft packet briefs, but implementation needs authorized packet workers or explicit tiny direct-leaf authority.
- Pending worktree ids and queued packet workers are active handles and need callback coverage, a monitor, or `monitor_blocked:<reason>`.
- Promote worker results only after Director child-thread readback and evidence reconciliation.
- Keep secrets, raw private data, bulky transcripts, and credentials out of workflow artifacts.
- If monitor or dispatch cannot be created, record the exact blocker instead of presenting the task as monitored or complete.

## Output

Return artifact paths, packet list, approvals, worker/monitor handles, readback/evidence state, integration status, blockers, and next dispatch or acceptance action.
