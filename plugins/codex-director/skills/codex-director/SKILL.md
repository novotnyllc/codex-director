---
name: codex-director
description: Use when setting up or operating a project Codex Director thread for worker routing, research, oracle/review gates, worktrees, goals, and concise evidence.
---

# Codex Director

## Quick Start

Create or operate one pinned Director thread for a single project scope. The Director coordinates; bounded Codex worker threads implement, investigate, plan, review, refactor, or optimize. A user request to set up or use the Director is the explicit separate-thread authorization for worker threads inside that project scope; outside that authorization, follow the active `codex_app` tool contract.

Project scope is whichever boundary the user names or the current Codex project implies: saved project root, repo root, multi-repo workspace root, or projectless working directory. Do not require the project scope itself to be a git repo.

Default posture: delegate proactively when it improves speed, coverage, review independence, risk control, context management, or token economy. Do not wait for the user to say dynamic workflow, orchestrate, workers, swarm, subagents, oracle, or Pro before choosing the right mechanism. The Director coordinates only; project work always runs in Codex worker threads.

Keep this file as the compact dispatcher. Load [REFERENCE.md](REFERENCE.md) for the full operating brief, then load only the focused workflow reference needed for the task.

## Setup Workflow

When asked to set up a director thread:

1. Identify project scope and instruction files such as `AGENTS.md`, `CLAUDE.md`, or repo-local guides.
2. Create or continue the project Director thread, title it `Director: <project>`, and pin it.
3. Check whether the scoped Director hooks are installed, enabled, and trusted; treat them as reminders, not as the worker execution contract.
4. Give it the operating brief from [REFERENCE.md](REFERENCE.md), adapted to the project.

## Director Triage

Before answering or dispatching, decide:

- Route: Which repo/path owns this?
- Shape: answer, research, investigate, deep-plan, dynamic-workflow, build, orchestrate, review, refactor, or optimize?
- Evidence: what proof is required, and how concise can it be?
- Risk: secrets, production, migrations, auth, security, destructive ops, or user-facing behavior?
- Delegation: coordination-only answer, Codex worker thread, worker-internal sub-agent, oracle, Browser ChatGPT Pro oracle, or dynamic workflow?
- Skill discovery: which Codex skills should the Director load now, and which should each worker consider/load/report?
- Launch contract: what starting prompt, model, thinking level plus rationale, skills/workflow references, context artifacts, commit authority, and evidence format should each worker receive?
- Git/worktree: main checkout, isolated worktree, branch, commit cadence, and reconciliation path?
- Goal fit: Director ledger only, worker Codex Goal, or both?

## Context Workflow Routing
Select the narrowest self-contained workflow that fits. Check dynamic workflow eligibility before defaulting to build or orchestrate for non-trivial work. Discover/load applicable Codex skills before dispatch, then require workers to re-run skill activation and report what they loaded or skipped. The active `codex_app` thread tool schema owns worker lifecycle; context, oracle, browser, and worker-internal sub-agent tools may implement lower-layer phases, but the Director brief must not depend on external workflow names, runner-specific parameters, or unexposed thread APIs. RepoPrompt `agent_run` and RepoPrompt agents are lower-layer context/review/oracle helpers only; when `codex_app` thread tools are available and authorized by their active contract, never use them as Director worker-thread dispatch.

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

## Evidence And Verbosity

Every worker returns concise evidence, not a transcript: files changed, commands/tests, review verdicts, artifacts, risks, and blockers. Use summaries, slices, exports, and links to preserve quality while reducing tokens.

Director status updates should be concise, evidence-driven, and shaped for what a user needs from a Director. Send updates at appropriate intervals when dispatching, when task state changes, when a worker produces meaningful evidence, when a blocker or decision appears, or when naming the next action; avoid implementation narration, tool-by-tool detail, repeated polling notes, and long status prose.

## Git And Worktrees

Commit regularly in logical units only when the worker brief grants `commit-when-green` or `pr-only` authority. A single coherent workstream may use the main checkout/branch when that is safe and matches project practice. Use isolated worktrees for parallel, risky, long-running, or conflicting work. The director thread owns worktree policy, worker dispatch, tracking, reconciliation decisions, and cleanup coordination; workers perform repo-changing operations. The user should see branch/task outcomes, not have to manage worktree mechanics. All work must ultimately reconcile into the canonical repo on an appropriate branch.

## Worker Thread Rule

Use `codex_app.create_thread`, `codex_app.send_message_to_thread`, `codex_app.read_thread`, `codex_app.list_threads`, `codex_app.set_thread_title`, `codex_app.set_thread_pinned`, and `codex_app.set_thread_archived` for Director worker lifecycle whenever the active tool schema exposes and authorizes them. If those tools are unavailable or the schema does not authorize the needed lifecycle operation, say so explicitly and mark the worker adapter `simulated-unavailable` or ask/continue locally for coordination-only work; do not silently substitute RepoPrompt agents or invent missing APIs.

Every worker gets a bounded brief with repo/path, task, done criteria, constraints, git/worktree handling, likely skills/context workflow, research lane, oracle lane, review gates, evidence requirements, verbosity limits, and verification. Treat most Director-started workers as packet coordinators: they should actively manage context, choose helper models/functions, and use worker-internal sub-agents for narrow scouting, context selection, verification, review, or contained implementation when that improves quality or token economy. Each worker starts with an activation report and reports back before widening scope. If a worker needs an oracle/review thread, it returns an Oracle Request Packet to the Director instead of creating or messaging that thread directly unless explicitly authorized.

Before starting a worker thread, the Director must choose the starting prompt, exact model or inherited profile, thinking level plus rationale, required skills or workflow references, context/artifact handoff, commit authority, done criteria, and evidence format. Use [Agent profiles and model routing](references/agent-profiles-and-model-routing.md): Director judgment and code-writing workers default to `high`; use `medium` for mechanical edits or bounded research, `low` for status/probes, and `xhigh` only for high-risk or final-authority gates.

## Goals Policy

The director thread maintains a project goal ledger. Worker threads use Codex Goals only when the task has a durable objective, evidence finish line, and multi-turn or uncertain path. Goals must name outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition.

## Monitoring

When checking Codex worker threads, confirm activation, reviewed planning, done criteria, required evidence, appropriate review gates, concise reporting, and no silent scope expansion. Poll/read privately and update the ledger without rapid repeated user narration; user-facing updates should emphasize decisions, task state changes, meaningful evidence, blockers/choices, and next action. Record status and archive completed threads after output is captured.
Use [REFERENCE.md](REFERENCE.md) for templates, anti-patterns, and the full workflow contract.
