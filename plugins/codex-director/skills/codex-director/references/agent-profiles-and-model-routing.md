# Agent Profiles And Model Routing

Use this when the Director thread is choosing Codex worker thread roles, model families, and reasoning effort, and when setting up the Director thread itself.

## Core Policy

Use delegation aggressively when it improves speed, coverage, review independence, risk control, context management, or token economy. Do not wait for the user to say "subagents", "swarm", "oracle", or "Pro".

Non-trivial Director-created worker threads are work-item coordinators, not monolithic executors: they must use the defined workflow/playbook that matches the assigned work item, select the relevant functions/files/tests before reading broadly, choose helper lanes by task shape, delegate at least one real independent scouting, context, verification, critique/review, implementation, or oracle/review lane before final evidence, and return concise evidence instead of accumulating transcript mass. Ordinary tool use, self-checks, or saying helpers were considered does not satisfy this gate. Use `packet` only for concrete `.workflow/<slug>/packets/` artifacts.

Acceptable helper/subagent lanes include research scouts, code/context scouts, verification helpers, critique/review helpers, implementation helpers for disjoint contained subwork, and oracle/review lanes when the workflow requires independent judgment. High-risk or non-trivial planning should include both a scout/context lane and a critique/review lane. If a non-trivial worker lacks helper/subagent capability, it must report `blocked:<reason>` or ask the Director/user for direction rather than continuing as a monolithic executor. Direct leaf is worker-internal only and requires separate tiny, mechanical, and low-risk rationale in activation and final evidence.

Helper outputs are advisory until the owning worker verifies them, reconciles them with authoritative repo/workflow evidence, and includes them in final evidence. Worker evidence remains advisory to the Director until the Director reads the child thread with `codex_app.read_thread`, captures the terminal child report, reconciles done criteria and helper/direct-leaf policy, and records acceptance.

Director-created workers use the latest non-Spark main model exposed by the active schema by default, for example `gpt-5.5` when it is listed. Never choose older main-family model ids such as `gpt-5.4` when a newer main model is available. The only older-numbered model exception is `gpt-5.3-codex-spark`, because Spark's latest available line is 5.3, and only when Spark is the right fit for a narrow scout, status/probe, optional artifact packaging, bounded research, Browser automation runner, or mechanical low-risk helper lane. Spark is never an authority lane.

The Director/coordinator thread itself defaults to latest-main/`xhigh`: routing, decomposition, worker launch contracts, project target resolution, review/oracle decisions, evidence reconciliation, integration decisions, and completion/blocker calls are the Director's real work. This default applies to the Director thread, not to every worker it launches.

Implementation and code-writing workers default to latest-main/high. Use Spark only for mechanical low-blast-radius edits with obvious verification, and use low/Spark only for status, lookup, or narrow read-only probes. Escalate implementation to latest-main/xhigh for architecture, auth/security, data models/migrations, production config, concurrency, payments/permissions, cross-repo contracts, or hard-to-reverse decisions.

Use only model and thinking overrides accepted by the active `codex_app` thread schema. Prefer the latest main model id and do not use older main-family ids. Spark is the only exception, and only for true Spark-fit lanes. If the Director passes `create_thread.model` or writes a `Model:` line in the worker brief, that value must be the latest main id unless the lane is explicitly Spark-fit. Omit the model only when the launch contract intentionally inherits a runtime default that is known to resolve to the latest main model; otherwise write the exact latest active-schema model id and thinking level into the worker brief.

## Agent Profiles

| Profile | Purpose | Default model | Effort |
| --- | --- | --- | --- |
| `research-scout` | Narrow repo/docs/web/prior-art question, no edits | Spark | low/medium |
| `context-scout` | Fast code-map, ownership, command, or file-location probe | Spark | low |
| `artifact-packager` | Package optional scratch/handoff context artifacts only when a stable file path is explicitly useful | Spark | medium |
| `chatgpt-pro-oracle-runner` | Assemble the prompt payload, open chatgpt.com with Browser only for a selected oracle run, prompt the user to log in if needed, start a new chat, minimally detect Pro availability, select ChatGPT Pro or the requested Pro-tier model when available, submit prompt, wait, capture result, or route to built-in main/`xhigh` fallback when Pro is unavailable | Spark | medium |
| `work-item-coordinator` | Own a non-trivial assigned work item, run the matching workflow/playbook, choose and use required context/helper lanes, select models/functions/files/tests, and roll up verified evidence | latest main | high |
| `implementation-worker` | Bounded build/refactor/test work item with code-writing or verification | latest main by default; Spark only for mechanical or very contained low-risk code | high by default; medium only for mechanical edits; xhigh for risky code |
| `adversarial-reviewer` | Challenge plan/code/evidence before continuation | latest main by default; Spark only for quick low-risk first pass | high/xhigh |
| `planner` | Turn research into work items, dependencies, gates | latest main | high |
| `integration-auditor` | Integrate packet results, reconcile commits/worktrees, audit evidence | latest main | high/xhigh |
| `security-data-reviewer` | Auth, data, migration, secrets, production-risk review | latest main | xhigh |

## Runtime Role Labels

When a concrete helper/delegation tool exposes generic role labels, map Director profiles this way:

| Director profile | Generic role |
| --- | --- |
| `research-scout` / `context-scout` | `explore` |
| `artifact-packager` / `chatgpt-pro-oracle-runner` | `engineer` or `explore` for read-only prep/automation |
| `work-item-coordinator` | `pair` for ambiguous/context-heavy work items, `engineer` for clear implementation work items |
| `implementation-worker` | `engineer` for clear work items, `pair` for ambiguous work items |
| `adversarial-reviewer` | `pair` or `design` depending on runtime support |
| `planner` | `pair` or `design` |
| `integration-auditor` | `pair` |
| `security-data-reviewer` | strongest available main-model review role |

Fresh worker is the default for independent bounded work items. Steer one existing worker only for tightly coupled sequential work, many tiny items, or when preserving working memory reduces risk.

## Native `multi_agent_v2` Helper Profiles

When a worker thread exposes native `multi_agent_v2` tools, treat them as the concrete worker-internal implementation of the runtime role labels above. The Director parent still creates only durable Codex worker threads through `codex_app`; it does not replace worker creation with `spawn_agent`, `followup_task`, `wait_agent`, `list_agents`, or `close_agent`.

Record the active helper surface in activation and evidence: `multi_agent_v2 surface: available:<tools>`, `namespaced:<namespace>`, `v1-only`, `unavailable:<reason>`, or `ambiguous:<reason>`. Use only fields exposed by the active helper schema. When `agent_type`, `model`, `reasoning_effort`, `service_tier`, or `fork_turns` are available, set them deliberately; when hidden, write the intended role/model/thinking/fork rationale into the helper prompt.

| RP role | Use it for | Model/effort default | Fork/context guidance |
| --- | --- | --- | --- |
| `explore` | one-question code, docs, git, test, external-fact, or prior-art scouting; no edits | Spark or latest-main at low/medium depending on risk and source freshness | prefer `fork_turns: "none"` plus exact paths/questions when self-contained |
| `pair` | default complex helper, ambiguous planning, root-cause synthesis, baseline/instrumentation loops, final reconciliation input | latest main/high; xhigh when the helper's answer could become final authority | fork enough recent context to preserve constraints, but pass artifact paths instead of transcript mass |
| `engineer` | clear bounded implementation or mechanical refactor slice after the owning worker has a plan | latest main/high for code; Spark/medium only for truly mechanical low-risk edits | assign explicit file/module ownership and sibling boundaries |
| `design` | bounded plan critique, UX/copy/design review, adversarial polish pass, report artifact | latest main/high or xhigh for high-impact critique | request a concise findings list or report path, not open-ended redesign |

RP-style lifecycle maps directly to V2 lifecycle: spawn with a narrow task name, detach/continue the owning worker, wait for mailbox signals, read the helper's actual message or final report, spot-check claims against source evidence, summarize only verified evidence, and close the helper. `wait_agent` and `list_agents` are status signals only. A completed helper left open is cleanup debt; an unread helper final is not evidence.

## Spark Routing

Use Spark for bounded, evidence-oriented throughput work:

- research scouts
- status summaries
- artifact/result collection
- optional scratch/handoff artifact packaging when a stable file path is needed
- Browser ChatGPT Pro oracle automation with built-in main/`xhigh` fallback when Pro is unavailable, unsafe, or lower-value than local review
- first-pass reconnaissance
- mechanical edits with clear tests
- very contained low-risk work-item execution
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

## Latest Main Model Routing

Use the latest non-Spark main model exposed by the active schema for:

- work-item coordinator workers that choose and enforce context/helper strategy
- director top-level task decisions
- dynamic workflow setup and concrete packet design
- final plan review
- cross-repo integration
- conflict resolution
- ordinary implementation with design judgment
- high-stakes review
- Director readback and acceptance decisions after worker terminal signals
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
- optional scratch/handoff artifact packaging when a stable file path is needed
- ordinary research scouts
- simple bounded reviews
- mechanical docs/config/test-data edits with obvious verification
- worker follow-ups that continue an already-reviewed plan without changing scope

Use `high` for:

- worker work-item coordination, ordinary plan judgment, and evidence synthesis before Director acceptance
- bounded implementation with real code changes
- planning from research
- ordinary adversarial review
- refactors
- optimization iterations
- dynamic workflow work-item execution from concrete packet files
- code-writing workers unless the edit is purely mechanical

Use `xhigh` for:

- the Director/coordinator thread's default routing, decomposition, worker launch contracts, project target resolution, review/oracle decisions, ledger reconciliation, and final acceptance
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

Escalate from Spark to the latest main model when:

- evidence conflicts
- risk crosses auth/security/data/migration/production boundaries
- worker outputs or dynamic workflow packet outputs disagree
- the result affects architecture
- the worker cannot name a runnable verification surface
- completion depends on judgment rather than simple evidence

Escalate worker or oracle lanes from `high` to `xhigh` when:

- the decision is final and hard to reverse
- the verification surface is incomplete or indirect
- the task spans repos or ownership boundaries
- a Goal or dynamic workflow claims completion but evidence is mixed

## Token Economy

Prefer narrow Spark scouts only when the task is a true Spark fit and the cost of a weaker answer is low. Prefer one latest-main work-item coordinator or integration pass after scouts finish. Pass artifact paths and concise summaries instead of full transcripts. For non-trivial work items, spend a small amount of reasoning up front deciding which workflow to run, which context to load, and which helpers to use; that is usually cheaper than letting the owning thread absorb the whole repo.

Clean up completed runtime sessions after their evidence is recorded. Keeping many stale sessions open increases monitoring cost and makes the Director ledger harder to trust.
