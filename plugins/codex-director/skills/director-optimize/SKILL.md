---
name: director-optimize
description: Runs the Codex Director optimization lane for performance, cost, memory, bundle size, throughput, or latency work. Use when a Director worker brief explicitly invokes $director-optimize for measurement-led improvement, bottleneck diagnosis, optimization patches, or performance verification.
---

# Director Optimize

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Optimize Workflow](../codex-director/references/optimize-workflow.md).
3. Report activation: `workflow-skill-loaded:$director-optimize`, selected workflow/playbook `director-optimize`, top-level control loop, metric target, helper/subagent lane plan, and evidence contract.
4. Establish a baseline or explain why one cannot be captured.
5. Change only after measurement, then verify improvement and regression risk.

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
- Treat final output as candidate evidence until Director readback and reconciliation.

## Output

Report baseline, change, post-change measurement, verification, regressions considered, unresolved risks, commit status when authorized, and cleanup/archive state.
