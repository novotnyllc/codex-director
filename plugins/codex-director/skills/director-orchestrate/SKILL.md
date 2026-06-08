---
name: director-orchestrate
description: Runs the Codex Director worker orchestration lane for multi-item or ambiguous bounded assignments. Use when a Director worker brief explicitly invokes $director-orchestrate, or when a worker must coordinate subwork, helper/subagent lanes, sequencing, packet handoffs, or evidence reconciliation inside its assigned scope.
metadata:
  short-description: Coordinate bounded worker lane
---

# Director Orchestrate

## Quick Start

Use only when explicitly invoked by a Director brief or by the user. This skill is the worker-side orchestration lane, not the parent Director coordinator.

1. Read local instructions and the owning Director brief.
2. Load [Orchestrate Workflow](../codex-director/references/orchestrate-workflow.md).
3. Report activation: `workflow-skill-loaded:$director-orchestrate`, selected workflow/playbook, top-level control loop, scope, helper/subagent lane plan, direct-leaf status, and evidence contract.
4. Build or update a compact ledger for the bounded assignment.
5. Decompose into the fewest safe items, run helper/subagent lanes for non-trivial work, reconcile evidence, and return concise final evidence.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, planned RP-style helper profiles, and helper cleanup. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, goal, exact scope, leave-alone files/modules, sibling lanes, plan/artifact paths, model/thinking/fork rationale, expected output, evidence standard, and cleanup expectation.
- Fan out only disjoint helper lanes. Name siblings in every parallel brief, wait or poll regularly, process the first completed helper without duplicating in-flight work, and close finished helpers.
- Map RP roles as `explore` for narrow scouts, `pair` for complex/default subwork, `engineer` for clear bounded execution after the plan is known, and `design` for critique or user-facing polish.
- V2 evidence counts only after this worker reads the helper output, spot-checks material claims, summarizes verified evidence into the ledger, and records `close_agent` or `close_blocked:<reason>`.

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
- Do not treat `wait_agent`, `list_agents`, or helper final-status notifications as accepted item evidence.
- Keep visible updates to final evidence, blockers, decisions, or ownership-changing handoffs.

## Output

Return the ledger-relevant facts: work items, worker/helper handles if any, files/artifacts touched, verification, review/oracle status, native helper surface, V2 helper paths/evidence/owner verification/cleanup when used, unresolved risks, cleanup/archive state, and next action.
