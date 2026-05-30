# Execution Mode Stack

Use this to decide how the chief-of-staff thread, dynamic workflow artifacts, RepoPrompt workflows, Codex worker threads, and oracle/review lanes fit together.

## Core Rule

There is only one top-level coordinator: the chief-of-staff Codex thread.

Everything else is an execution mode selected by the chief thread for a specific task:

```text
Chief-of-staff Codex thread
|-- direct answer or small local action
|-- one Codex worker thread using a selected workflow
|-- dynamic workflow for complex task orchestration
|   `-- packets mapped to Codex worker threads or simulated packet passes
`-- oracle/review/research lanes attached where needed
```

## Responsibilities

### Chief-of-staff thread

Owns:

- project portfolio and active work ledger
- routing to repo/path
- whether to use direct work, a worker thread, or a dynamic workflow run
- Codex worker thread creation, steering, monitoring, archival
- worktree/branch/commit/reconciliation policy
- final user-facing status

Does not own:

- deep implementation context
- worker-internal tactical decisions
- raw transcript dumps

### Dynamic workflow

Use `codex-dynamic-workflows` when the task needs task-level orchestration, not just a ledger.

Owns:

- success criteria and task-level plan
- approval gates
- packetization
- simulated subagent passes when no runner is available
- packet integration
- verification strategy and verification state
- reusable workflow recipes
- `.workflow/<slug>/` task artifact
- `plan.md`
- `state.json`
- `orchestration.md`
- `packets/`
- `results/`
- `final-report.md`
- workflow completeness audit

Dynamic workflow is not a replacement for the CoS. It is the CoS's task-level orchestrator for one complex task. The CoS still decides when to invoke it, how to staff packets with Codex worker threads, how to manage worktrees/commits, and how to reconcile the result into the larger project.

### RepoPrompt workflows

Use RepoPrompt workflows as preferred execution implementations when RepoPrompt is available and fits the task.

Owns:

- codebase context building
- oracle reasoning over curated context
- RP subagent execution when useful
- exports for plan/review handoff
- live implementation/review/investigation loops

RepoPrompt is not the durable project ledger. It is a high-quality context and execution engine.

### Codex worker threads

Own:

- one bounded packet or task
- activation report
- local plan and verification
- concise evidence
- commits for their work when authorized

Workers must report scope expansion, blockers, and verification gaps back to the CoS.

## Selection Order

Delegation is proactive. The user does not need to say "subagents", "swarm", "parallel", or "dynamic workflow" for the CoS to use them. Choose delegation when it improves speed, coverage, review independence, risk control, context management, or token economy.

### 1. Tiny or advisory

Use direct response or direct local action.

Examples:

- answer a narrow question
- inspect one file
- fix a typo
- run a simple command

No dynamic workflow. No RP orchestration. Fast self-check is enough.

### 2. Single bounded implementation, review, or investigation

Create one Codex worker thread if delegation helps, or do it directly if small.

Use the selected workflow reference:

- build
- review
- investigate/research
- deep plan
- refactor
- optimize
- prompt export
- Browser ChatGPT oracle

Prefer RP implementations where available:

- `rp-build` for bounded implementation
- `rp-review` for code review
- `rp-investigate` for deep read-only diagnosis
- `rp-deep-plan` for durable plans
- `rp-refactor` for behavior-preserving cleanup
- `rp-optimize` for measured performance loops
- `rp-oracle-export` for packaging prompts

No dynamic workflow unless durable packet/state artifacts are useful.

### 3. Multi-item but short-lived

Use orchestration without a durable `.workflow/` run when the task is multi-step but not large enough to need long-lived artifacts.

Preferred if available:

- `rp-orchestrate` inside the responsible Codex worker thread.

Otherwise:

- follow the CoS orchestrate workflow reference
- create multiple Codex worker threads only for disjoint items
- keep the CoS ledger as the state

### 4. Complex, risky, long-running, or reusable

Invoke `codex-dynamic-workflows`.

Use this when the task needs:

- task-level orchestration
- success criteria and approval gates
- approval tracking
- packet files
- result files
- integration checklist
- final report
- reusable workflow recipe
- many packets or cross-track coordination

When RepoPrompt is also available, use both:

1. CoS invokes `codex-dynamic-workflows` to create the task orchestration run.
2. CoS uses the dynamic workflow plan/state as the task source of truth.
3. For each packet, CoS dispatches a Codex worker thread.
4. The worker uses the best RP workflow for its packet when useful.
5. For multi-packet execution inside one worker, use `rp-orchestrate`.
6. Worker writes concise result evidence into `results/`.
7. CoS integrates, verifies, reconciles commits/worktrees, and writes final report.

## How `rp-orchestrate` Fits

`rp-orchestrate` is a live execution workflow. It is best when the current worker needs to decompose work, dispatch RepoPrompt subagents, verify items, and keep moving.

`codex-dynamic-workflows` is task-level orchestration. It is best when the task needs success criteria, packetization, approval gates, simulated or real subagent passes, integration, verification state, and a final audit trail.

Use both when the task is complex and RepoPrompt is available:

```text
CoS creates .workflow/<slug>/
CoS creates packet files
Codex worker thread handles Packet 02
Worker invokes rp-orchestrate for that packet if it has sub-items
Worker writes results/02-*.md
CoS integrates all packet results
```

Do not let `rp-orchestrate` create a second top-level plan that conflicts with `.workflow/plan.md`. It may create implementation subplans, but the dynamic workflow artifact remains the task source of truth.

## How Other RP Skills Fit

Use the narrow RP skill that matches each packet:

- Research packet -> `rp-investigate` or context/question mode
- Plan packet -> `rp-deep-plan`
- Build packet -> `rp-build`
- Review packet -> `rp-review`
- Refactor packet -> `rp-refactor`
- Optimize packet -> `rp-optimize`
- Browser/external oracle packet -> prompt export, then Browser ChatGPT oracle

The CoS should predict likely skills in the worker brief, but the worker must re-run skill activation after reading local instructions.

## Conflict Rules

- If CoS and dynamic workflow disagree, the CoS updates the workflow artifact or pauses for user input.
- If RP findings conflict with workflow plan, record the conflict in `results/` and update `plan.md` before implementation continues.
- If worker threads disagree, inspect authoritative repo/source evidence before choosing.
- If a packet grows beyond its scope, stop and re-plan rather than silently widening.

## Completion Rule

A task is complete only when all selected layers agree:

- CoS ledger says done.
- Workflow artifact, if used, passes completion audit.
- Worker threads have reported evidence.
- Review gates have passed or residual risk is accepted.
- Required commits are made.
- Worktrees are reconciled into the canonical repo/branch.
- Final user-facing status is concise and source-backed.
