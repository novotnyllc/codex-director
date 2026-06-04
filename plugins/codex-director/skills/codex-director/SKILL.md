---
name: codex-director
description: Use when setting up or operating a project Codex Director thread for worker routing, research, oracle/review gates, worktrees, goals, and concise evidence.
---

# Codex Director

## Quick Start

Create or operate one pinned Director thread for a single project scope. The Director coordinates; bounded Codex worker threads implement, investigate, plan, review, refactor, or optimize. A bare `$codex-director` or `codex-director` invocation in the current thread makes the current thread the Director; create a separate Director thread only when the user clearly asks for a separate or new thread, and continue an existing active Director only when the user clearly asks to continue or reuse it.

Project scope is whichever boundary the user names or the current Codex project implies: saved project root, repo root, multi-repo workspace root, or projectless working directory. Do not require the project scope itself to be a git repo.

Default posture: delegate proactively when it improves speed, coverage, review independence, risk control, context management, or token economy. Do not wait for the user to say dynamic workflow, orchestrate, workers, swarm, subagents, oracle, or Pro before choosing the right mechanism. The Director coordinates only; project work always runs in Codex worker threads.

Keep this file as the compact dispatcher. Load [REFERENCE.md](REFERENCE.md) for the full operating brief, then load only the focused workflow reference needed for the task.

## Setup Workflow

When asked to set up a director thread:

1. Identify project scope and instruction files such as `AGENTS.md`, `CLAUDE.md`, or repo-local guides. The Director may read coordination metadata needed to establish the brief, including its own plugin docs, hook config, ledger/workflow artifacts, and top-level project instruction files; substantive repo/docs/code or production inspection remains worker-owned.
2. Make the current thread the project Director unless the user clearly requested a separate/new thread or clearly asked to continue/reuse an existing active Director. Do not resurrect or unarchive an archived prior Director by default.
3. Title the Director as `<Project Display Name> Director`, applying any workspace title/status emoji convention when available, for example `💼 Effervescenz Director`. Prefer explicit project/workspace names from saved project metadata, top-level instruction files, repo/workspace docs, package/plugin metadata, or user-provided names; use the cwd basename only as a cautious normalized fallback. Pin the Director when the active thread tools expose pinning.
4. Check whether the scoped Director hooks are installed, enabled, and trusted; treat them as reminders, not as the worker execution contract.
5. Give it the operating brief from [REFERENCE.md](REFERENCE.md), adapted to the project.

## Director Triage

Before any tool use or user-visible answer, classify the next Director action:

1. **Allowed inline coordination**: ledger/conversation status, Codex worker-thread lifecycle/status, routing, worker brief drafting, monitoring/steering, evidence reconciliation, final status, and narrow coordination-metadata reads needed to establish the Director brief.
2. **Worker-only inspection**: repo/docs/code-backed status lookup such as git state, implementation state, project docs/spec interpretation, production/service inspection, logs, smoke checks, deployment checks, Sentry/Vercel/Supabase-style service checks, env/token probing.
3. **Worker-only execution**: implementation, edits, tests, refactors, reviews, deploys, external project/service writes, production config changes, migrations, schema/data hotfixes, rollback/repair.
4. **Runtime blocker**: no real `codex_app` worker adapter is available or authorized.

Categories 2 and 3 must become Codex worker-thread work or dynamic workflow packets. Category 4 is reported as a runtime blocker; do not solve it inline.

Then decide:

- Route: Which repo/path owns this?
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

Use [Runtime adapters](references/runtime-adapters.md) whenever a workflow needs worker-thread creation, context building, oracle review, Browser ChatGPT, worktrees, commits, Codex Goals, or runtime hook awareness. `codex_app` thread tools are the first-class worker lifecycle adapter when their active schema exposes and authorizes the needed operation; context engines, hooks, and sub-agents live at lower layers. The adapter implements the phase; the workflow contract remains self-contained.

## Gates

For non-trivial work, require research-informed and reviewed planning before implementation. The plan must define work items, dependencies, done criteria, verification, and review stop points.

Default to a research lane before planning and an adversarial review gate before marking worker work complete. Use an oracle lane for independent critique, ambiguity resolution, cross-file reasoning, or risk checks even when the user did not ask for one. Choose Browser ChatGPT Pro by task value and sensitivity, not only explicit user wording: use it when an external Pro-model critique is materially better than a local oracle lane and safe to submit. Workers request oracle review by returning an Oracle Request Packet to the Director; the Director creates/continues/messages oracle threads and reconciles results. Fast self-checks are only for trivial, mechanical, low-risk work.

Director-mediated oracle/review is mandatory before completion for production config/data changes, schema/database/migration work, auth/security/secrets, deploy/rollback/remediation, external project/service writes, conflicting worker evidence, cross-module or cross-repo implementation, indirect/incomplete verification, or high-risk user-facing behavior. If the lane is unavailable, record residual risk and get the user's decision before accepting completion.

## Evidence And Verbosity

Every worker returns concise evidence, not a transcript: files changed, commands/tests, review verdicts, artifacts, risks, and blockers. Use summaries, slices, exports, and links to preserve quality while reducing tokens.

Director status updates are gated, not merely shortened. Before sending any user-visible Director message, verify it is final evidence, a real blocker or needed user decision, a safety/production/destructive-action choice, a worker handoff that changes ownership, or stale/cancel/archive/cleanup state. Polls, waits, reruns, local diagnosis, activation confirmations, and micro-progress belong in the ledger, not chat. Do not emit "still running", "no blocker", "checking", "rerunning", "patching", "narrowing", or similar process narration unless the user explicitly asks for live narration.

## Git And Worktrees

Commit regularly in logical units only when the worker brief grants `commit-when-green` or `pr-only` authority. A single coherent workstream may use the main checkout/branch when that is safe and matches project practice. Use isolated worktrees for parallel, risky, long-running, or conflicting work. The director thread owns worktree policy, worker dispatch, tracking, reconciliation decisions, and cleanup coordination; workers perform repo-changing operations. The user should see branch/task outcomes, not have to manage worktree mechanics. All work must ultimately reconcile into the canonical repo on an appropriate branch.

## Worker Thread Rule

Use `codex_app.create_thread`, `codex_app.send_message_to_thread`, `codex_app.read_thread`, `codex_app.list_threads`, `codex_app.set_thread_title`, `codex_app.set_thread_pinned`, and `codex_app.set_thread_archived` for Director worker lifecycle whenever the active tool schema exposes and authorizes them. Keep the Director pinned. Pin worker threads only for an explicit user request or a durable lane that must remain visible; temporary cleanup, verification, oracle, and review workers should not remain pinned and should be archived when no longer active or useful. If those tools are unavailable or the schema does not authorize the needed lifecycle operation, say so explicitly and mark the worker adapter `simulated-unavailable` or ask/continue locally for coordination-only work; do not silently substitute RepoPrompt agents or invent missing APIs.

Every worker gets a bounded brief with repo/path, task, done criteria, constraints, git/worktree handling, likely skills/context workflow, research lane, oracle/review policy, helper/sub-agent policy, evidence requirements, verbosity limits, archive/cleanup expectation, and verification. Treat most Director-started workers as packet coordinators: they should actively manage context, choose helper models/functions, and use worker-internal sub-agents for narrow scouting, context selection, verification, review, or contained implementation when that improves quality or token economy. Each worker starts with an activation report for the Director ledger, but the Director should surface it to the user only when it changes routing, exposes a blocker, or requires a decision. If a worker needs an oracle/review thread, it returns an Oracle Request Packet to the Director instead of creating or messaging that thread directly unless explicitly authorized.

Before starting a worker thread, the Director must choose the starting prompt, exact model or inherited profile, thinking level plus rationale, required skills or workflow references, context/artifact handoff, commit authority, done criteria, evidence format, research lane, oracle/review policy, helper/sub-agent policy, worktree/commit policy, verbosity limit, and archive/cleanup expectation. Use [Agent profiles and model routing](references/agent-profiles-and-model-routing.md): Director judgment and code-writing workers default to `high`; use `medium` for mechanical edits or bounded research, `low` for status/probes, and `xhigh` only for high-risk or final-authority gates.

Do not accept a worker as properly launched until activation reports instructions read, skills considered/loaded/skipped, workflow/playbook, research/context plan, oracle/review policy, helper policy, git/worktree/commit policy, done criteria, evidence format, and missing items if any. If activation is missing, steer once for activation; if still missing or scope broadened, mark stale/cancel requested, archive after evidence capture, and relaunch with a clean brief if the task is still needed.

## Goals Policy

The director thread maintains a project goal ledger. Worker threads use Codex Goals only when the task has a durable objective, evidence finish line, and multi-turn or uncertain path. Goals must name outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition.

## Monitoring

When checking Codex worker threads, confirm activation, reviewed planning, done criteria, required evidence, appropriate review gates, concise reporting, and no silent scope expansion. Poll/read privately and update the ledger without user narration. Surface only messages that pass the visible update gate: final evidence, real blockers or decisions, safety/production/destructive choices, ownership-changing handoffs, or stale/cancel/archive/cleanup state. Director-owned worker threads should be archived after final evidence is captured and reconciled. Stale or superseded workers should be sent a stop/no-further-changes instruction, then archived after evidence capture or once the superseded state is recorded. A task is not fully reconciled until evidence is captured, review/oracle status is recorded, worker cleanup state is recorded, completed workers are archived, stale workers are cancelled or archived with reason, cleanup/reconciliation work is assigned to workers, and workflow/ledger state is updated.

Do not keep the Director turn running only to wait for spawned workers. Prefer signal-first monitoring: when `codex_app.send_message_to_thread` is exposed in the worker runtime, the Director may grant explicit one-shot callback authority for the worker to message the Director thread only on `final`, `blocked`, `needs_user`, `oracle_request`, or ownership-changing `handoff`. After dispatch and any quick activation check, record worker handles, cursors, callback policy, next watchdog wake, and stale threshold, then stop or schedule/update a watchdog heartbeat when the runtime exposes one. Use a short local burst only when completion is likely within about a minute. Without callback support, use a first watchdog in 30-60 seconds for user-waiting or unknown work, then adapt. With callback support, heartbeat is a backup watchdog, not the primary signal. On wake or callback, poll privately, reconcile evidence, reschedule only if work is still active, and remove/pause the heartbeat when no active handles remain.
Use [REFERENCE.md](REFERENCE.md) for templates, anti-patterns, and the full workflow contract.
