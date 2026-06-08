---
name: director-dynamic-workflow
description: Runs the Codex Director dynamic workflow bridge for complex task-level packetization and durable orchestration artifacts. Use when a Director brief explicitly invokes $codex-director:director-dynamic-workflow for approvals, packets, multi-repo or multi-worker work, risky writes, integration tracking, or resumable .workflow state.
metadata:
  short-description: Packetize complex Director work
---

# Director Dynamic Workflow

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

This split workflow skill is worker-side. If its activation marker, skill body, callback text, or readback evidence appears in a parent Director thread, the parent treats it only as routing input or child evidence. It does not load this workflow into the parent and does not permit parent inline browser, repo, provider, or project execution.

1. Read local instructions and the owning Director brief.
2. Load [Dynamic Workflow Integration](../codex-director/references/dynamic-workflow-integration.md).
3. Load `$codex-dynamic-workflows` when available and the task needs its artifact protocol.
4. Report activation: `workflow-skill-loaded:$codex-director:director-dynamic-workflow`, selected workflow/playbook `director-dynamic-workflow`, top-level control loop, artifact path, approvals, helper/subagent lane plan, and evidence contract.
5. Create or update `.workflow/<slug>/` artifacts only inside the approved project scope.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, planned RP-style helper profiles, and helper cleanup. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, workflow artifact paths, packet or artifact scope, do/do-not boundaries, sibling lanes, model/thinking/fork rationale, expected output, evidence standard, and cleanup expectation.
- Use V2 only under this worker for packet scouting, packet critique, artifact consistency checks, or bounded draft assistance. Map `explore` to packet/source scouting, `design` to critique, `pair` to complex packet-shape synthesis, and `engineer` only to mechanical artifact assistance.
- V2 helpers are not packet owners, do not create accepted `results/`, and do not replace Director-created packet worker threads.
- V2 helper evidence counts only after this worker spot-checks it, reflects it in packet/coordination evidence, and records `close_agent` or `close_blocked:<reason>`.

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
- Promote V2 helper findings only through this worker's packet/coordination evidence, never directly into accepted `results/`.
- Keep secrets, raw private data, bulky transcripts, and credentials out of workflow artifacts.
- If monitor or dispatch cannot be created, record the exact blocker instead of presenting the task as monitored or complete.

## Output

Return artifact paths, packet list, approvals, worker/monitor handles, readback/evidence state, native helper surface, V2 helper paths/evidence/owner verification/cleanup when used, integration status, blockers, and next dispatch or acceptance action.
