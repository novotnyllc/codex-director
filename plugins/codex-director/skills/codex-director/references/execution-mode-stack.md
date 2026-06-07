# Execution Mode Stack

Use this to decide how the director thread, dynamic workflow artifacts, self-contained workflow playbooks, Codex worker threads, and oracle/review lanes fit together.

## Core Rule

There is only one top-level coordinator: the director Codex thread.

Everything else is an execution mode selected by the director thread for a specific task:

```text
Director Codex thread
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
- Codex worker thread creation, steering, monitoring, readback, acceptance, and archival
- worktree/branch/commit/reconciliation policy
- final user-facing status after child-thread readback and evidence reconciliation

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
- verification strategy and verification tracking
- reusable workflow recipes
- `.workflow/<slug>/` task artifact
- `plan.md`
- `orchestration.md`
- `packets/`
- `results/`
- `final-report.md`
- workflow completeness audit

Dynamic workflow is not a replacement for the Director. It is the Director's task-level orchestrator for one complex task. The Director still decides when to invoke it, how to staff packets with Codex worker threads, what worktree/commit policy applies, and which worker owns integration or reconciliation into the larger project.

If the Director creates a coordinator-only worker for packetization or integration, that worker's checkpoint is not packet execution. After a coordinator checkpoint, the Director must create or continue the next packet/review/oracle worker, record the monitor covering it, or record an explicit dispatch blocker/approval wait state.

### Latest Codex Runtime And Context Tools

Use exposed `codex_app` thread/project tools for worker-thread lifecycle, with the active tool schema as the source of truth. Use optional context, oracle, browser, and worker-internal sub-agent tools for evidence or helper phases when they fit the task. Do not make the Director operating model depend on any non-`codex_app` thread runner or unexposed lifecycle API.

Owns:

- Codex worker-thread creation, steering, polling, archival, and cleanup through exposed `codex_app` contracts
- explicit Director thread/project contracts, worker briefs, activation reports, ledgers, and closeout evidence
- codebase context building
- oracle reasoning over curated context, mediated by the Director when implemented as a separate Codex thread
- worker-internal sub-agent or execution helpers when useful
- optional scratch/handoff artifacts for plan/review context when a stable path is useful
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

The Director does not perform project work. It stays available for instructions, check-ins, steering, coordination, workflow artifact updates, evidence integration, and final status. Any implementation, investigation, review, testing, refactor, optimization, research work, or repo/docs/code/prod inspection belongs in a Codex worker thread. Tiny project work still gets a tiny worker brief when it requires repo/docs/code/prod inspection or execution.

Direct leaf is a worker-internal execution mode only. It cannot authorize Director-inline project work. A worker may classify itself as direct leaf only when the assigned task is explicitly tiny, mechanical, and low-risk, and both activation and final evidence include separate rationale for tiny, mechanical, and low-risk.

## Selection Order

Delegation is proactive. The user does not need to say "swarm", "parallel", "dynamic workflow", "subagents", "oracle", or "Pro" for the Director to use available delegation mechanisms. Choose delegation when it improves speed, coverage, review independence, risk control, context management, model diversity, or token economy.

### 1. Coordination-only

Use a direct response only for coordination, status, routing, or user-instruction clarification.

Examples:

- report worker status
- explain the current plan
- ask for a missing approval
- update the Director ledger from worker evidence

No project execution in the Director thread. Direct leaf is not an exception to this rule; it is only a worker-internal shortcut for tiny, mechanical, low-risk work.

### 2. Single bounded implementation, review, or investigation

Create one Codex worker thread. Do not do it directly in the Director thread.

Use the selected explicit workflow skill and its matching reference:

- `$director-build` for build
- `$director-review` for review
- `$director-investigate` for investigate/research
- `$director-deep-plan` for deep plan
- `$director-refactor` for refactor
- `$director-optimize` for optimize
- `$director-browser-oracle` for Browser ChatGPT Pro oracle

Use optional tooling only to implement these playbooks; do not substitute tool names for the workflow itself.

No dynamic workflow unless durable packet/result artifacts are useful; the single worker still executes the work. If the worker treats the item as direct leaf, the Director may accept that only after child-thread readback confirms the tiny/mechanical/low-risk rationale and evidence.

### 3. Multi-item but short-lived

Use orchestration without a durable `.workflow/` run when the task is multi-step but not large enough to need long-lived artifacts.

- invoke `$director-orchestrate` and follow the Director orchestrate workflow reference
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

When optional context/delegation tools are also available, use them as implementations under the same task artifact source of truth:

1. Director invokes `codex-dynamic-workflows` to create the task orchestration run.
2. Director uses the dynamic workflow plan and artifacts as the task source of truth.
3. For each dynamic workflow packet, Director dispatches a Codex worker thread.
4. The worker uses the relevant self-contained workflow playbook for its assigned work item.
5. For work-item complexity, the worker chooses a helper/context strategy and may use the orchestration workflow, nested dynamic workflow artifacts, or native sub-agents only under that work item.
6. Worker writes concise result evidence into `results/` only through the workflow's accepted-result path.
7. Director reads back each child worker thread, reconciles evidence and helper/direct-leaf policy, dispatches any integration, verification, or reconciliation work to workers, records accepted evidence, and writes final report.

## How Recursive Helpers Fit

Worker-internal helpers are implementation helpers. They are best when the current worker needs to decompose work, select likely models/functions/files/tests, map context slices, delegate a bounded subtask, verify items, review a narrow surface, or package context without bloating the owning worker thread.

`codex-dynamic-workflows` is task-level orchestration. It is best when the task needs success criteria, packetization, approval gates, worker-thread packet passes, integration, verification tracking, and a final audit trail.

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

Latest Codex `codex_app` worker/thread/project tooling is the premise of this skill. Director setup confirms the contract before operating, and dynamic workflow packet work must not execute in the Director thread.

## How Workflow Playbooks Fit

Use the narrow self-contained workflow that matches each assigned work item. When the work item is a concrete dynamic workflow packet, keep the packet artifact as the durable source of truth:

- Research packet -> `$director-investigate`
- Plan packet -> `$director-deep-plan`
- Build packet -> `$director-build`
- Review packet -> `$director-review`
- Refactor packet -> `$director-refactor`
- Optimize packet -> `$director-optimize`
- Browser/external oracle packet -> `$director-browser-oracle`; use optional local prompt artifacts only for oversized payloads, upload/chunking, retry, audit, or handoff needs; if Pro is unavailable or ambiguous, route to built-in main/`xhigh` oracle/review fallback unless Pro-only was explicit

The Director should predict likely skills in the worker brief, but the worker must re-run skill activation after reading local instructions. Oracle packets flow through the Director: `worker -> Director -> oracle lane -> Director -> worker/result`.

## How Codex Goals Fit

Use Codex Goals inside the director thread or worker threads only when the objective is durable, evidence-based, and likely to span turns or iterations.

- Director project ledger tracks portfolio work.
- Dynamic workflow artifacts track complex task orchestration.
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
- Every Director-created worker that reached a terminal signal has been read with `codex_app.read_thread`, and the terminal child report was captured from the child thread itself.
- Worker threads have reported evidence, and the Director has reconciled it against done criteria.
- Non-trivial workers used required helper/subagent lanes, or direct-leaf workers provided credible tiny/mechanical/low-risk rationale.
- Review gates have passed or residual risk is accepted.
- Authorized commits or PR evidence are complete, or `no-commit` evidence is ready for user/Director decision.
- Worktrees are reconciled into the canonical repo/branch.
- No worker remains `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, or missing helper/direct-leaf acceptance.
- No coordinator checkpoint remains at "recommended next briefs" without `next-packet-dispatched`, `monitor-scheduled`, `blocked-on-dispatch:<reason>`, or `awaiting-approval:<reason>`.
- Runtime handles are collected, archived, canceled, or cleaned up.
- Final user-facing status is concise and source-backed.
