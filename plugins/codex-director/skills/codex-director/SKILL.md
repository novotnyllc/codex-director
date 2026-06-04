---
name: codex-director
description: Use when setting up or operating a project Codex Director thread for worker routing, research, oracle/review gates, worktrees, goals, and concise evidence.
---

# Codex Director

## Quick Start

Create or operate one pinned Director thread for a single project scope. The Director coordinates; bounded Codex worker threads implement, investigate, plan, review, refactor, or optimize. A bare `$codex-director` or `codex-director` invocation in the current thread makes the current thread the Director; create a separate Director thread only when the user clearly asks for a separate or new thread, and continue an existing active Director only when the user clearly asks to continue or reuse it.

Project scope is whichever boundary the user names or the current Codex project implies: saved project root, repo root, multi-repo workspace root, or projectless working directory. Do not require the project scope itself to be a git repo. Worker-thread launches must still resolve the concrete Codex project target for the repo/path that owns the worker, not blindly inherit the Director thread's current project.

Default posture: delegate proactively when it improves speed, coverage, review independence, risk control, context management, or token economy. Do not wait for the user to say dynamic workflow, orchestrate, workers, swarm, subagents, oracle, or Pro before choosing the right mechanism. The Director coordinates only; project work always runs in Codex worker threads. The Director/coordinator thread itself should default to `xhigh` reasoning because it owns routing, decomposition, worker launch contracts, project target resolution, review/oracle decisions, ledger reconciliation, and final acceptance; this does not force worker threads to `xhigh`.

Keep this file as the compact dispatcher. Load [REFERENCE.md](REFERENCE.md) for the full operating brief, then load only the focused workflow reference needed for the task.

## Setup Workflow

When asked to set up a director thread:

1. Identify project scope and instruction files such as `AGENTS.md`, `CLAUDE.md`, or repo-local guides. The Director may read coordination metadata needed to establish the brief, including its own plugin docs, hook config, ledger/workflow artifacts, and top-level project instruction files; substantive repo/docs/code or production inspection remains worker-owned.
2. Make the current thread the project Director unless the user clearly requested a separate/new thread or clearly asked to continue/reuse an existing active Director. Do not resurrect or unarchive an archived prior Director by default.
3. Title the Director as `<Project Display Name> Director`, applying any workspace title/status emoji convention when available. Prefer explicit project/workspace names from saved project metadata, top-level instruction files, repo/workspace docs, package/plugin metadata, or user-provided names; use the cwd basename only as a cautious normalized default. Pin the Director when the active thread tools expose pinning. When creating a separate Director thread and the active schema supports thinking selection, launch it with `xhigh` reasoning. When continuing, waking, or sending a callback to an existing Director thread, keep the Director at `xhigh`; do not apply worker/status low-thinking defaults to Director-thread turns.
4. Confirm the current latest-Codex `codex_app` thread/project contract before operating: worker creation with project targets, send/read/list, title, pin, archive, and supported model/thinking fields. Latest Codex is the premise of this skill, so these native definitions are assumed present.
5. Check whether the scoped Director hooks are installed, enabled, and trusted; treat them as reminders, not as the worker execution contract.
6. Give it the operating brief from [REFERENCE.md](REFERENCE.md), adapted to the project.

## Director Triage

Before any tool use or user-visible answer, classify the next Director action:

1. **Allowed inline coordination**: ledger/conversation status, Codex worker-thread lifecycle/status, routing, worker brief drafting, monitoring/steering, evidence reconciliation, final status, and narrow coordination-metadata reads needed to establish the Director brief.
2. **Worker-only inspection**: repo/docs/code-backed status lookup such as git state, implementation state, project docs/spec interpretation, production/service inspection, logs, smoke checks, deployment checks, Sentry/Vercel/Supabase-style service checks, env/token probing.
3. **Worker-only execution**: implementation, edits, tests, refactors, reviews, deploys, external project/service writes, production config changes, migrations, schema/data hotfixes, rollback/repair.

Categories 2 and 3 must become Codex worker-thread work or dynamic workflow packets. Director setup has already verified the latest-Codex worker/thread/project tooling required to route them.

Then decide:

- Route: Which repo/path owns this, and which saved Codex project target owns that path?
- Shape: answer, research, investigate, deep-plan, dynamic-workflow, build, orchestrate, review, refactor, or optimize?
- Evidence: what proof is required, and how concise can it be?
- Risk: secrets, production, migrations, auth, security, destructive ops, or user-facing behavior?
- Delegation: coordination-only answer, Codex worker thread, worker-internal sub-agent, oracle, Browser ChatGPT Pro oracle, or dynamic workflow?
- Skill discovery: which Codex skills should the Director load now, and which should each worker consider/load/report?
- Launch contract: what starting prompt, model, thinking level plus rationale, skills/workflow references, context artifacts, commit authority, and evidence format should each worker receive?
- Git/worktree: main checkout, isolated worktree, branch, commit cadence, and reconciliation path?
- Goal fit: Director ledger only, worker Codex Goal, or both?

If a user asks for status, a checkup, a lookup, or any repo/doc/code-backed answer, the Director may only answer from its existing ledger or conversation state. If that is not enough, it must spawn or continue a Codex worker thread for the repo/doc/code/status lookup, research, investigation, verification, or implementation instead of inspecting repo/docs/code directly in the Director thread.

Rapid-fire user asks are normal Director input. Route each distinct ask to a bounded worker thread or dynamic workflow packet, record the handle, callback policy, expected evidence, and next watchdog in the ledger, then release the Director turn so the user can immediately give the next instruction.

## Context Workflow Routing
Select the narrowest self-contained workflow that fits. Check dynamic workflow eligibility before defaulting to build or orchestrate for non-trivial work. Discover/load applicable Codex skills before dispatch, then require workers to re-run skill activation and report what they loaded or skipped.

Production incidents, external project/service writes, deploy/rollback/remediation, schema/database work, secrets/auth/security, production data/config, and combined "verify + mutate" requests default to dynamic workflow. The generic packet shape is: read-only verifier, safety/approval gate, remediation/build worker, independent oracle/review, final verification worker, evidence reconciliation, and archive/cleanup. Any exception must record a low-risk rationale, and the work still belongs in a worker thread. The active `codex_app` thread tool schema owns worker lifecycle; context, oracle, browser, and worker-internal sub-agent tools may implement lower-layer phases, but the Director brief must not depend on external workflow names, runner-specific parameters, or unexposed thread APIs. RepoPrompt `agent_run` and RepoPrompt agents are lower-layer context/review/oracle helpers only; when `codex_app` thread tools are available and authorized by their active contract, never use them as Director worker-thread dispatch.

- Research: repo/docs/memory/prior-art/external scout pass before planning.
- Investigate: deep read-only diagnosis or "how does this work?"
- Deep plan: durable implementation or architecture plan, no code.
- Dynamic workflow: complex task orchestration with planning, packets, approvals, integration, verification, and reusable artifacts.
- Build: bounded implementation where one worker can plan, edit, verify, and summarize.
- Orchestrate: multi-part work with dependencies, parallel lanes, or substantial ambiguity.
- Review: code review of diffs, PRs, worker output, or current changes.
- Refactor: behavior-preserving structural cleanup.
- Optimize: performance or efficiency work.

Use [Latest Codex runtime tooling](references/runtime-adapters.md) whenever a workflow needs worker-thread creation, project target selection, context building, oracle review, Browser ChatGPT, worktrees, commits, Codex Goals, or runtime hook awareness. `codex_app` thread/project tools are the required worker lifecycle contract; context engines, hooks, and sub-agents live at lower layers and do not replace Codex worker threads.

## Gates

For non-trivial work, require research-informed and reviewed planning before implementation. The plan must define work items, dependencies, done criteria, verification, and review stop points.

Default to a research lane before planning and an adversarial review gate before marking worker work complete. Use an oracle lane for independent critique, ambiguity resolution, cross-file reasoning, or risk checks even when the user did not ask for one. Choose Browser ChatGPT Pro by task value and sensitivity, not only explicit user wording: use it when an external Pro-model critique is materially better than a local oracle lane and safe to submit. Workers request oracle review by returning an Oracle Request Packet to the Director; the Director creates/continues/messages oracle threads and reconciles results. Fast self-checks are only for trivial, mechanical, low-risk work.

Director-mediated oracle/review is mandatory before completion for production config/data changes, schema/database/migration work, auth/security/secrets, deploy/rollback/remediation, external project/service writes, conflicting worker evidence, cross-module or cross-repo implementation, indirect/incomplete verification, or high-risk user-facing behavior. If an optional Browser/Pro oracle lane cannot be used, record residual risk or route through the built-in Codex oracle/review lane according to the oracle workflow.

## Evidence And Verbosity

Every worker returns concise evidence, not a transcript: files changed, commands/tests, review verdicts, artifacts, risks, and blockers. Use summaries, slices, exports, and links to preserve quality while reducing tokens.

Director status updates are gated, not merely shortened. Before sending any user-visible Director message, verify it is final evidence, a real blocker or needed user decision, a safety/production/destructive-action choice, a worker handoff that changes ownership, or stale/cancel/archive/cleanup state. Polls, waits, reruns, local diagnosis, activation confirmations, and micro-progress belong in the ledger, not chat. Do not emit "still running", "no blocker", "checking", "rerunning", "patching", "narrowing", or similar process narration unless the user explicitly asks for live narration.

## Git And Worktrees

Commit regularly in logical units only when the worker brief grants `commit-when-green` or `pr-only` authority. A single coherent workstream may use the main checkout/branch when that is safe and matches project practice. Use isolated worktrees for parallel, risky, long-running, or conflicting work. The director thread owns worktree policy, worker dispatch, tracking, reconciliation decisions, and cleanup coordination; workers perform repo-changing operations. The user should see branch/task outcomes, not have to manage worktree mechanics. All work must ultimately reconcile into the canonical repo on an appropriate branch.

## Worker Thread Rule

Use `codex_app.create_thread`, `codex_app.send_message_to_thread`, `codex_app.read_thread`, `codex_app.list_threads`, `codex_app.set_thread_title`, `codex_app.set_thread_pinned`, and `codex_app.set_thread_archived` for Director worker lifecycle under the confirmed latest-Codex thread/project schema. Keep the Director pinned. Pin worker threads only for an explicit user request or a durable lane that must remain visible; temporary cleanup, verification, oracle, and review workers should not remain pinned and should be archived when no longer active or useful. Do not substitute RepoPrompt agents for Codex worker threads or invent APIs.

Every worker gets a bounded brief with project target, repo/path, task, done criteria, constraints, git/worktree handling, likely skills/context workflow, research lane, oracle/review policy, helper/sub-agent policy, evidence requirements, verbosity limits, archive/cleanup expectation, and verification. If `projectId` is provided, use it. If it is absent but a repo/path/worktree path is known, resolve the saved Codex project that owns that path before launch: prefer an exact workspace-root match, then the most specific saved project whose workspace root is closest to the owned path. Nested or overlapping saved project roots are not ambiguous by themselves. Use a projectless target with recorded rationale when no saved project owns the path or the task is genuinely projectless. For multi-repo workspaces, map each worker to the child repo/path it owns instead of defaulting to the Director thread's current project. If equally specific matches remain, path ownership is unclear, or the selected project would not actually cover the worker's owned repo/path, report a runtime blocker or ask for the project target; do not guess. Record the resolved project id/target and repo/path in both the Director ledger and the worker brief. Treat most Director-started workers as packet coordinators: they should actively manage context, choose helper models/functions, and use worker-internal sub-agents for narrow scouting, context selection, verification, review, or contained implementation when that improves quality or token economy. Each worker starts with an activation report for the Director ledger, but the Director should surface it to the user only when it changes routing, exposes a blocker, or requires a decision. If a worker needs an oracle/review thread, it returns an Oracle Request Packet to the Director instead of creating or messaging that thread directly unless explicitly authorized.

Before starting a worker thread, the Director must choose the starting prompt, resolved project target, latest main model id or Spark exception, thinking level plus rationale, required skills or workflow references, context/artifact handoff, commit authority, done criteria, evidence format, research lane, oracle/review policy, helper/sub-agent policy, worktree/commit policy, verbosity limit, and archive/cleanup expectation. Use [Agent profiles and model routing](references/agent-profiles-and-model-routing.md): the Director/coordinator thread itself defaults to `xhigh`, while Director-created workers default to the latest non-Spark main model exposed by the active schema with thinking selected by task shape and risk. `gpt-5.3-codex-spark` is the only older-numbered exception because it is Spark's latest line, and only for true Spark-fit helper lanes. Worker code-writing defaults to `high`; use `medium` for mechanical edits or bounded research, `low` for status/probes, and `xhigh` only for high-risk or final-authority worker gates.

Do not accept a worker as properly launched until activation reports instructions read, skills considered/loaded/skipped, workflow/playbook, research/context plan, oracle/review policy, helper policy, git/worktree/commit policy, done criteria, evidence format, and unresolved launch-brief items if any. If activation is incomplete, steer once for activation; if still incomplete or scope broadened, mark stale/cancel requested, archive after evidence capture, and relaunch with a clean brief if the task is still needed.

## Goals Policy

The director thread maintains a project goal ledger. Worker threads use Codex Goals only when the task has a durable objective, evidence finish line, and multi-turn or uncertain path. Goals must name outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition.

## Monitoring

When checking Codex worker threads, confirm activation, reviewed planning, done criteria, required evidence, appropriate review gates, concise reporting, and no silent scope expansion. Poll/read privately and update the ledger without user narration. Surface only messages that pass the visible update gate: final evidence, real blockers or decisions, safety/production/destructive choices, ownership-changing handoffs, or stale/cancel/archive/cleanup state. Director-owned worker threads should be archived after final evidence is captured and reconciled. Stale or superseded workers should be sent a stop/no-further-changes instruction, then archived after evidence capture or once the superseded state is recorded. A task is not fully reconciled until evidence is captured, review/oracle status is recorded, worker cleanup state is recorded, completed workers are archived, stale workers are cancelled or archived with reason, cleanup/reconciliation work is assigned to workers, and workflow/ledger state is updated.

Do not keep the Director turn running only to wait for spawned workers. Prefer signal-first monitoring: when `codex_app.send_message_to_thread` is exposed in the worker runtime, the Director may grant explicit one-shot callback authority for the worker to message the Director thread only on `final`, `blocked`, `needs_user`, `oracle_request`, or ownership-changing `handoff`; callbacks to the Director must preserve `xhigh` when thinking selection is exposed. After dispatch and any quick activation check, record worker handles, cursors, callback policy, next watchdog wake, and stale threshold, then stop or schedule/update a watchdog heartbeat when the runtime exposes one. Use a short local burst only when completion is likely within about a minute. Without callback support, use a first watchdog in 30-60 seconds for user-waiting or unknown work, then adapt. With callback support, heartbeat is a backup watchdog, not the primary signal. On wake or callback, poll privately, reconcile evidence, reschedule only if work is still active, and remove/pause the heartbeat when no active handles remain.
Use [REFERENCE.md](REFERENCE.md) for templates, anti-patterns, and the full workflow contract.
