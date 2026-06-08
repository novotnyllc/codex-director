---
name: director-optimize
description: Runs the Codex Director optimization lane for performance, cost, memory, bundle size, throughput, or latency work. Use when a Director worker brief explicitly invokes $director-optimize for measurement-led improvement, bottleneck diagnosis, optimization patches, or performance verification.
metadata:
  short-description: Run measurement-led optimization
---

# Director Optimize

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Optimize Workflow](../codex-director/references/optimize-workflow.md).
3. Report activation: `workflow-skill-loaded:$director-optimize`, selected workflow/playbook `director-optimize`, top-level control loop, metric target, helper/subagent lane plan, and evidence contract.
4. Establish a baseline or explain why one cannot be captured.
5. Change only after measurement, then verify improvement and regression risk.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, planned RP-style helper profiles, and helper cleanup. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, metric, workload, scope boundary, measurement command, sibling lanes, model/thinking/fork rationale, expected output, evidence standard, and cleanup expectation.
- Use `explore` helpers for bottleneck candidates, target/call-graph mapping, benchmark discovery, conventions, and scope boundaries. Use `pair` helpers for instrumentation/baseline or one optimization-and-harden loop. Use `design` only for bounded UX/perceived-performance critique.
- Keep optimization attribution serial. Parallel helpers are allowed only for disjoint scouting or explicitly approved alternative experiments; do not run multiple metric-changing patches in parallel.
- V2 evidence counts only after this worker spot-checks measurements, compares against variance/baseline, summarizes scoreboard impact, and records `close_agent` or `close_blocked:<reason>`.

## Workflow

1. Activate: restate optimization goal, metric, target threshold if any, selected workflow, top-level loop, helper policy, and verification contract.
2. Baseline: measure or locate existing reliable measurements. Record command, dataset, environment, sample size, and noise caveats.
3. Diagnose: identify likely bottlenecks using profiling, traces, logs, code inspection, or targeted experiments.
4. Helper lane: for non-trivial work, use a helper/subagent lane for profiling interpretation, hypothesis review, benchmark design, or regression review.
5. Plan: choose the smallest change likely to move the metric, with correctness risks and rollback path.
6. Implement: make scoped changes and preserve public behavior.
7. Re-measure: rerun comparable checks, compare to baseline, and capture regressions or noise.
8. Review: inspect correctness, concurrency, resource use, data safety, and user-facing behavior.
9. Finish: return baseline, changed metric, validation, review verdict, residual risk, commit status when authorized, and cleanup/archive state.

## Measurement Standard

Prefer repeatable commands and comparable inputs. If measurement is impossible or too expensive in the worker context, return `measurement_blocked:<reason>` and a safe next measurement plan rather than claiming improvement.

## Required Invariants

- Optimization is measurement-led; do not claim improvement without evidence or a stated measurement blocker.
- Keep correctness and public behavior ahead of speed.
- Use helper/subagent lanes for non-trivial bottleneck search, measurement, or review, or record a blocked helper capability.
- Stop for production load tests, destructive actions, cost-incurring experiments, or ambiguous metrics.
- If the work becomes broad or multi-lane, ask the Director to reroute to `$director-orchestrate` or `$director-dynamic-workflow`.
- Do not treat `wait_agent`, `list_agents`, or helper final-status notifications as measurement evidence.
- Treat final output as candidate evidence until Director readback and reconciliation.

## Output

Report baseline, change, post-change measurement, verification, regressions considered, native helper surface, V2 helper paths/evidence/owner verification/cleanup when used, unresolved risks, commit status when authorized, and cleanup/archive state.
