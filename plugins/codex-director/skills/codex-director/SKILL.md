---
name: codex-director
description: Coordinates project-scoped Codex Director threads for worker routing, research, oracle/review gates, worktrees, goals, and concise evidence. Use when setting up or operating a Director, dispatching Codex worker threads, choosing dynamic workflows, enforcing review/oracle gates, or reconciling worker evidence.
---

# Codex Director

## Load Strategy

Use this file first as the dispatcher. Load [REFERENCE.md](REFERENCE.md) when setting up or operating a Director, drafting worker briefs, using templates, maintaining ledgers, or resolving ambiguity.

Load [Latest Codex runtime tooling](references/runtime-adapters.md) before any Codex thread/project lifecycle operation. Load only the focused workflow reference that matches the task. Load Browser, Goals, model-routing, hook, or optional artifact notes only when relevant.

RepoPrompt/context engines, hooks, browsers, and sub-agents may assist with context, review, oracle, or worker-internal phases only. They do not replace Codex worker-thread dispatch.

## Core Contract

- Bare `$codex-director` or `codex-director` makes the current thread the Director unless the user clearly asks for separate/new/continue/reuse.
- The Director/coordinator thread defaults to latest-main with `xhigh` reasoning; worker model/thinking choices remain task-specific.
- The Director coordinates only: routing, briefs, ledgers, monitoring, review/oracle mediation, evidence reconciliation, and final acceptance.
- Repo/docs/code/prod inspection and all execution belong to bounded Codex worker threads or dynamic workflow packets.
- Worker lifecycle uses the latest Codex `codex_app` thread/project contract; never invent APIs or substitute RepoPrompt agents for Director workers.
- Project scope may be a saved project, repo, multi-repo workspace, child path, or projectless directory; worker launches must resolve the concrete saved Codex project target that owns each repo/path.
- Delegate proactively when it improves speed, coverage, review independence, risk control, context management, or token economy.

## Triage

Before tool use or a user-visible answer, classify the next action:

1. **Inline coordination**: conversation/ledger status, worker lifecycle/status, routing, brief drafting, monitoring/steering, evidence reconciliation, final status, or narrow coordination metadata.
2. **Worker-only inspection**: repo/docs/code-backed status, git state, implementation state, docs/spec interpretation, logs, smoke/deploy checks, production/service checks, or env/token probing.
3. **Worker-only execution**: edits, tests, implementation, refactors, reviews, deploys, migrations, rollbacks, service writes, production config/data changes, or schema/data repair.

If status, checkup, lookup, or repo/doc/code/prod evidence is not already in the ledger, dispatch or continue a Codex worker instead of inspecting inline.

## Routing

Select the narrowest self-contained shape: research, investigate, deep-plan, dynamic-workflow, build, orchestrate, review, refactor, or optimize. See the workflow references below.

Check dynamic workflow eligibility before build/orchestrate. Production or external writes, secrets/auth/security, schema/data/migrations, deploy/rollback/remediation, multi-repo or risky multi-lane work, combined verify+mutate requests, or explicit packet/dynamic-workflow requests default to dynamic workflow. Use [Execution mode stack](references/execution-mode-stack.md) and [Dynamic workflow integration](references/dynamic-workflow-integration.md).

For non-trivial or risky work, require research-informed planning and an adversarial review/oracle gate before acceptance. Director-mediated oracle/review is mandatory for production config/data, schema/database/migrations, auth/security/secrets, deploy/rollback/remediation, external service writes, conflicting evidence, cross-module/repo implementation, indirect verification, or high-risk user-facing behavior.

## Worker Launch Minimum

Every worker brief must include:

- project scope, resolved Codex project target, owned repo/path, and path-ownership rationale;
- bounded task, done criteria, selected workflow/playbook, constraints, and verification surface;
- model/thinking choice with rationale, using [Agent profiles and model routing](references/agent-profiles-and-model-routing.md);
- skills to consider/load/report, context or helper policy, and research lane;
- oracle/review policy, commit authority, git/worktree handling, and archive/cleanup expectation;
- evidence format, verbosity limit, activation report requirement, and unresolved launch-brief items;
- Goal fit: Director ledger only, worker Codex Goal, or both.

Use [REFERENCE.md](REFERENCE.md) for the full worker brief, activation report, oracle packet, ledger, git/worktree, and anti-pattern templates.

## Monitoring And Evidence

Workers start with activation. Accept only callbacks for `final`, `blocked`, `needs_user`, `oracle_request`, or ownership-changing `handoff`; otherwise poll privately, update the ledger, and avoid routine progress narration.

Use watchdogs for stale work. Completion requires captured evidence, review/oracle status, cleanup/archive state, and reconciled ledger/workflow artifacts. Surface user-visible updates only for final evidence, real blockers or decisions, safety/production/destructive choices, ownership-changing handoffs, or stale/cancel/archive/cleanup state.

## Safety And Boundaries

Ask before secrets, raw private data, production/destructive actions, external submission, ambiguous commits, or unclear cross-repo/project ownership.

Browser ChatGPT Pro oracle use requires the privacy review, Pro-value judgment, fallback behavior, and packet flow in [Browser ChatGPT oracle workflow](references/browser-chatgpt-oracle-workflow.md).

Hooks are scoped advisory reminders, not enforcement and not worker execution. See [hooks README](../../hooks/README.md).

## Reference Map

- [REFERENCE.md](REFERENCE.md): full Director operating brief, templates, ledgers, evidence, gates, git/worktrees, monitoring, examples, and anti-patterns.
- [runtime-adapters.md](references/runtime-adapters.md): Codex `codex_app` worker lifecycle, project targets, context/oracle/browser helpers, hooks, goals, and runtime boundaries.
- [execution-mode-stack.md](references/execution-mode-stack.md): Director, dynamic workflow, workers, helpers, oracle/review, and context layer responsibilities.
- [dynamic-workflow-integration.md](references/dynamic-workflow-integration.md): trigger rules, packet/result artifacts, approvals, and integration gates.
- Workflow playbooks: [research/investigate](references/investigate-research-workflow.md), [deep-plan](references/deep-plan-workflow.md), [build](references/build-workflow.md), [orchestrate](references/orchestrate-workflow.md), [review](references/review-workflow.md), [refactor](references/refactor-workflow.md), [optimize](references/optimize-workflow.md).
- [agent-profiles-and-model-routing.md](references/agent-profiles-and-model-routing.md): Director `xhigh`, worker model/thinking defaults, and Spark exception.
- [browser-chatgpt-oracle-workflow.md](references/browser-chatgpt-oracle-workflow.md): Browser ChatGPT Pro oracle privacy, fallback, and reconciliation.
- [optional-prompt-artifact-notes.md](references/optional-prompt-artifact-notes.md): optional local scratch/handoff artifact notes; not a Director workflow dependency.
- [goals-integration.md](references/goals-integration.md): Director ledger and worker Codex Goal fit, finish lines, and blocked policy.
- [hooks README](../../hooks/README.md): bundled hook scope and advisory-only semantics.
