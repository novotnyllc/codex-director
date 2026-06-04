# Execution Mode Stack

Use this to decide how the director thread, dynamic workflow artifacts, self-contained workflow playbooks, Codex worker threads, and oracle/review lanes fit together.

## Core Rule

There is only one top-level coordinator: the director Codex thread.

Everything else is an execution mode selected by the director thread for a specific task:

```text
Director Codex thread
|-- plugin-bundled hooks
|   |-- reinforce role boundaries, routing, compaction recovery, closeout
|-- `codex_app` thread layer
|   |-- create/title/pin/read/steer/archive worker threads through exposed `codex_app` contracts
|   `-- resolve project targets and preserve worker lifecycle evidence through latest-Codex contracts
|-- coordination and status answers only
|-- one Codex worker thread using a selected workflow
|-- dynamic workflow for complex task orchestration
|   |-- packets mapped to Codex worker threads
|   `-- nested worker workflows or sub-agents only under an owning packet
|-- Codex Goals inside worker threads when persistence is warranted
`-- oracle/review/research lanes attached where needed
```

## Responsibilities

### Director thread

Owns:

- project portfolio and active work ledger
- routing to repo/path
- whether a request is coordination-only, one worker thread, or a dynamic workflow run
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
- worker-thread packet ownership
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

Dynamic workflow is not a replacement for the Director. It is the Director's task-level orchestrator for one complex task. The Director still decides when to invoke it, how to staff packets with Codex worker threads, what worktree/commit policy applies, and which worker owns integration or reconciliation into the larger project.

### Latest Codex Runtime And Context Tools

Use exposed `codex_app` thread/project tools for worker-thread lifecycle, with the active tool schema as the source of truth. Use optional context, oracle, browser, and worker-internal sub-agent tools for evidence or helper phases when they fit the task. Do not make the Director operating model depend on any non-`codex_app` thread runner or unexposed lifecycle API.

Owns:

- Codex worker-thread creation, steering, polling, archival, and cleanup through exposed `codex_app` contracts
- Director hook reminders for role boundaries, compaction recovery, nested helper evidence, and closeout
- codebase context building
- oracle reasoning over curated context, mediated by the Director when implemented as a separate Codex thread
- worker-internal sub-agent or execution helpers when useful
- exports for plan/review handoff
- live implementation/review/investigation loops inside the owning worker thread

Context and helper tools are not the durable project ledger and are not the `codex_app` thread/project layer. They can support self-contained workflow phases, but they do not replace latest-Codex worker lifecycle tooling. See [Latest Codex runtime tooling](runtime-adapters.md) for the concrete Codex tool contract and project-target rules.

### Codex worker threads

Own:

- one bounded packet or task
- activation report
- local plan and verification
- Codex Goal when the packet/task needs persistence
- concise evidence
- commits for their work when authorized

Workers must report scope expansion, blockers, and verification gaps back to the Director. Workers that need oracle review return an Oracle Request Packet to the Director; they do not create, continue, or message oracle threads directly unless explicitly delegated that authority.

### Director availability invariant

The Director does not perform project work. It stays available for instructions, check-ins, steering, coordination, workflow-state updates, evidence integration, and final status. Any implementation, investigation, review, testing, refactor, optimization, or research work belongs in a Codex worker thread. Tiny work still gets a tiny worker brief.

## Selection Order

Delegation is proactive. The user does not need to say "swarm", "parallel", "dynamic workflow", "subagents", "oracle", or "Pro" for the Director to use available delegation mechanisms. Choose delegation when it improves speed, coverage, review independence, risk control, context management, model diversity, or token economy.

### 1. Coordination-only

Use a direct response only for coordination, status, routing, or user-instruction clarification.

Examples:

- report worker status
- explain the current plan
- ask for a missing approval
- update the Director ledger from worker evidence

No project execution in the Director thread.

### 2. Single bounded implementation, review, or investigation

Create one Codex worker thread. Do not do it directly in the Director thread.

Use the selected workflow reference:

- build
- review
- investigate/research
- deep plan
- refactor
- optimize
- prompt export
- Browser ChatGPT Pro oracle

Use optional tooling only to implement these playbooks; do not substitute tool names for the workflow itself.

No dynamic workflow unless durable packet/state artifacts are useful; the single worker still executes the work.

### 3. Multi-item but short-lived

Use orchestration without a durable `.workflow/` run when the task is multi-step but not large enough to need long-lived artifacts.

- follow the Director orchestrate workflow reference
- create multiple Codex worker threads only for disjoint items
- require each worker to choose a helper/context strategy and use worker-internal sub-agents for disjoint scouting, model/function selection, context mapping, verification, or review when they reduce risk, context load, or token cost
- keep the Director ledger as the state

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

When optional context/delegation tools are also available, use them as implementations under the same artifact source of truth:

1. Director invokes `codex-dynamic-workflows` to create the task orchestration run.
2. Director uses the dynamic workflow plan/state as the task source of truth.
3. For each packet, Director dispatches a Codex worker thread.
4. The worker uses the relevant self-contained workflow playbook for its packet.
5. For packet-internal complexity, the worker chooses a helper/context strategy and may use the orchestration workflow, nested dynamic workflow artifacts, or native sub-agents only under that packet.
6. Worker writes concise result evidence into `results/`.
7. Director dispatches any integration, verification, or reconciliation work to workers, records accepted evidence, and writes final report.

## How Recursive Helpers Fit

Worker-internal helpers are implementation helpers. They are best when the current worker needs to decompose work, select likely models/functions/files/tests, map context slices, delegate a bounded subtask, verify items, review a narrow surface, or package context without bloating the owning worker thread.

`codex-dynamic-workflows` is task-level orchestration. It is best when the task needs success criteria, packetization, approval gates, worker-thread packet passes, integration, verification state, and a final audit trail.

Use both when the task is complex and optional tooling is available:

```text
Director creates .workflow/<slug>/
Director creates packet files
Codex worker thread handles Packet 02
Worker uses nested workflow artifacts or native sub-agents only if the packet has real sub-items
Worker writes results/02-*.md
Director records accepted packet evidence and coordinates any integration worker
```

Do not let a worker-internal helper create a second top-level plan that conflicts with `.workflow/plan.md`. It may create implementation subplans under its packet, but the parent dynamic workflow artifact remains the task source of truth.

Latest Codex `codex_app` worker/thread/project tooling is the premise of this skill. Director setup confirms the contract before operating, and packet work must not execute in the Director thread.

## How Workflow Playbooks Fit

Use the narrow self-contained workflow that matches each packet:

- Research packet -> investigate/research workflow
- Plan packet -> deep plan workflow
- Build packet -> build workflow
- Review packet -> review workflow
- Refactor packet -> refactor workflow
- Optimize packet -> optimize workflow
- Browser/external oracle packet -> Director-mediated Browser ChatGPT Pro oracle; use prompt export only for durable payload, upload/chunking, retry, audit, or handoff needs; if Pro is unavailable or ambiguous, route to built-in main/`xhigh` oracle/review fallback unless Pro-only was explicit

The Director should predict likely skills in the worker brief, but the worker must re-run skill activation after reading local instructions. Oracle packets flow through the Director: `worker -> Director -> oracle lane -> Director -> worker/result`.

## How Codex Goals Fit

Use Codex Goals inside the director thread or worker threads only when the objective is durable, evidence-based, and likely to span turns or iterations.

- Director project ledger tracks portfolio work.
- Dynamic workflow tracks complex task orchestration.
- Codex Goal gives a single thread a persistent finish line.

Worker Goals must name the outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition. The Director should audit evidence before accepting a Goal as complete. See [Codex Goals integration](goals-integration.md).

## Conflict Rules

- If Director and dynamic workflow disagree, the Director updates the workflow artifact or pauses for user input.
- If tooling, oracle, or review-lane findings conflict with the workflow plan, record the conflict in `results/` and update `plan.md` before implementation continues.
- If worker threads disagree, dispatch a focused investigation/review worker or require authoritative repo/source evidence before choosing.
- If helper-tool output conflicts with authoritative repo/workflow evidence, trust the source evidence and rerun or revise the helper pass.
- If a packet grows beyond its scope, stop and re-plan rather than silently widening.

## Completion Rule

A task is complete only when all selected layers agree:

- Director ledger says done.
- Workflow artifact, if used, passes completion audit.
- Worker threads have reported evidence.
- Review gates have passed or residual risk is accepted.
- Authorized commits or PR evidence are complete, or `no-commit` evidence is ready for user/Director decision.
- Worktrees are reconciled into the canonical repo/branch.
- Runtime handles are collected, archived, canceled, or cleaned up.
- Final user-facing status is concise and source-backed.
