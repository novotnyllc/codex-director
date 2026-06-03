# Agent Profiles And Model Routing

Use this when the director thread is choosing Codex worker thread roles, model families, and reasoning effort.

## Core Policy

Use delegation aggressively when it improves speed, coverage, review independence, risk control, context management, or token economy. Do not wait for the user to say "subagents" or "swarm".

Use `gpt-5.3-codex-spark` as a separate-bucket throughput model for bounded work. It is older, so it should not be the final authority for high-stakes judgment. Use the main/default stronger model for planning authority, conflict resolution, integration, security/data decisions, and final completion audits.

`xhigh` is an escalation level, not a standing role.

Native Codex thread tools accept these model override values: `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, and `gpt-5.3-codex-spark`. They accept these thinking levels: `low`, `medium`, `high`, and `xhigh`. Omit the model only when the launch contract intentionally inherits the current project/default profile; otherwise write the exact model id and thinking level into the worker brief.

## Agent Profiles

| Profile | Purpose | Default model | Effort |
| --- | --- | --- | --- |
| `research-scout` | Narrow repo/docs/web/prior-art question, no edits | Spark | low/medium |
| `context-scout` | Fast code-map, ownership, command, or file-location probe | Spark | low |
| `prompt-exporter` | Package context for oracle/review lanes | Spark | medium |
| `browser-oracle-runner` | Open chatgpt.com with Browser, start a new chat, select the highest-capability available or requested model, record the visible model label, submit prompt, wait, and capture result | Spark | medium |
| `implementation-worker` | Bounded build/refactor/test packet with clear instructions | Spark or main | high |
| `adversarial-reviewer` | Challenge plan/code/evidence before continuation | Spark first pass, main for final/high-risk | high/xhigh |
| `planner` | Turn research into work items, dependencies, gates | main | high |
| `integration-auditor` | Integrate packet results, reconcile commits/worktrees, audit evidence | main | high/xhigh |
| `security-data-reviewer` | Auth, data, migration, secrets, production-risk review | main | xhigh |

## Runtime Role Labels

When a delegation adapter exposes generic role labels, map Director profiles this way:

| Director profile | Generic role |
| --- | --- |
| `research-scout` / `context-scout` | `explore` |
| `prompt-exporter` / `browser-oracle-runner` | `engineer` or `explore` for read-only prep |
| `implementation-worker` | `engineer` for clear packets, `pair` for ambiguous packets |
| `adversarial-reviewer` | `pair` or `design` depending on runtime support |
| `planner` | `pair` or `design` |
| `integration-auditor` | `pair` |
| `security-data-reviewer` | strongest available main-model review role |

Fresh worker is the default for independent packets. Steer one existing worker only for tightly coupled sequential work, many tiny items, or when preserving working memory reduces risk.

## Spark Routing

Use Spark for bounded, evidence-oriented work:

- research scouts
- status summaries
- artifact/result collection
- prompt export packaging
- Browser ChatGPT oracle automation
- first-pass reconnaissance
- mechanical edits with clear tests
- low-risk packet execution
- first-pass adversarial review
- "find evidence for/against this one claim"

Do not use Spark as final authority for:

- architecture choices with long-term consequences
- subtle code review
- security/auth/data/migration decisions
- conflicting worker output integration
- complex Goal completion audits
- ambiguous UX/product judgment
- current API/library freshness when browsing or primary sources are needed

## Main Model Routing

Use the main/default stronger model for:

- director top-level task decisions
- dynamic workflow setup and packet design
- final plan review
- cross-repo integration
- conflict resolution
- high-stakes review
- security/auth/data/migration judgment
- deciding whether work is complete or blocked

## Effort Levels

Use `low` for:

- status sweeps
- artifact collection
- command discovery
- file-location probes
- narrow "find this" scouts

Use `medium` for:

- Browser oracle round trips
- prompt export
- ordinary research scouts
- simple bounded reviews
- small implementation packets

Use `high` for:

- bounded implementation with real code changes
- planning from research
- ordinary adversarial review
- refactors
- optimization iterations
- dynamic workflow packet execution

Use `xhigh` for:

- final plan review before complex implementation
- auth/security/data/migration review
- conflicting evidence resolution
- cross-repo reconciliation
- root-cause analysis with contradictory evidence
- deciding whether a complex Goal is complete or blocked
- production-risk decisions

## Spark `xhigh`

Spark `xhigh` is useful for bounded older-model-safe reasoning when preserving the main model bucket matters. Use it for deeper but still scoped work:

- compare two bounded implementation options
- review a specific packet result
- reason over a contained failure report
- critique a narrow plan section

Do not use Spark `xhigh` as the last word on high-stakes or cross-cutting decisions. Escalate final authority to the main model, usually `high` or `xhigh` depending on risk.

## Escalation Rules

Escalate from Spark to main model when:

- evidence conflicts
- risk crosses auth/security/data/migration/production boundaries
- packet outputs disagree
- the result affects architecture
- the worker cannot name a runnable verification surface
- completion depends on judgment rather than simple evidence

Escalate from `high` to `xhigh` when:

- the decision is final and hard to reverse
- the verification surface is incomplete or indirect
- the task spans repos or ownership boundaries
- a Goal or dynamic workflow claims completion but evidence is mixed

## Token Economy

Prefer many narrow Spark scouts over one giant context load when questions are independent. Prefer one main-model integration pass after scouts finish. Pass artifact paths and concise summaries instead of full transcripts.

Clean up completed runtime sessions after their evidence is recorded. Keeping many stale sessions open increases monitoring cost and makes the Director ledger harder to trust.
