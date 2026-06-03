# Codex Goals Integration

Use when the director thread or a Codex worker thread is deciding whether to create, continue, audit, pause, or complete a Codex Goal.

## Relationship To The Director Stack

Codex Goals are persistence and completion-pressure for a single thread objective. They are not a replacement for director coordination, dynamic workflow orchestration, or review gates.

```text
Director ledger = portfolio state
Dynamic workflow = complex task orchestration
Codex worker thread = execution unit
Codex Goal = persistent objective inside a thread
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
Goal outcome: <measurable end state>
Verification surface: <commands/artifacts/files/review>
Constraints: <must preserve>
Iteration policy: <next-step rule>
Blocked stop: <condition and report format>
```

If a previous Goal exists in the worker thread, inspect it before continuing. Clear or pause stale Goals before unrelated work.

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

1. Compare the stated outcome to evidence.
2. Confirm named verification surfaces were run or inspected.
3. Confirm constraints did not regress.
4. Confirm review gates passed or residual risk is accepted.
5. Confirm dynamic workflow packet/result state is updated if applicable.
6. Confirm commits/worktrees are reconciled when repo changes were made.

Budget exhaustion, a plausible summary, or partial verification is not completion.

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
- Packet result files should include Goal outcome, verification surface, completion evidence, and blockers.
- Director completion requires both Goal audit and dynamic workflow completion audit.

## Anti-Patterns

- Creating a Goal for vague persistence without a finish line.
- Completing a Goal against the wrong surface.
- Treating budget exhaustion as done.
- Hiding uncertainty in research Goals.
- Continuing an old Goal during an unrelated detour.
- Using a Goal to bypass approval gates.
