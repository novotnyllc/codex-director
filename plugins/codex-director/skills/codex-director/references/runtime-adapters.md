# Latest Codex Runtime Tooling

Use this reference whenever a Director workflow says to create a Codex worker thread, choose a project target, title/pin/archive/read/steer a thread, build context, invoke an oracle, manage a worktree, commit, or use a Codex Goal. Latest Codex native thread and project tooling is the contract for Director worker lifecycle. Required Codex definitions and native schemas are assumed present by definition; this skill is not a portable workflow engine with interchangeable worker engines.

## Core Rule

Name the role and outcome first, then use the concrete latest-Codex thread/project operation that owns it:

```text
Need: independent worker for Packet 02
Role: implementation worker using build workflow
Codex tool: `codex_app.create_thread` with resolved project target
Evidence: activation report in ledger, changed files, tests, review verdict
```

Codex worker thread lifecycle belongs to the active `codex_app` thread and project tool contracts. Sub-agent APIs are worker-internal execution helpers, not substitutes for Director-managed Codex worker threads. Context engines are context builders, reviewers, or oracle helpers, not worker-thread lifecycle tools.

RepoPrompt `agent_run` and RepoPrompt agents are context/review/oracle lower-layer helpers only. Do not use them as the Director worker-thread dispatch mechanism. Director setup confirms the required latest-Codex `codex_app` thread/project tools and schema before operating, and the skill assumes those native definitions are present. Do not swap in RepoPrompt agents for Codex worker threads.

The Director thread is coordination-only. It may triage, brief, check in, steer, reconcile evidence, update ledgers or workflow artifacts, and answer coordination/status questions from its existing ledger or conversation state. It must not implement, investigate, edit, test, or otherwise execute project work in its own thread. Direct inline corrective repo execution after a worker stalls is prohibited; for emergencies, the Director records explicit authority and dispatches a bounded emergency worker or dynamic workflow, but the Director still must not inspect or execute repo/prod work inline. If a status/checkup/lookup answer would require repo/docs/code inspection, the Director must spawn or continue a Codex worker thread instead of doing the work inline. Latest-Codex thread/project tooling is the assumed execution surface for that worker-thread path.

The Director is a rapid-fire intake surface, not a single-task executor. For multiple user asks, dispatch or continue separate bounded worker threads or workflow packets, record handles and expected evidence in the ledger, and stop after the dispatch/checkpoint instead of waiting inline unless the user explicitly asks for live narration.

## Tooling Boundaries

Use these layers:

1. `codex_app` thread/project tools are required for Director-owned worker lifecycle: create, target, title, pin, read, steer, archive, and callback signaling when authorized.
2. Native sub-agent tools are worker-internal helpers for decomposition, verification, or bounded helper tasks when the owning worker chooses them.
3. Context, oracle, and Browser tools provide evidence, review, and durable artifacts; they do not own Codex worker lifecycle.
4. Local shell/git/file tools are only for Director-owned coordination chores such as reading ledger files, inspecting worker evidence, checking git status before dispatch, or recording reconciliation state. Do not use them to perform project work in the Director thread or to satisfy repo/doc/code-backed status, checkup, or lookup requests.
5. Director setup/activation confirms the required latest-Codex worker/thread/project tooling before any Director operation. The skill assumes these native definitions are present and treats them as the Director worker lifecycle contract.

## Setup Contract Confirmation

At Director setup and before the first worker dispatch in a session, confirm the active latest-Codex `codex_app` thread/project tools and schema. Record the confirmed contract in the ledger:

```text
Codex thread/project tooling: verified
Capability source: active tool metadata
Searched terms: thread, session, conversation, chat, tab, fork, pin, title, archive, create, switch, list, close, send, wait, poll, project, target, worktree
Required ops verified:
Schema notes:
Excluded hits:
```

Latest Codex is the premise of the skill; keep this setup record focused on the active Codex-native thread/project contract.

Exclude these hits from `codex_app` thread detection:

- Gmail or Outlook email threads
- GitHub review/comment threads
- Notion or app discussion threads
- RepoPrompt agent sessions, compose tabs, workspace tabs, or context chats
- `multi_agent_v1` sub-agents
- Browser or Chrome tabs

## Thread And Project Tooling

The active `codex_app` tool schema is the contract. Do not document or call thread lifecycle operations that are not present in that schema. A bare request to set up or use a Director makes the current thread the Director; create a separate Director thread only when the user clearly asks for a separate or new one. The Director may continue an existing active Director only when the user clearly asks to continue or reuse it, and must not resurrect or unarchive an archived prior Director by default. Title the Director as `<Project Display Name> Director`, applying any stable workspace Director/title emoji convention when available, and keep it pinned when pinning is exposed. The Director title is a stable project handle; do not rename it for transient tasks, incidents, packets, callbacks, or worker focus changes. Rename it only to correct project identity or stable Director/title convention, on explicit user request, or when the Director intentionally changes project scope. Prefer explicit project/workspace names over the cwd basename. Track active task focus in the ledger and child-worker titles; child-worker titles must not overwrite, mask, or replace the parent Director focus. A user request to set up or use the Director authorizes bounded worker threads inside that project scope; outside that scope, `codex_app.create_thread` still requires fresh authorization from the active tool instructions.

Current `codex_app` thread contract:

| Operation | Tool | Contract |
|---|---|---|
| Create worker thread | `codex_app.create_thread` | `prompt`, resolved `target`, optional `model`, optional `thinking`; use only when the active tool instructions authorize creating a new or separate thread |
| Continue / steer worker | `codex_app.send_message_to_thread` | `threadId`, `prompt`, optional `model`, optional `thinking` |
| Continue / wake Director | `codex_app.send_message_to_thread` | `threadId` is the Director thread id; pass `thinking: "xhigh"` when thinking selection is exposed, including heartbeat wakeups and user-requested Director continuations |
| Worker callback to Director | `codex_app.send_message_to_thread` from the worker runtime, only if exposed there and explicitly authorized in the worker brief | `threadId` is the Director thread id; signal only `final`, `blocked`, `needs_user`, `oracle_request`, or ownership-changing `handoff`; pass `thinking: "xhigh"` when exposed so callbacks do not downshift the Director |
| List threads | `codex_app.list_threads` | optional `query`, optional `limit` |
| Read / poll worker | `codex_app.read_thread` | `threadId`, optional `cursor`, optional `turnLimit`, optional `includeOutputs`, optional `maxOutputCharsPerItem` |
| Set title | `codex_app.set_thread_title` | `threadId`, `title` |
| Pin / unpin | `codex_app.set_thread_pinned` | `threadId`, `pinned` |
| Archive / unarchive | `codex_app.set_thread_archived` | `threadId`, `archived` |

`codex_app.create_thread.target` has exactly these top-level shapes in the current schema:

```text
project target:
  type: "project"
  projectId: <saved project id / workspace root>
  environment:
    type: "local"
    OR
    type: "worktree"
    startingState: optional { type: "working-tree" } or { type: "branch", branchName: <branch> }

projectless target:
  type: "projectless"
  directoryName: optional output directory name
```

### Project Target Resolution

Before launching a worker, resolve the `create_thread.target` from the worker's owning repo/path, not from the Director thread's current project by default.

Resolution order:

1. If the launch contract includes an explicit `projectId`, use that saved Codex project target.
2. If `projectId` is absent and the repo/path/worktree path is known, find saved Codex projects that own that path. Prefer an exact workspace-root match, then the most specific saved project whose workspace root is closest to the owned path.
3. For nested or overlapping saved project roots, do not treat overlap as ambiguity by itself. The closest owning workspace root wins.
4. For multi-repo workspaces, bind each worker to the child repo/path it owns. Do not send every worker to the Director thread's project just because the Director was opened there.
5. If no saved project owns the path, use a `projectless` target with recorded rationale. Projectless is also valid when the task is genuinely projectless.
6. If equally specific matches remain, path ownership is unclear, or the selected project would not actually cover the worker's owned repo/path, stop before launch and report a runtime blocker or ask the user for the project target. Do not guess.

Record the resolved `projectId` or `projectless` target, resolution basis, repo/path, worktree path, and projectless rationale when applicable in the worker brief and Director ledger. On resume, steering, or replacement launch, reuse that recorded target unless the user changes ownership.

Lifecycle mapping:

| Need | `codex_app` behavior |
|---|---|
| Create new thread | `codex_app.create_thread` with a valid `target`; only when the active tool contract permits new thread creation |
| Select project/worktree | For project targets, choose `target.environment.type = "local"` or `"worktree"`; worktree can start from the current working tree or a named branch when supported by schema |
| Send initial brief | Put the full self-contained launch contract in `create_thread.prompt` |
| Fork existing conversation context | Not exposed; pass an artifact path or self-contained context in the prompt |
| List active threads | `codex_app.list_threads` with a project/task query and limit |
| Switch/bind UI to thread | Not exposed; keep `threadId` in the ledger and use read/send by id |
| Send follow-up | `codex_app.send_message_to_thread` |
| Wait | Not exposed; do not invent a blocking wait call |
| Poll | `codex_app.read_thread`; record cursor/last turn seen |
| Cancel/stop | No hard-cancel tool is exposed in the current `codex_app` schema; send a stop request with `codex_app.send_message_to_thread`, record `cancel_requested`, poll for acknowledgment or staleness, then archive after evidence/cancel note is captured |
| Archive/close | `codex_app.set_thread_archived` |
| Set title/pin | `codex_app.set_thread_title`, `codex_app.set_thread_pinned` |

### Launch Contract

Before calling `codex_app.create_thread`, define:

- worker title tied to the bounded material task
- starting prompt
- explicit authorization basis for creating a new/separate thread under the active tool instructions; for a Director thread itself, this requires a clear separate/new-thread request
- resolved target project/worktree or projectless directory, including the project id/target and resolution basis
- model and thinking level plus rationale
- required skills or workflow references
- context artifacts or source files to read first
- mandatory helper/subagent lanes for non-trivial Director-created work, or direct-leaf exception with separate tiny, mechanical, and low-risk rationale
- git/worktree handling and commit authority derived from the user's request
- done criteria
- evidence format and verbosity limit
- Director callback policy and Director thread id, if worker-to-Director callbacks are available and useful

Use `create_thread.prompt` for the full launch prompt. Use `create_thread.model` with an exact model id allowed by the active schema when the selected worker profile calls for an override. A separate Director thread defaults to latest-main/`xhigh` when the active schema supports those choices. Existing Director thread continuations, heartbeat wakeups, and worker callbacks into the Director also use `xhigh` when thinking selection is exposed; do not inherit or pass low/medium/high worker thinking into the Director thread. Director-created workers default to the latest non-Spark main model, for example `gpt-5.5` when it is exposed, with thinking selected by worker task shape and risk; never choose older main-family model ids just because the schema exposes them. The only older-numbered model exception is `gpt-5.3-codex-spark`, because Spark's latest available line is 5.3, and only when Spark is the right fit for a narrow scout, status/probe, prompt export, bounded research, Browser automation runner, or mechanical low-risk helper lane. If the Director writes a `Model:` field into the brief or passes `create_thread.model`, it must use the exact latest main id unless the lane is explicitly Spark-fit. Use `create_thread.thinking` only with active-schema values: `low`, `medium`, `high`, or `xhigh`. Worker thinking defaults remain task-based: low/medium for routine probes or mechanical work, high for ordinary work-item coordination and implementation, and xhigh for high-risk or final-authority worker gates. Otherwise mark the brief as inheriting default runtime settings only when the runtime default is known to resolve to the latest main model. After creation, title workers when useful, but keep the Director pinned and pin worker threads only for an explicit user request or a durable lane that must remain visible.

Every real worker must start with an activation report. Record routine activation in the Director ledger; surface it to the user only when activation changes routing, exposes a blocker, or requires a decision. If the worker does not return activation, steer it once:

```text
Before continuing, return the activation report required by the Director brief:
instructions read, task shape, selected workflow, research lane, helper/subagent lanes or direct-leaf tiny/mechanical/low-risk rationale, oracle lane, review gate, evidence, git/worktree handling, Goal fit, done criteria.
```

If the worker still skips activation, broadens scope, becomes stale, or is superseded, send a stop/no-further-changes instruction, record the reason and any usable evidence, archive the worker after evidence capture or superseded-state recording, and re-brief only if the task is still needed. Do not reuse that worker for a different material task; create a fresh worker handle for the new assignment.

### Required Thread Handle Fields

Every running or queued worker needs a ledger handle:

```text
worker_id:
thread_id:
thread_title:
director_created_worker: yes | no
director_thread_id:
owning_director_task_id:
codex_thread_project_tooling: verified
status: queued | running | needs_input | blocked | cancel_requested | stale | pending-readback | readback_blocked:<reason> | insufficient-evidence | accepted | archived
project_id:
target: local | worktree | projectless
project_resolution_basis: explicit-projectId | exact-root-match | closest-owning-root-match | projectless-no-saved-project | projectless-task | blocked-equally-specific | blocked-unclear-ownership | blocked-selected-project-mismatch
repo_path:
worktree_path:
branch:
base_ref:
model: latest main id, inherited latest-main default, or `gpt-5.3-codex-spark` for a Spark-fit lane only
thinking:
thinking_rationale:
starting_prompt_or_artifact:
skills_required:
workflow_playbook:
commit_authority:
done_criteria:
evidence_required:
created_at:
last_poll_at:
next_wake_at:
monitor_interval:
monitor_mechanism: heartbeat | cron | manual | none
monitor_id:
stale_after:
callback_policy: none | director-thread-signal
director_callback_thread_id:
last_callback_at:
last_callback_signal:
terminal_signal: none | callback:final | callback:blocked | callback:needs_user | callback:oracle_request | callback:handoff | poll:final
last_turn_seen:
read_cursor:
readback_status: not-started | pending-readback | readback_complete | readback_blocked:<reason>
terminal_thread_read_at:
final_report_captured: yes | no
evidence_reconciled: yes | no
helper_policy_accepted: yes | no | direct-leaf:<tiny/mechanical/low-risk rationale> | blocked:<reason>
acceptance_status: running | pending-readback | insufficient-evidence | accepted | blocked | stale | archived
next_action:
blockers:
archive_after:
cleanup_required:
pinned: director-only | explicit-user-request | durable-lane | not-pinned
```

For non-dynamic work, this ledger can live in the Director thread notes or a repo-local status artifact. Escalate to `.workflow/<slug>/` when the task needs persistent packet tracking, multiple worker handles, worktrees, approval checkpoints, integration tracking, or durable evidence files.

### Resumable Monitoring, Input, And Staleness

Read a newly created worker once after creation to confirm activation when practical. Do not keep the Director turn running only to wait for spawned workers. After dispatch, record worker handles, cursor or last turn seen, `last_poll_at`, `callback_policy`, `next_wake_at`, `monitor_interval`, and `stale_after`; then stop the Director turn or schedule the lightest available wake mechanism.

Prefer signal-first monitoring when the worker runtime exposes `codex_app.send_message_to_thread` and the Director brief explicitly authorizes callback use. The worker may send a single callback to the Director thread for `final`, `blocked`, `needs_user`, `oracle_request`, or ownership-changing `handoff`; it must not send routine progress, poll, rerun, or "no blocker" callbacks. When thinking selection is exposed on the callback send, the callback must use `thinking: "xhigh"` because it wakes the Director thread. The Director treats the callback as a wake signal only, marks `terminal_signal`, sets `readback_status: pending-readback`, then reads the worker thread before accepting evidence.

Concrete callback-to-readback sequence:

1. Receive callback, poll result, heartbeat wake, resume notice, expected-final, or stale summary.
2. Update `terminal_signal` and callback metadata without accepting completion.
3. Call `codex_app.read_thread` with the recorded `thread_id` and `read_cursor` when available so only unread child turns are processed; use `last_turn_seen` when cursors are unavailable.
4. If `read_thread` succeeds and contains a terminal child report, record `readback_complete`, `terminal_thread_read_at`, updated `read_cursor`/`last_turn_seen`, and `final_report_captured: yes`.
5. Reconcile the child report against done criteria, required evidence, review/oracle gates, and helper/direct-leaf policy.
6. Record `acceptance_status: accepted | insufficient-evidence | blocked | stale` and record archive/cleanup state separately.

Duplicate or out-of-order callbacks update `terminal_signal` and then read only unread child turns by cursor. Do not downgrade already accepted evidence unless `read_thread` reveals a newer terminal child update that changes the final report or blocker. If `read_thread` fails, is unavailable, or returns no terminal child report, record `readback_blocked:<reason>`, `pending-readback`, or `insufficient-evidence`; never record `accepted` from the callback payload alone.

Use a short quiet polling burst only when the worker is likely to finish within about a minute or an immediate dependent decision is expected. Otherwise prefer callback signaling plus a watchdog heartbeat. If callback signaling is not active for the worker, prefer a thread heartbeat attached to the Director thread for near-term follow-up when appropriate; heartbeat prompts that wake the Director thread must use `xhigh` reasoning when that setting is exposed. Use a detached cron/workspace automation only for genuinely detached monitoring. If no wake mechanism is exposed, record `monitor_mechanism: manual`, `next_wake_at`, and the next action rather than leaving the Director spinning.

Default cadence should keep overall work fast:

- Callback available: rely on the callback for terminal/blocking signals; set a watchdog heartbeat for 2-3 minutes only to catch lost callbacks or silent stalls.
- No callback, user actively waiting, or unknown short work: first watchdog in 30-60 seconds.
- Build/test/review without callback: 1-2 minutes while likely active, then 2-4 minutes after confirmed long-running execution.
- Worker-reported long operation: 3-5 minutes, then shorten to 30-90 seconds near verification or expected completion.
- Never choose a wake longer than 3 minutes while the user is actively waiting unless callback signaling is available or the worker explicitly gave a longer ETA.
- Poll immediately after user steering, suspected blockage, a dependent worker finishing, or a worker-reported handoff.

Polling cadence is not user-update cadence. Poll privately and update the ledger quietly. Do not emit user-facing messages for routine polls, waits, activation confirmations, reruns, local diagnosis, or "no blocker" checks. Surface only final evidence, real blockers or user decisions, safety/production/destructive choices, ownership-changing handoffs, and stale/cancel/archive/cleanup state. Do not return a user-visible final verdict until child-thread readback has captured terminal worker evidence and the Director has reconciled done criteria, evidence, review/oracle status, and helper/direct-leaf acceptance; if evidence is missing, report `pending-readback`, `readback_blocked:<reason>`, `stale`, or `insufficient-evidence`. Completion is not fully reconciled until worker cleanup state is recorded. Collapse repeated failures and reruns into one message only when the diagnosis changes materially or user action is needed.

Heartbeat hygiene:

- Keep at most one active heartbeat monitor per Director task unless the user explicitly asks for independent monitors.
- Prefer updating an existing monitor over creating a duplicate.
- Heartbeat prompt should be self-contained: read the Director ledger, poll recorded workers with `read_thread`, surface only visible-gate output, reschedule if active work remains, and pause/delete itself when no active worker handles remain.
- If callback signaling is active, heartbeat is a watchdog only; do not use it as the primary progress mechanism.
- Do not use heartbeat wakeups as a substitute for worker ownership; workers still own implementation, verification, and final evidence.
- Temporary cleanup, verification, oracle, and review workers should not remain pinned and should be archived once no longer active or useful.

When a worker needs input:

1. Answer from the brief, ledger, project instructions, or existing user authority when the answer is within scope and does not require repo/doc/code inspection.
1. If the answer would require repo/doc/code inspection for a status, checkup, lookup, research, investigation, verification, or implementation request, spawn or continue a Codex worker thread instead of reading repo/docs/code directly in the Director thread.
2. When steering a worker thread, choose the steering prompt's thinking level from the worker policy: `low` for routine worker reminders/status, `medium` for continuing a reviewed plan, `high` for substantive judgment or implementation steering, and `xhigh` for risky or final worker decisions. When the target is the Director thread instead, use `xhigh`.
3. Ask the user when the answer changes outcome, expands scope, exposes sensitive data, requires production/destructive action, or changes commit authority.
4. Record the decision in the ledger or the relevant workflow artifact.

A worker is stale when it misses the expected check-in window, stops making observable progress, or no longer matches the active brief. Steer once with the original boundary or stop request. If it remains stale, mark `stale`, archive after capturing the last readable state, and dispatch a replacement worker with a clean brief. If archive tooling is unavailable, record `archive_blocked:<reason>` and do not claim cleanup.

### Cancel And Cleanup Semantics

Cancellation is a state transition in the Director ledger:

```text
running -> cancel_requested -> blocked | stale -> archived
```

The current `codex_app` thread contract uses cooperative cancellation: send a stop instruction with `codex_app.send_message_to_thread`, then poll with `codex_app.read_thread`. Do not archive a worker before recording its last known status, cancellation acknowledgment or blocker, partial artifacts, branch/worktree, and cleanup needs. If archive is not exposed or fails, record `archive_blocked:<reason>` in the ledger.

Partial worktree cleanup is project work. The Director records the cleanup requirement and dispatches a cleanup/reconciliation worker. The Director does not resolve files, remove branches, or rewrite working trees inline.

## Hooks Tooling

Codex supports lifecycle hooks and loads them from `hooks.json`, inline `[hooks]` config, and plugin-bundled `hooks/hooks.json`. Hooks are enabled by default under the canonical `features.hooks` key, but non-managed hooks still require trust review and can be disabled by runtime policy.

Codex Director intentionally does not register plugin-bundled hooks. `plugins/codex-director/hooks/hooks.json` is empty because plugin-bundled hooks may apply to every Codex thread, and marker or transcript detection is not a reliable Director scope boundary.

There is no Director hook runner in the plugin package. Do not design Director behavior around hooks unless Codex exposes real thread-attached metadata or explicit per-thread binding and a future implementation is added.

No Director hook events or commands are registered in the plugin package.

Director role context, scoped warnings, state hygiene, and closeout reminders belong in worker briefs, activation reports, monitoring, review gates, and ledger state. Hooks do not create threads and are not a substitute for `codex_app.create_thread`.

## Worker-Internal Sub-Agent Helper Layer

Sub-agents and other native delegation helpers sit below Codex worker threads. Non-trivial Director-created workers are work-item coordinators, not monolithic executors. They must use the defined workflow/playbook that matches the assigned work item and at least one real worker-internal helper/subagent lane when the work is non-trivial. High-risk or non-trivial planning should use both a scout/context lane and a critique/review lane. Use `packet` only for concrete `.workflow/<slug>/packets/` artifacts.

Allowed uses:

- a worker thread decomposes one assigned work item into narrow subtasks
- a worker runs a bounded scout, verification, review, or implementation helper
- a worker uses a helper to select likely models/functions/files/tests before loading broad context
- a worker uses a helper to map context slices, call sites, ownership, or verification surfaces
- a dynamic workflow packet recursively needs its own mini-orchestration
- the helper's output can be rolled up into the worker's result file or evidence summary

Rules:

1. Start non-trivial work items with the selected workflow/playbook and a helper/context strategy: what must be scouted, which helper/subagent lane will run, what should stay in the owning worker, and what context should be excluded. Ordinary tool use, self-checks, or saying helpers were considered does not satisfy the helper gate. Direct leaf execution is worker-internal only, never Director-inline, and is allowed only for tiny, mechanical, low-risk work with separate activation rationale for tiny, mechanical, and low-risk.
2. Only parallelize disjoint work.
3. Tell each sub-agent what sibling helpers are doing and what files/modules to avoid.
4. Assign model/thinking by task shape: Spark/low for narrow probes, Spark/medium for bounded research or mechanical edits, latest-main/high for code-writing/review handoff, latest-main/xhigh for high-risk review or final authority. Spark means `gpt-5.3-codex-spark`; main means the latest non-Spark model exposed by the active schema.
5. Use helpers to reduce context load, not to create more transcript mass; ask for file paths, line refs, facts, commands, and confidence.
6. Wait or poll regularly; do not leave helpers unattended.
7. Verify helper output before the owning worker claims its work item is complete. If non-trivial work lacks helper/subagent capability, report `blocked:<reason>` or request Director/user direction instead of silently continuing as a monolithic executor.
8. Roll up helper evidence into the worker summary; do not expose helper transcripts as the Director ledger.
9. Do not let a sub-agent create a second top-level dynamic workflow plan. Nested plans must stay under the owning work item or dynamic workflow packet.
10. Do not let a worker-internal helper create nested top-level Codex worker threads unless the Director brief explicitly delegated that authority.

## Context Engine Helper Layer

A context engine can implement research, planning, review, or oracle phases. The Director still owns the workflow contract.

Usual mapping:

- Verify workspace: bind to the project root first.
- Broad planning: context builder in plan mode, saving a stable artifact only when handoff genuinely needs a path.
- Investigation: context builder in question mode, then focused oracle/chat follow-up.
- Review: git survey, then context builder in review mode with explicit comparison scope.
- Oracle: curate selection first, then oracle send in plan/review/chat mode.
- Handoff: save plan/review/oracle responses as artifacts only when workers need a stable path.

Context-engine oracle turns are worker-internal or Director-owned context helpers. When the oracle is a separate Codex thread, use the Codex Oracle Thread Lane below; do not let ordinary worker threads message that oracle directly.

Do not document a context engine as part of the Director's `codex_app` thread runtime. It may be adopted later when it is the best context builder, but the Codex Director skill remains Codex-app-native and the worker lifecycle remains `codex_app` threads.

When no context engine is available:

- Have the owning worker use local search and file reads sparingly.
- Prefer structured parsers and repo-local commands over broad manual reading.
- Write a short context note with files read, facts found, assumptions, and unknowns.
- Use a Director-mediated separate worker/reviewer as the oracle lane when possible.

## Codex Oracle Thread Lane

Use this to replicate RepoPrompt-style oracle behavior with Codex threads when Browser ChatGPT Pro is unavailable, ambiguous, unsafe for the payload, unnecessary, or lower-value than a local source-backed review.

- The Director creates or continues a dedicated oracle/review Codex thread using `codex_app` thread tools and records the thread id in the ledger.
- Default to latest-main/high for ordinary independent critique and latest-main/`xhigh` when this is the ChatGPT Pro-unavailable fallback, high-risk review, final-authority gate, or conflict-resolution lane.
- The Director sends curated Oracle Request Packets to the oracle thread: mode, exact question, evidence/artifact paths, concise summary, constraints, requested output, and fallback tolerance.
- Worker threads do not send messages to the oracle thread directly. They return Oracle Request Packets to the Director, and the Director routes, monitors, reads, reconciles, and sends findings back.
- Continue the same oracle thread when follow-up depends on the same evidence lineage. Create a fresh oracle thread when the question, risk level, task, or independence boundary changes.
- Oracle output remains advisory; local evidence, tests, and source-backed facts remain authoritative.

## Browser ChatGPT Pro Oracle Lane

Browser ChatGPT Pro is a concrete oracle lane, not the oracle role itself.

Use it when a Pro web-model second opinion is materially valuable, whether or not the user explicitly said Pro: high-ambiguity planning, product/UX/content judgment, broad architecture tradeoffs, conflicting local reviews, final external critique before high-cost work, or user requests for ChatGPT Pro/web. Prefer the local Codex oracle/review lane for sensitive payloads, routine source-backed code review, normal diffs, and fast review loops. Do not open or navigate an in-app Browser just to check whether Pro is available; inspect Pro availability only during a selected Browser Pro oracle run, or in an already-open ChatGPT tab when safe and non-disruptive.

Before Browser work, read any existing local capability sentinel as a routing hint only. Preferred sentinel locations are user state (`$XDG_STATE_HOME/codex-director/chatgpt-pro-capability.json` or `~/.local/state/codex-director/chatgpt-pro-capability.json`), repo-local untracked `.codex-director/local-state/`, then Director ledger/thread notes when sandboxed. Missing, stale, or inaccessible sentinel means `unknown` and must not trigger Browser navigation.

If the sentinel is expired and Browser Pro would materially affect routing, refresh it only from already-available non-invasive surfaces: an already-open safe ChatGPT tab, Browser/tab metadata that does not open a page, or the model-picker inspection from a just-completed selected Browser Pro oracle run. If no safe surface exists, leave it stale or record `refresh_status: deferred_no_safe_surface`; do not prompt for login or open Browser just to refresh. Write or refresh the sentinel only after those safe checks or a real Browser Pro oracle run.

Before sending anything:

1. Check for secrets, credentials, raw private data, transcripts, tokens, invite links, regulated data, or proprietary exports.
2. Redact or summarize sensitive payloads unless the user explicitly approves the exact external submission.
3. If ChatGPT is not signed in, ask the user to log in through the in-app Browser and resume after confirmation. Do not ask for credentials in chat.
4. Inspect the model picker/account UI enough to record Pro availability, visible labels inspected, and selected label; keep this inspection minimal and avoid account settings or in-progress user chats.
5. Send the prompt directly through Browser only when ChatGPT Pro or the requested Pro-tier model is available, unless the user explicitly allowed a non-Pro web fallback.
6. Save the result as a local artifact, and save the prompt only when needed.
7. Report only verdict, must-fix findings, Pro availability result, selected label or fallback note, prompt source/artifact path if created, and result artifact path unless more detail is needed.

If Browser, upload, Pro availability detection, or Pro model selection fails:

- Use the built-in Codex oracle/review lane with main/`xhigh` and record the substitution, unless the user explicitly required Browser/Pro-only/no fallback.
- If sign-in is missing, prompt the user to log in through the in-app Browser first; use fallback only if the user declines/cannot log in and fallback is allowed.
- Use a non-Pro web model only when the user explicitly allows that fallback; record it as non-Pro and do not call it the Pro oracle.

Never silently pretend ChatGPT Pro reviewed the work, and never report a non-Pro web fallback as the Pro oracle.

## Commit Authority Modes

Every worker brief must name one mode:

- `no-commit`: edit/verify only; an integration worker or user commits after review.
- `commit-when-green`: worker may commit logical units after verification.
- `ask-before-commit`: worker must stop before each commit.
- `pr-only`: worker may prepare branch/commits but final merge is via PR/review.

Derive authority from the user request and task shape. Use `commit-when-green` or `pr-only` when the user asked for durable implementation that naturally includes commits, use `no-commit` when the user explicitly forbids commits or assigns edit/verify-only work, and ask only when authority is genuinely unclear. Commits must not include secrets, raw private data, generated bulky artifacts, unrelated edits, or unresolved conflict markers.

## Worktree Policy

Use the main checkout only for one coherent workstream when the repo is clean enough and project practice allows it.

Use a worktree when work is parallel, risky, long-running, likely to conflict, or needs an isolated branch. If project convention does not define a location, prefer a sibling managed container:

```text
<repo-parent>/<repo-name>.worktrees/<task-slug>/
branch: director/<task-slug>
```

Record in the ledger:

- repo root
- branch
- worktree path
- owner worker
- base commit
- files/modules owned
- status
- merge/reconcile plan

Reconciliation checklist:

1. Confirm source and target branches.
2. Confirm worker evidence and review verdict.
3. Fetch/rebase/merge according to project practice.
4. Resolve conflicts deliberately; rerun affected verification.
5. Commit or PR the integrated result.
6. Remove the worktree only after the branch/result is recoverable.

Hide worktree mechanics from the user unless there is a decision, conflict, or blocker. The final user-facing status should name the branch/commit/PR and any remaining risks.

## Codex Goal State Machine

Goal states:

```text
none -> inspect -> create/continue -> audit -> complete
                         |              |
                         |              -> blocked
                         -> pause/clear for detours or stale goals
```

Use a Goal only when the task has all three properties:

- durable objective
- evidence finish line
- multi-turn or uncertain path

Goal text must include outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition. Completion requires evidence against the named verification surface; budget exhaustion is not completion.

Workers must report Goal status in final evidence:

```text
Goal: none / active / completed / blocked / cleared
Outcome checked:
Verification surface:
Evidence:
Residual uncertainty:
```

## Installability Tooling

For plugin-package checks:

- Validate `.codex-plugin/plugin.json`.
- Validate the shared marketplace entry when installability changes.
- Confirm `hooks/hooks.json` remains empty unless a future opt-in, thread-attached hook design is intentionally being validated.
- Validate every `SKILL.md` frontmatter.
- Check relative links.
- Verify README commands match the current plugin layout.
- If evaluating quality, run the plugin/skill evaluator before and after changes when available.

For install instructions, use the configured GitHub marketplace source:

```bash
codex plugin marketplace add <owner>/<marketplace>
codex plugin add <plugin-name> --marketplace <owner>
```

Do not publish local checkout install commands in user-facing docs unless the user explicitly asks for development-only instructions.
