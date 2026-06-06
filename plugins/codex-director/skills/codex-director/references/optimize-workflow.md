# Optimize Workflow

Use for performance, latency, memory, allocation, throughput, frame time, bundle size, or efficiency work.

## Principle

Performance work only improves what can be measured. The loop is: map, measure, change one thing, re-measure, review, decide.

For Director-created optimization workers, non-trivial optimization requires real helper/subagent evidence for bottleneck scouting, measurement design, verification, or critique. Direct leaf is worker-internal only for tiny, mechanical, low-risk measurement or tuning changes with separate rationale.

## Phase 0: Target And Stop Rule

Confirm the worker launch contract first: model, thinking level plus rationale, commit authority, required skills/workflows, repo/path, helper/direct-leaf policy, and evidence format. Record skills considered, loaded, skipped, and not loaded in activation.

Translate the user request into:

- metric name and unit
- workload or scenario
- current baseline source
- target threshold or "until gains plateau"
- correctness constraints
- acceptable risk

If the target is vague, research first. Do not optimize "slow" without a measurable proxy.

## Phase 1: Bottleneck Scouting

Run scouts before planning. For non-trivial Director-created optimization, at least one scout/helper lane is mandatory unless direct-leaf tiny/mechanical/low-risk rationale is valid; if helper capability is unavailable, report `blocked:<reason>` instead of optimizing monolithically:

- Target implementation and call graph.
- Callers and hot loops.
- Input construction and data dependencies.
- Adjacent operations in the same path.
- Existing benchmarks, profiler traces, perf TODOs.
- Project measurement commands and conventions.
- Scope boundary: files in and out.

The bottleneck scout should look beyond the named function. The expensive part may be a caller, repeated input construction, sync I/O, locking, serialization, rendering, or cache miss pattern.

Scout output:

- 2-3 ranked candidates.
- file:line refs.
- "suspicious because" rationale.
- known measurement command.

## Phase 2: Measurement Plan

Before any optimization:

- choose the metric
- choose command/workload
- define sample count
- define variance handling
- decide how to discard outliers
- decide where instrumentation lives
- ensure debug-only instrumentation is gated or removable

Preferred path: use a context/planning tool to design instrumentation and first candidates from scout findings.

Create a scoreboard before changing behavior:

```text
Target:
Baseline command:
Baseline value:
Budget / threshold:
Constraints:
Iteration:
Change:
Result:
Verdict:
Next decision:
```

If the metric cannot be measured, the first work item is instrumentation or benchmark setup. Do not optimize against vibes.

## Phase 3: Baseline

Land instrumentation or benchmark harness first if needed. Then capture baseline.

Rules:

- Do not optimize before baseline.
- Run enough samples to understand variance.
- Record environment and command.
- Commit instrumentation separately when it is worth preserving.
- If variance hides likely gains, improve measurement before optimizing.
- Prefer debug/test-only instrumentation. Do not add production overhead unless the task explicitly asks for observability.

Maintain a scoreboard:

```text
Iteration | Change | Commit | Command | Median | P95/Peak/etc | Delta | Notes
Baseline  | none   | <hash> | <cmd>   | ...    | ...          | ...   | ...
```

## Phase 4: Optimization Loop

For each iteration:

1. Pick one bottleneck candidate.
2. Make one attributed change.
3. Run correctness tests.
4. Re-measure.
5. Append scoreboard row.
6. Review result.
7. Decide keep, revise, revert, or stop.

Do not combine multiple performance ideas in one iteration unless they cannot be separated.

Use one worker for a full optimize-and-harden iteration when possible: implement, verify correctness, measure, and report. Use worker-internal helpers for disjoint measurement, bottleneck, verification, or review lanes when that reduces bias or context load. Use separate top-level workers only when measurement and implementation can be cleanly isolated by the Director.

## Phase 5: Oracle / Adversarial Decision

Use an oracle or review lane at decision points:

- Did the change earn its risk?
- Is the measured gain outside variance?
- Did correctness regress?
- Is complexity justified?
- Should the loop continue?
- Which candidate is next?

Respect stop signals: target met, plateau, risk too high, measurement unreliable, or iteration cap reached.

Default iteration cap is five optimization loops. Before launching a sixth loop, surface the current scoreboard and ask the Director or user for explicit continuation authority; do not extend the cap just because another candidate remains.

The oracle/review lane should see the scoreboard and evidence, not the whole transcript. Ask for a stop/continue verdict and the one next experiment that would most likely matter.

When an optimization worker reaches this decision point, it returns an Oracle Request Packet with the scoreboard, measurement caveats, correctness evidence, candidate list, helper/direct-leaf status, and requested stop/continue verdict. The Director chooses and messages the oracle/review lane, then routes the decision back. Oracle output is advisory; the worker still verifies and reports final evidence, and the Director later accepts only after child-thread readback and reconciliation.

## Phase 6: Finalization

- Remove or gate temporary instrumentation.
- Keep benchmarks that should remain.
- Run final correctness and measurement checks.
- Commit final logical units.
- Record final before/after numbers.
- Run final review.

## Evidence

Report:

- metric and baseline
- command and environment
- scoreboard
- final delta
- commit hash per attributed change
- tests/checks
- review verdict
- helper/subagent lanes used, or direct-leaf rationale with separate tiny, mechanical, and low-risk detail
- cleanup/archive expectation and worktree/branch reconciliation state
- reason for stopping

For Director acceptance, final optimization evidence is not complete until the Director reads the child thread with `codex_app.read_thread`, captures the terminal report, reconciles measurement/correctness/review/helper status, and records cleanup/archive state.

## Anti-Patterns

- Optimizing without a baseline.
- Reporting relative terms like "faster" without numbers.
- Shipping temporary instrumentation accidentally.
- Combining unrelated performance ideas in one iteration.
- Continuing iterations after stop criteria are met.
- Claiming optimization success from a callback, oracle verdict, or stale summary before child-thread readback.
- Treating non-trivial optimization as complete without helper/subagent evidence or valid direct-leaf rationale.
