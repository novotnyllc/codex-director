# Agent Profiles And Model Routing

Use this when the director thread is choosing Codex worker thread roles, model families, and reasoning effort.

## Core Policy

Use delegation aggressively when it improves speed, coverage, review independence, risk control, context management, or token economy. Do not wait for the user to say "subagents", "swarm", "oracle", or "Pro".

Most Director-started worker threads should behave as packet coordinators: select the relevant functions/files/tests before reading broadly, choose helper lanes by task shape, delegate independent scouting or verification to narrow sub-agents, and return concise evidence instead of accumulating transcript mass.

Director-created workers use the current main model by default, for example `gpt-5.5` when the active schema exposes it. Never choose older main-family model ids just because they are listed by the runtime. The only older-model exception is `gpt-5.3-codex-spark`, and only when Spark is the right fit for a narrow scout, status/probe, prompt export, bounded research, Browser automation runner, or mechanical low-risk helper lane. Spark is never an authority lane.

Director-level judgment defaults to `high`: routing, decomposition, risk assessment, worker selection, evidence reconciliation, integration decisions, and completion/blocker calls are the Director's real work. Use `xhigh` only for high-risk or final-authority gates, not as a standing mode.

Implementation and code-writing workers default to current-main/high. Use Spark only for mechanical low-blast-radius edits with obvious verification, and use low/Spark only for status, lookup, or narrow read-only probes. Escalate implementation to current-main/xhigh for architecture, auth/security, data models/migrations, production config, concurrency, payments/permissions, cross-repo contracts, or hard-to-reverse decisions.

Use only model and thinking overrides accepted by the active `codex_app` thread schema. Prefer the current main model id and do not use older main-family ids. Spark is the only exception, and only for true Spark-fit lanes. Omit the model only when the launch contract intentionally inherits the current project/default profile; otherwise write the exact active-schema model id and thinking level into the worker brief.

## Agent Profiles

| Profile | Purpose | Default model | Effort |
| --- | --- | --- | --- |
| `research-scout` | Narrow repo/docs/web/prior-art question, no edits | Spark | low/medium |
| `context-scout` | Fast code-map, ownership, command, or file-location probe | Spark | low |
| `prompt-exporter` | Package durable context artifacts for oracle/review/upload/retry/handoff lanes | Spark | medium |
| `chatgpt-pro-oracle-runner` | Assemble the prompt payload, open chatgpt.com with Browser only for a selected oracle run, prompt the user to log in if needed, start a new chat, minimally detect Pro availability, select ChatGPT Pro or the requested Pro-tier model when available, submit prompt, wait, capture result, or route to built-in main/`xhigh` fallback when Pro is unavailable | Spark | medium |
| `packet-coordinator` | Own a non-trivial packet, choose context/helper strategy, select models/functions/files/tests, and roll up evidence | main | high |
| `implementation-worker` | Bounded build/refactor/test packet with code-writing or verification | current main by default; Spark only for mechanical or very contained low-risk code | high by default; medium only for mechanical edits; xhigh for risky code |
| `adversarial-reviewer` | Challenge plan/code/evidence before continuation | current main by default; Spark only for quick low-risk first pass | high/xhigh |
| `planner` | Turn research into work items, dependencies, gates | main | high |
| `integration-auditor` | Integrate packet results, reconcile commits/worktrees, audit evidence | main | high/xhigh |
| `security-data-reviewer` | Auth, data, migration, secrets, production-risk review | main | xhigh |

## Runtime Role Labels

When a delegation adapter exposes generic role labels, map Director profiles this way:

| Director profile | Generic role |
| --- | --- |
| `research-scout` / `context-scout` | `explore` |
| `prompt-exporter` / `chatgpt-pro-oracle-runner` | `engineer` or `explore` for read-only prep/automation |
| `packet-coordinator` | `pair` for ambiguous/context-heavy packets, `engineer` for clear implementation packets |
| `implementation-worker` | `engineer` for clear packets, `pair` for ambiguous packets |
| `adversarial-reviewer` | `pair` or `design` depending on runtime support |
| `planner` | `pair` or `design` |
| `integration-auditor` | `pair` |
| `security-data-reviewer` | strongest available main-model review role |

Fresh worker is the default for independent packets. Steer one existing worker only for tightly coupled sequential work, many tiny items, or when preserving working memory reduces risk.

## Spark Routing

Use Spark for bounded, evidence-oriented throughput work:

- research scouts
- status summaries
- artifact/result collection
- prompt export packaging when a durable artifact is needed
- Browser ChatGPT Pro oracle automation with built-in main/`xhigh` fallback when Pro is unavailable, unsafe, or lower-value than local review
- first-pass reconnaissance
- mechanical edits with clear tests
- very contained low-risk packet execution
- first-pass adversarial review where a main-model final verdict will follow if findings matter
- "find evidence for/against this one claim"

Do not use Spark as final authority for:

- architecture choices with long-term consequences
- non-mechanical implementation
- subtle code review
- security/auth/data/migration decisions
- conflicting worker output integration
- complex Goal completion audits
- ambiguous UX/product judgment
- current API/library freshness when browsing or primary sources are needed

## Main Model Routing

Use the current main model for:

- packet coordinator workers that choose context/helper strategy
- director top-level task decisions
- dynamic workflow setup and packet design
- final plan review
- cross-repo integration
- conflict resolution
- ordinary implementation with design judgment
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
- routine poll/read/steer prompts that do not require judgment

Use `medium` for:

- Browser ChatGPT Pro oracle automation
- prompt export when a durable artifact is needed
- ordinary research scouts
- simple bounded reviews
- mechanical docs/config/test-data edits with obvious verification
- worker follow-ups that continue an already-reviewed plan without changing scope

Use `high` for:

- Director routing, decomposition, staffing, evidence reconciliation, and completion judgment
- bounded implementation with real code changes
- planning from research
- ordinary adversarial review
- refactors
- optimization iterations
- dynamic workflow packet execution
- code-writing workers unless the edit is purely mechanical

Use `xhigh` for:

- final plan review before complex implementation
- auth/security/data/migration review
- architecture, concurrency, payments, permissions, production config, or cross-repo contract changes
- conflicting evidence resolution
- cross-repo reconciliation
- root-cause analysis with contradictory evidence
- deciding whether a complex Goal is complete or blocked
- production-risk decisions
- final authority when worker outputs disagree or verification is indirect

## Escalation Rules

Escalate from Spark to the current main model when:

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

Prefer narrow Spark scouts only when the task is a true Spark fit and the cost of a weaker answer is low. Prefer one current-main packet coordinator or integration pass after scouts finish. Pass artifact paths and concise summaries instead of full transcripts. For non-trivial packets, spend a small amount of reasoning up front deciding which context to load and which helpers to run; that is usually cheaper than letting the owning thread absorb the whole repo.

Clean up completed runtime sessions after their evidence is recorded. Keeping many stale sessions open increases monitoring cost and makes the Director ledger harder to trust.
