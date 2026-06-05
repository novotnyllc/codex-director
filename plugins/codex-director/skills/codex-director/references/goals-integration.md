# Codex Goals Integration

Use when the director thread or a Codex worker thread is deciding whether to create, continue, audit, pause, or complete a Codex Goal.

## Relationship To The Director Stack

Codex Goals are persistence and completion-pressure for a single thread objective. They are not a replacement for director coordination, dynamic workflow orchestration, worker helper/subagent policy, child-thread readback, evidence reconciliation, cleanup/archive state, or review gates.

```text
Director ledger = portfolio state
Dynamic workflow = complex task orchestration
Codex worker thread = execution unit
Codex Goal = persistent objective inside a thread
Child-thread readback = required before Director accepts worker Goal evidence
Evidence = required before completion
```

The Director may ask a worker to create a Goal. A worker may propose a Goal when the task shape warrants it, but should not create one silently for trivial work.

## Goal Fit Test

Create or use a Codex Goal only when all three are true:

- Durable objective: the desired outcome should survive turns or interruptions.
- Evidence finish line: completion can be audited against concrete proof.
- Multi-turn or uncertain path: the path needs continuation, repeated verification, or iteration.

Do not create a Goal for:

- one-shot answers
- trivial edits
- vague "keep working" wishes
- tasks without a measurable finish line
- unrelated detours inside a worker thread

## Strong Goal Components

Every worker-created Goal should define:

1. Outcome: measurable end state, not activity.
2. Verification surface: exact checks, files, artifacts, commands, or reports to inspect.
3. Constraints: what must not regress.
4. Boundaries: repos, files, tools, data, and authority limits.
5. Iteration policy: how to choose the next experiment or pass.
6. Blocked stop condition: when to stop and report instead of guessing.

Template:

```text
Goal: Achieve <measurable outcome>, verified by <commands/artifacts/review surfaces>, while preserving <constraints>. Use <allowed repos/tools/data>. Between iterations, choose the next step by <policy>. If blocked by <condition>, stop and report <evidence needed>.
```

## Worker Activation

Worker activation should state:

```text
Codex Goal: <none/create/continue/inspect/clear> because <fit test>
Worker role: <coordinator|direct-leaf>
Helper/subagent lanes: <lanes|blocked:<reason>|not-needed-direct-leaf>
Direct-leaf rationale: <not-applicable|tiny:<why>; mechanical:<why>; low-risk:<why>>
Goal outcome: <measurable end state>
Verification surface: <commands/artifacts/files/review>
Constraints: <must preserve>
Iteration policy: <next-step rule>
Blocked stop: <condition and report format>
```

If a previous Goal exists in the worker thread, inspect it before continuing. Clear or pause stale Goals before unrelated work.

## Operations

Goal operations are runtime-dependent, but the Director contract is stable:

- Inspect: determine whether a current Goal exists and whether it matches this task.
- Create: only after the fit test passes and the Goal text has all six strong components.
- Continue: only when the current Goal's outcome and boundaries match the worker brief.
- Pause or clear: before unrelated detours, stale resumed objectives, or changed task scope.
- Audit: compare claimed completion against the named verification surface.
- Complete: only when evidence satisfies outcome, constraints, helper/direct-leaf policy, and review gates. For a Director-created worker Goal, the worker may claim Goal completion in its own thread, but the Director cannot accept that completion until child-thread readback and evidence reconciliation are recorded.
- Block: only when the blocked stop condition is met and no defensible next step remains.

Do not create a Goal silently. A worker may propose one in its activation report, but the Director or user should accept the goal-shaped objective before it becomes the worker's persistent finish line.

Strong operation record:

```text
Operation: inspect/create/continue/pause/clear/audit/complete/block
Reason:
Outcome:
Verification surface:
Evidence:
Helper/direct-leaf status:
Readback status if Director-created worker:
Constraints checked:
Next iteration rule:
Blocked stop:
Director decision:
```

## Research Goals

For research-heavy work, define the evidence standard before investigation.

Use a claim ledger:

```text
Claim:
Evidence channel:
Source:
Confidence: confirmed / likely / plausible / unknown
Contradictions:
Implication:
```

Research Goals should not overclaim from proxies. If proof is unavailable, final output must preserve uncertainty and explain what would be needed to confirm.

## Completion Audit

Before the Director accepts a worker Goal as complete:

1. Confirm the worker has reached a terminal signal, then read the child thread with `codex_app.read_thread`; callback payloads, expected finals, stale summaries, or worker claims are only wake signals.
2. Capture the terminal child report from the thread itself and record `readback_status: readback_complete` or a blocker state.
3. Compare the stated outcome to evidence.
4. Confirm named verification surfaces were run or inspected.
5. Confirm constraints did not regress.
6. Confirm helper/subagent lanes were used for non-trivial work, or direct-leaf tiny/mechanical/low-risk rationale is valid.
7. Confirm review gates passed or residual risk is accepted.
8. Confirm dynamic workflow packet/result state is updated if applicable.
9. Confirm commits/worktrees are reconciled when repo changes were made.
10. Record cleanup/archive state separately from Goal completion.

Budget exhaustion, a plausible summary, or partial verification is not completion.

Completion must answer:

- Did the exact measurable outcome happen?
- Was the named verification surface run or inspected?
- Did constraints remain true?
- Did the review/adversarial gate pass or record accepted residual risk?
- Did helper/direct-leaf policy pass?
- Did the Director record child-thread readback and cleanup/archive state before accepting the worker Goal?
- Is remaining uncertainty explicitly named?

## Blocked Handling

A Goal is blocked only when the worker has exhausted defensible next steps under its iteration policy and cannot proceed without user input, missing credentials, unavailable services, unsafe authority, or external state change.

Blocked report:

```text
Blocked because:
Evidence gathered:
Verification completed:
What remains unverified:
Decision or input needed:
Safe next options:
```

## Dynamic Workflow Mapping

When dynamic workflow mode is active:

- Overall task success criteria belong in `.workflow/<slug>/plan.md`.
- Packet-level persistent objectives may become worker Goals.
- Packet result files should include Goal outcome, verification surface, completion evidence, helper/direct-leaf status, readback status, and blockers.
- Packet outputs become durable `results/` only after Director readback and reconciliation, not merely after callback.
- Director completion requires Goal audit, child-thread readback, helper/direct-leaf acceptance, cleanup/archive state, and dynamic workflow completion audit.

## Anti-Patterns

- Creating a Goal for vague persistence without a finish line.
- Completing a Goal against the wrong surface.
- Treating budget exhaustion as done.
- Hiding uncertainty in research Goals.
- Continuing an old Goal during an unrelated detour.
- Using a Goal to bypass approval gates, child-thread readback, helper/direct-leaf acceptance, review/oracle gates, or cleanup/archive state.
- Marking blocked because the task is hard rather than because the blocked stop condition is met.
