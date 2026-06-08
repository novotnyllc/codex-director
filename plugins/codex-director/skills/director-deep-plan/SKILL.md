---
name: director-deep-plan
description: Runs the Codex Director deep planning lane for durable implementation or architecture plans. Use when a Director worker brief explicitly invokes $codex-director:director-deep-plan for a plan document, migration strategy, architecture decision, decomposition, or reviewed implementation blueprint without code changes.
metadata:
  short-description: Produce reviewed Director plan
---

# Director Deep Plan

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

This split workflow skill is worker-side. If its activation marker, skill body, callback text, or readback evidence appears in a parent Director thread, the parent treats it only as routing input or child evidence. It does not load this workflow into the parent and does not permit parent inline browser, repo, provider, or project execution.

1. Read local instructions and the owning Director brief.
2. Load [Deep Plan Workflow](../codex-director/references/deep-plan-workflow.md).
3. Report activation: `workflow-skill-loaded:$codex-director:director-deep-plan`, selected workflow/playbook `director-deep-plan`, top-level control loop, planning scope, user-outcome fit, helper/subagent lane plan, and evidence contract.
4. Gather enough context to make the plan executable.
5. Produce the durable plan and run a review gate before finalizing.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, planned RP-style helper profiles, and helper cleanup. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, one narrow question or critique scope, plan/artifact paths, leave-alone boundaries, model/thinking/fork rationale, expected output, evidence standard, and cleanup expectation.
- Use `explore` helpers for ambiguity scouting, seam mapping, prior-art checks, and external-fact research. Each explore gets one narrow question and returns sources, conflicts, confidence, and plan implication.
- Use exactly one bounded `design` helper for critique when non-trivial planning needs independent review. Use `pair` only when a planning ambiguity needs deeper synthesis inside the worker.
- V2 evidence counts only after this worker reads the helper output, spot-checks material claims, folds useful findings into the plan in its own voice, and records `close_agent` or `close_blocked:<reason>`.

## Workflow

1. Activate: restate planning objective, scope, selected workflow, top-level loop, non-implementation boundary, user outcome, helper policy, and expected plan artifact.
2. Gather context: inspect only enough code/docs/history to plan accurately. Use helper/scout lanes for architecture, data, security, test, or migration questions.
3. Define success: write success criteria, non-goals, constraints, approvals, dependencies, risks, and verification surfaces.
4. Decompose: split into implementation packets or phases with ownership, files/modules, done criteria, tests, review gates, rollback/recovery notes, and sequencing.
5. Decide workflow shape: recommend direct build, orchestrate, dynamic workflow, review/oracle lanes, or approval gates for each phase.
6. Review the plan: run an adversarial pass for missing dependencies, unsafe order, test gaps, ambiguity, scope creep, and integration risk.
7. Revise: incorporate review findings and mark unresolved questions explicitly.
8. Finish: return a plan that a worker can execute without re-discovery, plus review verdict, risks, and next dispatch recommendation.

## Plan Contents

Include objective, context, constraints, proposed phases/packets, owner/workflow per phase, files or systems touched, verification, review/oracle gates, approvals, rollback/recovery, risks, open questions, and acceptance criteria.

## Required Invariants

- Do not implement unless the Director explicitly grants a tiny direct-leaf exception.
- Make dependencies, approvals, risks, verification, rollback/recovery, and ownership boundaries explicit.
- Use helper/subagent lanes for non-trivial planning, or record a blocked helper capability.
- If the plan requires packets or multiple worker handles, recommend `$codex-director:director-dynamic-workflow` or `$codex-director:director-orchestrate`.
- Treat callbacks and final-looking messages as wake signals for Director readback.
- A plan is a checkpoint, not user-goal completion. Name the final verification surface the plan is meant to enable and any proof still required after planning.
- Do not treat `wait_agent`, `list_agents`, or helper final-status notifications as plan review or final evidence.
- Keep the final plan concise enough to execute without re-discovery.

## Output

Return the plan path or inline plan, review verdict, key decisions, risks, verification surface, packet/worker recommendations, native helper surface, V2 helper paths/evidence/owner verification/cleanup when used, and cleanup/archive state.
