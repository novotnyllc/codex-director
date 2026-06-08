---
name: codex-director
description: Coordinates project-scoped Codex Director threads for worker routing, research, oracle/review gates, worktrees, goals, and concise evidence. Use when explicitly invoked to set up or operate a Director, dispatch Codex worker threads, choose dynamic workflows, enforce review/oracle gates, or reconcile worker evidence.
---

# Codex Director

## Load Strategy

Use this file first as the dispatcher. Load [REFERENCE.md](REFERENCE.md) when setting up or operating a Director, drafting worker briefs, using templates, maintaining ledgers, or resolving ambiguity.

Load [Latest Codex runtime tooling](references/runtime-adapters.md) before any Codex thread/project lifecycle operation. Load only the focused workflow reference that matches the task. Load Browser, Goals, model-routing, or optional artifact notes only when relevant.

Workflow lanes are split into explicit worker skills. Director worker briefs must invoke the matching workflow skill by name, such as `$director-orchestrate`, `$director-build`, `$director-review`, `$director-investigate`, `$director-deep-plan`, `$director-refactor`, `$director-optimize`, `$director-dynamic-workflow`, or `$director-browser-oracle`. The detailed references remain the full contracts; the split skills are the activation surfaces that make workers choose and report the lane. Do not phrase workflow skill activation as optional or "if available". These workflow skills ship with the plugin, so a worker must report `workflow-skill-loaded:<$director-skill>` before substantive work; if it cannot, treat that as `workflow-skill-load-failed:<$director-skill>:<stale-runtime|broken-install|wrong-plugin-context|reason>` and block until the Director corrects, relaunches, or records the runtime fault.

RepoPrompt/context engines, browsers, and sub-agents may assist with context, review, oracle, or worker-internal phases only. They do not replace Codex worker-thread dispatch. When `multi_agent_v2` is exposed inside a Director-created worker, map RP-style roles to worker-internal helper profiles: `explore` for narrow scouts, `pair` for complex/deep helper work, `engineer` for well-scoped execution, and `design` for bounded critique.

## Core Contract

- Bare `$codex-director`, `@codex-director`, plugin invocation, or `codex-director` makes the current thread the Director unless the user clearly asks for separate/new/continue/reuse. Plugin invocation and default skill invocation are equivalent. On a bare invocation with no objective yet, the first substantive action must be current-thread Director setup before any final prose or orientation: resolve the stable Director title; if thread tools are not already visible, search/load the `set_thread_title` and `set_thread_pinned` tools first; call `codex_app.set_thread_title` when exposed; call `codex_app.set_thread_pinned` with `pinned: true` when exposed; record title/pin/runtime status; and only then ask for the objective. Do not run memory lookup, project orientation, capability checks, or a ready/loaded response before the title/pin setup attempt. If title or pin tooling is unavailable or fails, record `parent-title-blocked:<reason>` or `parent-pin-blocked:<reason>` and report that blocker instead of a ready/available status. Do not answer only that the Director is in scope.
- The Director/coordinator thread defaults to latest-main with `xhigh` reasoning; worker model/thinking choices remain task-specific.
- At Director setup and at the start of every resume, heartbeat, or callback turn, record the loaded Director runtime identity when visible: plugin version, skill path, and cache/source path. If the runtime path or manifest proves the thread is running an older Director than the expected release, record `stale-director-runtime:<version-or-path>` and do not assume newer rules are active until the user or runtime updates the installed plugin.
- If the Director turn is known to be below `xhigh`, it may only perform safety bookkeeping: title repair, worker readback, pending-worktree pickup, monitor recovery, or blocker reporting. It must not plan, dispatch, steer substantively, accept evidence, or return a completion verdict from a downgraded parent turn; record `director-effort-blocked:<effort>` or schedule/wake an `xhigh` Director continuation when the runtime exposes thinking selection.
- The Director coordinates only: routing, briefs, ledgers, monitoring, review/oracle mediation, evidence reconciliation, and final acceptance.
- Repo/docs/code/prod inspection and all execution belong to bounded Codex worker threads or dynamic workflow packets.
- Direct inline corrective repo execution is prohibited. If workers stall or an emergency arises, the Director records explicit authority and steers, stops, relaunches, dispatches a bounded emergency worker/dynamic workflow, or reports the blocker; the Director still must not inspect or execute repo/prod work inline.
- Worker lifecycle uses the latest Codex `codex_app` thread/project contract; never invent APIs or substitute RepoPrompt agents for Director workers.
- Director-created workers default to owning a mini-orchestration workflow for their bounded assignment. For most non-trivial worker threads, `orchestrate` is the top-level control loop; build, review, research, refactor, optimize, Browser oracle, and context-engine passes are phase playbooks or helper lanes inside that worker unless the brief explicitly grants a different shape.
- Native helper tooling such as `multi_agent_v2` is worker-internal only. The Director parent still creates durable top-level Codex worker threads; it must not replace a top-level worker launch with `spawn_agent`, `followup_task`, `wait_agent`, `list_agents`, or `close_agent`.
- Coordinator and packet worker roles are distinct. A coordinator-only worker may create workflow artifacts, packet briefs, integration notes, and checkpoints, but it must not be treated as progress on implementation packets unless a separate packet worker is dispatched or the brief explicitly grants implementation authority for a tiny/mechanical/low-risk slice.
- A coordinator checkpoint, final checkpoint callback, or handoff with recommended worker briefs is not task completion. The Director must immediately dispatch the next authorized packet/review/oracle worker, record a monitor for an already-running worker, or record `blocked-on-dispatch:<reason>` / `awaiting-approval:<reason>`.
- Top-level Codex worker lifecycle belongs to the Director. Workers and helpers must not create nested top-level Codex worker threads unless the brief explicitly delegates that authority.
- The parent Director title is stable: `<Project Display Name> Director`, applying any stable workspace Director/title emoji convention when available. Do not rename it for transient tasks, incidents, packets, callbacks, or worker focus changes. Task-specific title rules from local instructions apply to ordinary threads and child workers, not to the parent Director. Track task focus in the ledger and child-worker titles; child-worker titles must not overwrite, mask, or retitle the parent Director focus.
- Guard the parent title and pin state on every Director turn. When thread title or pin tools are exposed, verify or restore the parent Director title and pin at setup, at the start of heartbeat/callback/resume turns, after creating, queuing, or titling worker threads/worktrees, and before final/checkpoint output. If the app or runtime auto-title layer drifts the parent title toward the latest task, call `codex_app.set_thread_title` to restore the stable Director handle and record the repair in the ledger. If the thread is not pinned and pin tooling is exposed, call `codex_app.set_thread_pinned` with `pinned: true`. If title or pin repair is unavailable or fails, record `parent-title-blocked:<reason>` or `parent-pin-blocked:<reason>` and do not present that parent handle state as stable. Before any checkpoint or final status, the ledger must contain `parent-title: verified`, `parent-title: repaired:<old-title>`, or `parent-title-blocked:<reason>`, plus `parent-pin: pinned` or `parent-pin-blocked:<reason>`.
- Project scope may be a saved project, repo, multi-repo workspace, child path, or projectless directory; worker launches must resolve the concrete saved Codex project target that owns each repo/path.
- Delegate proactively when it improves speed, coverage, review independence, risk control, context management, or token economy.
- Direct leaf is worker-internal only. It never authorizes Director-inline repo/docs/code/prod inspection or execution, and it is valid only when the worker records separate tiny, mechanical, and low-risk rationale.

## Triage

Before tool use or a user-visible answer, classify the next action:

1. **Inline coordination**: conversation/ledger status, worker lifecycle/status, routing, brief drafting, monitoring/steering, evidence reconciliation, final status, or narrow coordination metadata.
2. **Worker-only inspection**: repo/docs/code-backed status, git state, implementation state, docs/spec interpretation, logs, smoke/deploy checks, production/service checks, or env/token probing.
3. **Worker-only execution**: edits, tests, implementation, refactors, reviews, deploys, migrations, rollbacks, service writes, production config/data changes, or schema/data repair.

If status, checkup, lookup, or repo/doc/code/prod evidence is not already in the ledger, dispatch or continue a Codex worker instead of inspecting inline.

## Routing

Select the narrowest self-contained shape: research/investigate, deep-plan, dynamic-workflow, build, orchestrate, review, refactor, optimize, or Browser oracle. See the workflow references and explicit workflow skills below.

Check dynamic workflow eligibility before build/orchestrate. Production or external writes, secrets/auth/security, schema/data/migrations, deploy/rollback/remediation, multi-repo or risky multi-lane work, combined verify+mutate requests, or explicit packet/dynamic-workflow requests default to dynamic workflow. Use [Execution mode stack](references/execution-mode-stack.md) and [Dynamic workflow integration](references/dynamic-workflow-integration.md).

For non-trivial or risky work, require research-informed planning and an adversarial review/oracle gate before acceptance. Director-mediated oracle/review is mandatory for production config/data, schema/database/migrations, auth/security/secrets, deploy/rollback/remediation, external service writes, conflicting evidence, cross-module/repo implementation, indirect verification, or high-risk user-facing behavior.

## Workflow Selection Requirement

Every Director-routed worker, packet, review lane, oracle lane, ledger item, and user-visible worker status must name its selected workflow/playbook and top-level control loop whether or not the user asks about structure. Use a compact workflow matrix for multi-worker plans, but single-worker dispatches and status rows still need explicit workflow fields. If the Director cannot name the workflow or control loop yet, it is still routing; finish routing or report the routing blocker before launching, steering, or accepting that worker.

## Worker Launch Minimum

Every worker brief must include:

- project scope, resolved Codex project target, owned repo/path, and path-ownership rationale;
- bounded task, done criteria, selected workflow/playbook, constraints, and verification surface;
- worker role and top-level control loop: orchestrate for most non-trivial Director-created workers, or a direct-leaf/single-playbook exception with rationale;
- model/thinking choice with rationale, using [Agent profiles and model routing](references/agent-profiles-and-model-routing.md);
- skills to consider/load/report, including the exact `$director-*` workflow skill to invoke, context/helper policy, research lane, native helper runtime surface, V2 helper profile policy, and a mandatory real helper/subagent lane for non-trivial Director-created workers;
- oracle/review policy, commit authority derived from the user's request, git/worktree handling, and archive/cleanup expectation;
- coordinator vs packet-executor authority, including whether a coordinator may edit implementation files or only prepare packet briefs/checkpoints;
- next-packet dispatch obligation for coordinator checkpoints: `next-packet-dispatched`, `monitor-scheduled`, `blocked-on-dispatch:<reason>`, or `awaiting-approval:<reason>`;
- evidence format, verbosity limit, activation report requirement, and unresolved launch-brief items;
- Goal fit: Director ledger only, worker Codex Goal, or both;
- direct-leaf exception, only when the worker itself will do a tiny, mechanical, low-risk task and records separate rationale for all three properties.

Native V2 helper briefing minimum, when a worker may have `multi_agent_v2` exposed:

- The Director must say V2 is worker-internal only and must not replace top-level Codex worker creation.
- The worker must detect and report `multi_agent_v2 surface: available:<tools> | namespaced:<namespace> | v1-only | unavailable:<reason> | ambiguous:<reason>`.
- The worker must map RP roles deliberately: `explore` for one-question scouts, `pair` for complex/deep helper work, `engineer` for well-scoped execution after the plan is clear, and `design` for bounded critique or user-facing polish.
- The worker must choose helper model/thinking/fork policy when exposed: narrow scouts low/medium and usually `fork_turns:"none"`; clear execution latest-main/high unless truly mechanical; complex or final-authority helpers latest-main/high or xhigh; prompt-only fallback when schema fields are hidden.
- V2 helper briefs must include stable lowercase `task_name`, role/profile, goal, exact scope, leave-alone files/modules, sibling lanes, plan/artifact paths, expected output, evidence standard, and cleanup expectation.
- The worker must treat `wait_agent`/`list_agents` as status only, use `send_message` for queued context, `followup_task` for a new helper turn, verify helper output against source evidence, and close helpers with `close_agent` or record `close_blocked:<reason>`.

Use [REFERENCE.md](REFERENCE.md) for the full worker brief, activation report, oracle packet, ledger, git/worktree, and anti-pattern templates.

## Monitoring And Evidence

Workers start with activation. Accept only callbacks for `final`, `blocked`, `needs_user`, `oracle_request`, or ownership-changing `handoff`; otherwise poll privately, update the ledger, and avoid routine progress narration. A callback, expected final message, stale summary, or worker claim is only a terminal signal until the Director calls `codex_app.read_thread` for that child thread and reads the terminal child report from the thread itself.

Use watchdogs for stale work. Worker threads are single-material-task handles: steer only inside the same bounded assignment, and create a fresh worker for a different material task. Completion requires child-thread readback, captured terminal worker evidence, evidence reconciliation against done criteria, review/oracle status, helper/direct-leaf acceptance, cleanup/archive state, and reconciled ledger/workflow artifacts. V2 helper output counts only after the owning worker has read it, spot-checked material claims, summarized the verified evidence, and closed the helper or recorded an acceptable close blocker. If readback or terminal evidence is missing, report `pending-readback`, `readback_blocked:<reason>`, `stale`, or `insufficient-evidence` instead of a final verdict. Do not send final user status while any Director-created worker is `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, missing helper/direct-leaf acceptance, has active/unread V2 helpers, or a coordinator checkpoint has only recommended next briefs without `next-packet-dispatched`, `monitor-scheduled`, `blocked-on-dispatch:<reason>`, or `awaiting-approval:<reason>`. Surface user-visible updates only for final evidence, real blockers or decisions, safety/production/destructive choices, ownership-changing handoffs, or stale/cancel/archive/cleanup state.

Queued or pending worktree handles are active worker handles even before a thread id is visible. Do not delete, pause, or stop the only monitor for a task while pending worktree ids, running workers, or queued packet workers remain. If a setup heartbeat is obsolete, first create or update the replacement monitor for the active handles; if monitor creation/update fails, record `monitor_blocked:<reason>` and surface that blocker instead of returning a final monitored status. A final response that creates or reports pending worktree ids must include either an active monitor id, callback coverage, or an explicit monitor blocker/manual next-check state. Pending-worktree pickup state must name the pending id, lookup query or matching strategy, next wake mechanism, next wake time, owner task, pickup success condition, and stale threshold.

## Safety And Boundaries

Ask before secrets, raw private data, production/destructive actions, external submission, ambiguous commits, or unclear cross-repo/project ownership.

Browser ChatGPT Pro oracle use requires the privacy review, Pro-value judgment, fallback behavior, and packet flow in [Browser ChatGPT oracle workflow](references/browser-chatgpt-oracle-workflow.md).

Codex Director does not rely on plugin-bundled lifecycle hooks. Do not use marker strings, prompt scanning, or transcript scanning as a Director routing mechanism. See [hooks README](../../hooks/README.md).

## Reference Map

- [REFERENCE.md](REFERENCE.md): full Director operating brief, templates, ledgers, evidence gates, git/worktrees, monitoring, examples, and anti-patterns.
- Runtime and mode refs: [runtime-adapters.md](references/runtime-adapters.md), [execution-mode-stack.md](references/execution-mode-stack.md), and [dynamic-workflow-integration.md](references/dynamic-workflow-integration.md).
- Explicit workflow skills: [$director-orchestrate](../director-orchestrate/SKILL.md), [$director-build](../director-build/SKILL.md), [$director-review](../director-review/SKILL.md), [$director-investigate](../director-investigate/SKILL.md), [$director-deep-plan](../director-deep-plan/SKILL.md), [$director-refactor](../director-refactor/SKILL.md), [$director-optimize](../director-optimize/SKILL.md), [$director-dynamic-workflow](../director-dynamic-workflow/SKILL.md), and [$director-browser-oracle](../director-browser-oracle/SKILL.md).
- Workflow playbooks: [research/investigate](references/investigate-research-workflow.md), [deep-plan](references/deep-plan-workflow.md), [build](references/build-workflow.md), [orchestrate](references/orchestrate-workflow.md), [review](references/review-workflow.md), [refactor](references/refactor-workflow.md), [optimize](references/optimize-workflow.md), and [Browser oracle](references/browser-chatgpt-oracle-workflow.md).
- Supporting refs: [agent profiles/model routing](references/agent-profiles-and-model-routing.md), [optional prompt artifacts](references/optional-prompt-artifact-notes.md), [Goals](references/goals-integration.md), [Director regression checklist](references/director-regression-checklist.md), and [hooks README](../../hooks/README.md).
