---
name: director-deep-plan
description: Runs the Codex Director deep planning lane for durable implementation or architecture plans. Use when a Director worker brief explicitly invokes $director-deep-plan for a plan document, migration strategy, architecture decision, decomposition, or reviewed implementation blueprint without code changes.
---

# Director Deep Plan

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Deep Plan Workflow](../codex-director/references/deep-plan-workflow.md).
3. Report activation: selected workflow/playbook `director-deep-plan`, top-level control loop, planning scope, helper/subagent lane plan, and evidence contract.
4. Gather enough context to make the plan executable.
5. Produce the durable plan and run a review gate before finalizing.

## Workflow

1. Activate: restate planning objective, scope, selected workflow, top-level loop, non-implementation boundary, helper policy, and expected plan artifact.
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
- If the plan requires packets or multiple worker handles, recommend `$director-dynamic-workflow` or `$director-orchestrate`.
- Treat callbacks and final-looking messages as wake signals for Director readback.
- Keep the final plan concise enough to execute without re-discovery.

## Output

Return the plan path or inline plan, review verdict, key decisions, risks, verification surface, packet/worker recommendations, and cleanup/archive state.
