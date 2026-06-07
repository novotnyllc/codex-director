---
name: director-orchestrate
description: Runs the Codex Director worker orchestration lane for multi-item or ambiguous bounded assignments. Use when a Director worker brief explicitly invokes $director-orchestrate, or when a worker must coordinate subwork, helper/subagent lanes, sequencing, packet handoffs, or evidence reconciliation inside its assigned scope.
---

# Director Orchestrate

## Quick Start

Use only when explicitly invoked by a Director brief or by the user. This skill is the worker-side orchestration lane, not the parent Director coordinator.

1. Read local instructions and the owning Director brief.
2. Load [Orchestrate Workflow](../codex-director/references/orchestrate-workflow.md).
3. Report activation: selected workflow/playbook, top-level control loop, scope, helper/subagent lane plan, direct-leaf status, and evidence contract.
4. Build or update a compact ledger for the bounded assignment.
5. Decompose into the fewest safe items, run helper/subagent lanes for non-trivial work, reconcile evidence, and return concise final evidence.

## Workflow

1. Scope and ledger: restate the assignment, done criteria, owning repo/path, constraints, commit authority, worker handle, and selected workflow.
2. Contextualize: identify project nouns, likely files/modules, risks, instructions, and missing facts. Use only narrow direct inspection before delegating deeper context.
3. Decide task shape: direct single-playbook, worker-internal orchestration, or dynamic workflow packetization. Default to orchestration for non-trivial work.
4. Research: run a scout/helper lane for unknowns that affect the plan. Summarize confirmed facts, uncertainty, and plan constraints.
5. Decompose: create up to five work items, preferably two or three. Each item needs done criteria, owner, workflow/playbook, helper lane, dependencies, review gate, and evidence.
6. Plan review: challenge item boundaries, dependency order, parallel safety, risk, tests, and acceptance criteria before execution continues.
7. Execute or staff lanes: perform only the work authorized by the brief. If coordinator-only, return packet briefs/checkpoints instead of implementing.
8. Reconcile: verify each item, read helper outputs, resolve conflicts, update ledger/artifacts, and decide accepted, blocked, stale, or insufficient evidence.
9. Complete: audit readback/evidence, helper/direct-leaf acceptance, review/oracle state, cleanup/archive state, and next action before final.

## Escalate Or Stop

Ask the Director to reroute when the work needs separate top-level Codex workers, approval gates, production/external writes, cross-repo integration, long-lived monitors, or `.workflow/<slug>/` artifacts. Stop instead of continuing when scope, authority, secrets, or destructive risk is unclear.

## Required Invariants

- Stay inside the repo/path, done criteria, commit authority, and constraints in the Director brief.
- Name `director-orchestrate` and the top-level control loop in activation, checkpoints, and final evidence.
- Non-trivial work needs a real helper/subagent lane or a clear blocked helper capability. Direct leaf is allowed only with separate tiny, mechanical, and low-risk rationale.
- A coordinator checkpoint is not task completion. It must include `next-packet-dispatched`, `monitor-scheduled`, `blocked-on-dispatch:<reason>`, or `awaiting-approval:<reason>`.
- Do not create nested top-level Codex workers unless the Director explicitly delegates that authority.
- Treat callbacks and final-looking messages as wake signals for Director readback, not acceptance.
- Keep visible updates to final evidence, blockers, decisions, or ownership-changing handoffs.

## Output

Return the ledger-relevant facts: work items, worker/helper handles if any, files/artifacts touched, verification, review/oracle status, unresolved risks, cleanup/archive state, and next action.
