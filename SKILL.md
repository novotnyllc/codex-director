---
name: codex-project-chief-of-staff
description: Set up and operate a project-scoped chief-of-staff Codex thread that routes, creates, monitors, steers, and archives Codex worker threads. Use when the user wants a coordinating thread, project task portfolio, thread routing policy, or Codex-native delegation across repos/workspaces with context-aware workers.
---

# Codex Project Chief Of Staff

## Quick Start

Create or operate one pinned chief-of-staff Codex thread for a single project scope. The chief thread coordinates; Codex worker threads implement, investigate, plan, or review.

Project scope is whichever boundary the user names or the current Codex project implies: saved project root, repo root, multi-repo workspace root, or projectless working directory. Do not require the project scope itself to be a git repo.

Default posture: delegate proactively when it improves speed, coverage, review independence, risk control, or token economy.

Thread vocabulary:

- Chief-of-staff thread: the pinned coordinating Codex thread.
- Codex worker thread: a background Codex thread for one bounded task.
- Context engine: tools/workflows used for planning, discovery, review, and verification.
- Research lane: a scout pass that gathers repo, docs, memory, prior-art, and external facts before planning.
- Oracle: a second-opinion reasoning lane for plan critique, review, ambiguity resolution, or risk checks.
- Adversarial review: an independent challenge pass that looks for bugs, missed requirements, unsafe assumptions, and verification gaps.
- Subagent: an optional worker-internal delegate used only when the selected workflow calls for it.

## Setup Workflow

When asked to set up a chief-of-staff thread:

1. Identify the project scope and relevant instruction files such as `AGENTS.md`, `CLAUDE.md`, or repo-local guides.
2. Create or continue the project chief-of-staff Codex thread.
3. Title it clearly, for example `Chief of Staff: <project>`.
4. Pin it.
5. Give it the operating brief from [REFERENCE.md](REFERENCE.md), adapted to the project.

## CoS Triage

Before answering or dispatching, the chief thread decides:

- Route: Which repo/path owns this?
- Shape: answer, investigate, plan, build, review, refactor, optimize, or orchestrate?
- Research: what local, memory, prior-art, or external facts must be scouted before planning?
- Done criteria: What must be true when complete?
- Evidence/token budget: what proof is required, and how concise should it be?
- Agent/model profile: Spark throughput, main-model judgment, or `xhigh` escalation?
- Risk: secrets, production, private data, destructive ops, migrations, auth, security, user-facing behavior?
- Skill/context prediction: Which named skills, context tools, oracle lane, or review workflows should the worker use?
- Delegation: direct answer, worker thread(s), subagents, or dynamic workflow?
- Work plan: What are the right work items, dependencies, and stop points?
- Review gate: fast self-check, adversarial review thread, oracle critique, or full code review?
- Git/worktree: main checkout or isolated worktree, branch name, commit cadence, reconciliation path?
- Goal fit: chief-ledger only, worker Codex Goal, or both with evidence finish line?

## Context Workflow Routing
Select the narrowest workflow that fits. If RepoPrompt MCP tools are available, prefer them for context-heavy work because `context_builder`, Oracle, exports, and RP skills provide strong planning/review handoffs. If RepoPrompt is not available, use equivalent local search/read/test tools, Codex worker threads, and the same workflow discipline.

- Research: repo/docs/memory/prior-art/external scout pass before planning. Use a Codex research thread, subagent, `context_builder`, or local/web searches as appropriate.
- Investigate: deep read-only diagnosis or "how does this work?" Prefer `rp-investigate` when available.
- Deep plan: durable implementation or architecture plan, no code. Prefer `rp-deep-plan` when available.
- Build: bounded implementation where one worker can plan and edit. Prefer `rp-build` or `context_builder` plan mode when available.
- Orchestrate: multi-part work with dependencies, parallel lanes, or substantial ambiguity. Prefer `rp-orchestrate` when available.
- Dynamic workflow: complex task orchestration with planning, packets, approvals, integration, verification, and reusable artifacts. Invoke `codex-dynamic-workflows` when available and warranted.
- Review: code review of diffs, PRs, worker output, or current changes. Prefer `rp-review` or `context_builder` review mode when available.
- Refactor: behavior-preserving structural cleanup. Prefer `rp-refactor` when available.
- Optimize: performance or efficiency work. Prefer `rp-optimize` when available.

Orchestration is the chief thread's mental model always, but formal orchestration tools or subagents should be invoked only when decomposition or delegation is actually needed.

## Gates

For non-trivial work, require research-informed and reviewed planning before implementation. The plan must define work items, dependencies, done criteria, verification, and review stop points.

Default to a research lane before planning and an adversarial review gate before marking worker-thread tasks complete. Use an oracle lane for independent critique, ambiguity resolution, cross-file reasoning, or risk checks; Browser ChatGPT can serve as an oracle when appropriate. Fast self-checks are acceptable only for trivial, mechanical, or clearly low-risk work. See [REFERENCE.md](REFERENCE.md) for detailed gate criteria and templates.

## Evidence And Verbosity

Every Codex worker thread should return concise evidence, not a transcript. Require only what proves the task: files changed, commands/tests, review verdicts, artifacts, risks, and blockers. Use summaries, slices, exports, and links to preserve quality while reducing tokens.

## Git And Worktrees

Commit regularly in logical units when repository work is being changed. A single coherent workstream may use the main checkout/branch when that is safe and matches project practice. Use isolated worktrees for parallel, risky, long-running, or conflicting work. The chief thread owns worktree creation, tracking, reconciliation, and cleanup; the user should see branch/task outcomes, not have to manage worktree mechanics. All work must ultimately reconcile into the canonical repo on an appropriate branch.

## Worker Thread Rule

Every Codex worker thread gets a bounded brief with repo/path, task, done criteria, constraints, git/worktree handling, likely skills/context workflow, research lane, oracle lane, review gates, evidence requirements, verbosity limits, and expected verification. Each worker must start with an activation report covering those fields. If scope expands beyond the brief, it reports back before widening.

Use [Agent profiles and model routing](references/agent-profiles-and-model-routing.md) to choose Spark for bounded throughput work, the main model for judgment/integration, and `xhigh` only for escalations.

## Goals Policy

The chief thread maintains a project goal ledger. Worker threads use Codex Goals only when the task has a durable objective, evidence finish line, and multi-turn or uncertain path. Goals must name outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition.

## Monitoring

When checking Codex worker threads, confirm activation, reviewed planning, done criteria, required evidence, appropriate review gates, concise reporting, and no silent scope expansion. Record status and archive completed threads after output is captured.
Use [REFERENCE.md](REFERENCE.md) for the full operating brief, worker brief template, activation report, status format, and anti-patterns.
