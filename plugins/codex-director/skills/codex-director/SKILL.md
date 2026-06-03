---
name: codex-director
description: Use when setting up or operating a project Codex Director thread for worker routing, research, oracle/review gates, worktrees, goals, and concise evidence.
---

# Codex Director

## Quick Start

Create or operate one pinned Director thread for a single project scope. The Director coordinates; bounded Codex worker threads implement, investigate, plan, review, refactor, or optimize.

Project scope is whichever boundary the user names or the current Codex project implies: saved project root, repo root, multi-repo workspace root, or projectless working directory. Do not require the project scope itself to be a git repo.

Default posture: delegate proactively when it improves speed, coverage, review independence, risk control, or token economy.

Keep this file as the compact dispatcher. Load [REFERENCE.md](REFERENCE.md) for the full operating brief, then load only the focused workflow reference needed for the task.

## Setup Workflow

When asked to set up a director thread:

1. Identify project scope and instruction files such as `AGENTS.md`, `CLAUDE.md`, or repo-local guides.
2. Create or continue the project Director thread, title it `Director: <project>`, and pin it.
3. Give it the operating brief from [REFERENCE.md](REFERENCE.md), adapted to the project.

## Director Triage

Before answering or dispatching, decide:

- Route: Which repo/path owns this?
- Shape: answer, research, investigate, deep-plan, build, orchestrate, review, refactor, or optimize?
- Evidence: what proof is required, and how concise can it be?
- Risk: secrets, production, migrations, auth, security, destructive ops, or user-facing behavior?
- Delegation: direct answer, worker thread, available delegation runner, oracle, or dynamic workflow?
- Git/worktree: main checkout, isolated worktree, branch, commit cadence, and reconciliation path?
- Goal fit: Director ledger only, worker Codex Goal, or both?

## Context Workflow Routing
Select the narrowest self-contained workflow that fits. Optional context, oracle, browser, or delegation tools may implement a phase when available, but the Director brief must not depend on external workflow names or runner-specific parameters.

- Research: repo/docs/memory/prior-art/external scout pass before planning.
- Investigate: deep read-only diagnosis or "how does this work?"
- Deep plan: durable implementation or architecture plan, no code.
- Build: bounded implementation where one worker can plan, edit, verify, and summarize.
- Orchestrate: multi-part work with dependencies, parallel lanes, or substantial ambiguity.
- Dynamic workflow: complex orchestration with planning, packets, approvals, integration, verification, and reusable artifacts.
- Review: code review of diffs, PRs, worker output, or current changes.
- Refactor: behavior-preserving structural cleanup.
- Optimize: performance or efficiency work.

Use [Runtime adapters](references/runtime-adapters.md) whenever a workflow needs worker-thread creation, context building, oracle review, Browser ChatGPT, worktrees, commits, or Codex Goals. The adapter implements the phase; the workflow contract remains self-contained.

## Gates

For non-trivial work, require research-informed and reviewed planning before implementation. The plan must define work items, dependencies, done criteria, verification, and review stop points.

Default to a research lane before planning and an adversarial review gate before marking worker work complete. Use an oracle lane for independent critique, ambiguity resolution, cross-file reasoning, or risk checks. Fast self-checks are only for trivial, mechanical, low-risk work.

## Evidence And Verbosity

Every worker returns concise evidence, not a transcript: files changed, commands/tests, review verdicts, artifacts, risks, and blockers. Use summaries, slices, exports, and links to preserve quality while reducing tokens.

## Git And Worktrees

Commit regularly in logical units when repository work is being changed. A single coherent workstream may use the main checkout/branch when that is safe and matches project practice. Use isolated worktrees for parallel, risky, long-running, or conflicting work. The director thread owns worktree creation, tracking, reconciliation, and cleanup; the user should see branch/task outcomes, not have to manage worktree mechanics. All work must ultimately reconcile into the canonical repo on an appropriate branch.

## Worker Thread Rule

Every worker gets a bounded brief with repo/path, task, done criteria, constraints, git/worktree handling, likely skills/context workflow, research lane, oracle lane, review gates, evidence requirements, verbosity limits, and verification. Each worker starts with an activation report and reports back before widening scope.

Use [Agent profiles and model routing](references/agent-profiles-and-model-routing.md) to choose Spark for bounded throughput work, the main model for judgment/integration, and `xhigh` only for escalations.

## Goals Policy

The director thread maintains a project goal ledger. Worker threads use Codex Goals only when the task has a durable objective, evidence finish line, and multi-turn or uncertain path. Goals must name outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition.

## Monitoring

When checking Codex worker threads, confirm activation, reviewed planning, done criteria, required evidence, appropriate review gates, concise reporting, and no silent scope expansion. Record status and archive completed threads after output is captured.
Use [REFERENCE.md](REFERENCE.md) for templates, anti-patterns, and the full workflow contract.
