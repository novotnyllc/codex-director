# Runtime Adapters

Use this reference whenever a Director workflow says to create a Codex worker thread, build context, invoke an oracle, manage a worktree, commit, or use a Codex Goal. The workflow contract is stable; adapters are interchangeable implementations, but they do not all live at the same layer.

## Core Rule

Name the role and outcome first, then choose the best available implementation:

```text
Need: independent worker for Packet 02
Role: implementation worker using build workflow
Adapter: `codex_app` thread tool
Evidence: activation report, changed files, tests, review verdict
```

Never make a worker brief depend on a private path, a single vendor, or an unstable API name. Codex worker thread lifecycle belongs to the active `codex_app` thread tool contracts. Sub-agent APIs are worker-internal execution helpers, not substitutes for Director-managed Codex worker threads. Context engines are context builders, reviewers, or oracle helpers, not thread adapters.

RepoPrompt `agent_run` and RepoPrompt agents are context/review/oracle lower-layer helpers only. When `codex_app.create_thread`, `codex_app.send_message_to_thread`, `codex_app.read_thread`, `codex_app.list_threads`, `codex_app.set_thread_title`, `codex_app.set_thread_pinned`, or `codex_app.set_thread_archived` are available, do not use RepoPrompt agents as the Director worker-thread dispatch mechanism. If the `codex_app` thread tools are unavailable or their active schema does not authorize the needed operation, record that limitation, use `simulated-unavailable`, and ask or continue locally only for coordination work instead of silently swapping in RepoPrompt agents.

The Director thread is coordination-only. It may triage, brief, check in, steer, reconcile evidence, update workflow state, and answer coordination/status questions. It must not implement, investigate, edit, test, or otherwise execute project work in its own thread. If no real worker thread is available, report the runtime blocker instead of doing the work inline.

## Adapter Selection

Prefer this order:

1. `codex_app` thread tools for real background worker threads, using the active tool schema as the source of truth.
2. Native sub-agent tools, when allowed by the active workflow, for worker-internal decomposition, verification, or bounded helper tasks.
3. Tool-specific context engines for context building, review, oracle, and durable prompt artifacts.
4. Local shell/git/file tools only for Director-owned coordination chores such as reading ledger files, inspecting worker evidence, checking git status before dispatch, or recording reconciliation state. Do not use them to perform project work in the Director thread.
5. Runtime blocker reporting when no separate worker thread is available.

Use the first adapter that satisfies the workflow's layer, independence, evidence, and safety needs. Do not block context building merely because a preferred context engine is unavailable. Do block project execution when no real Codex worker thread can own the work.

## Capability Detection

At Director setup and before the first worker dispatch in a session, inspect the active tool metadata for `codex_app` thread tools. Record the result in the ledger:

```text
Thread adapter: codex_app | simulated-unavailable
Capability source: active tool metadata
Searched terms: thread, session, conversation, chat, tab, fork, pin, title, archive, create, switch, list, close, send, wait, poll
Available ops:
Missing ops:
Excluded hits:
```

`simulated-unavailable` means a brief or ledger item exists without an executing worker. It is a blocked state, not permission for the Director to perform the work inline.

Exclude these hits from `codex_app` thread detection:

- Gmail or Outlook email threads
- GitHub review/comment threads
- Notion or app discussion threads
- RepoPrompt agent sessions, compose tabs, workspace tabs, or context chats
- `multi_agent_v1` sub-agents
- Browser or Chrome tabs

## Thread Management Adapter

The active `codex_app` tool schema is the contract. Do not document or call thread lifecycle operations that are not present in that schema. A user request to set up or use a Director is the explicit separate-thread authorization for bounded worker threads inside that project scope; outside that scope, `codex_app.create_thread` still requires fresh authorization from the active tool instructions.

Current `codex_app` thread contract:

| Operation | Tool | Contract |
|---|---|---|
| Create worker thread | `codex_app.create_thread` | `prompt`, `target`, optional `model`, optional `thinking`; use only when the active tool instructions authorize creating a new or separate thread |
| Continue / steer worker | `codex_app.send_message_to_thread` | `threadId`, `prompt`, optional `model`, optional `thinking` |
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

- worker title
- starting prompt
- explicit authorization basis for creating a new/separate thread under the active tool instructions, usually the user-requested Director scope
- target project/worktree or projectless directory
- model and thinking level plus rationale
- required skills or workflow references
- context artifacts or source files to read first
- git/worktree handling and commit authority
- done criteria
- evidence format and verbosity limit

Use `create_thread.prompt` for the full launch prompt. Use `create_thread.model` with an exact model id allowed by the active schema, such as `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, or `gpt-5.3-codex-spark`, when the selected worker profile calls for an override. Use `create_thread.thinking` only with active-schema values: `low`, `medium`, `high`, or `xhigh`. Thinking/model defaults: Director judgment and code-writing workers use main/high; Spark is a separate-budget scout/helper lane for status, probes, prompt export, bounded research, and mechanical low-risk work; high-risk or final-authority gates use main/xhigh. Otherwise mark the brief as inheriting the default runtime settings. After creation, title and pin important project/packet workers when useful.

Every real worker must start with an activation report. If it does not, steer it once:

```text
Before continuing, return the activation report required by the Director brief:
instructions read, task shape, selected workflow, research lane, oracle lane, review gate, evidence, git/worktree handling, Goal fit, done criteria.
```

If the worker still skips activation or broadens scope, stop that lane and re-brief it.

### Required Thread Handle Fields

Every running or queued worker needs a ledger handle:

```text
worker_id:
thread_id:
thread_title:
adapter: codex_app | simulated-unavailable
status: queued | running | needs_input | blocked | cancel_requested | stale | completed | archived
project_id:
target: local | worktree | projectless
repo_path:
worktree_path:
branch:
base_ref:
model:
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
last_turn_seen:
read_cursor:
next_action:
blockers:
archive_after:
cleanup_required:
```

For non-dynamic work, this ledger can live in the Director thread notes or a repo-local status artifact. Escalate to `.workflow/<slug>/` when the task needs persistent packet state, multiple worker handles, worktrees, approval checkpoints, integration state, or durable evidence files.

### Polling, Input, And Staleness

Read a newly created worker once after creation to confirm activation. For active short tasks, poll every 30-60 seconds. For long-running tasks, poll every 2-5 minutes and immediately after user steering, suspected blockage, or a dependent worker finishing.

Polling cadence is not user-update cadence. Poll privately and update the ledger quietly between concise user-facing updates. Updates at appropriate intervals are fine, but they should emphasize decisions, task state changes, meaningful worker evidence, blockers/choices, and next action; avoid implementation narration, tool-by-tool detail, repeated polling notes, and long status prose.

When a worker needs input:

1. Answer from the brief, ledger, project instructions, or existing user authority when the answer is within scope.
2. Choose the steering prompt's thinking level from the same policy: `low` for routine reminders/status, `medium` for continuing a reviewed plan, `high` for substantive judgment or implementation steering, and `xhigh` for risky or final decisions.
3. Ask the user when the answer changes outcome, expands scope, exposes sensitive data, requires production/destructive action, or changes commit authority.
4. Record the decision in the ledger or `.workflow/<slug>/state.json`.

A worker is stale when it misses the expected check-in window, stops making observable progress, or no longer matches the active brief. Steer once with the original boundary or stop request. If it remains stale, mark `stale`, archive after capturing the last readable state, and dispatch a replacement worker with a clean brief.

### Cancel And Cleanup Semantics

Cancellation is a state transition in the Director ledger:

```text
running -> cancel_requested -> stale | completed-cancelled -> archived
```

Adapter discovery may add a hard-cancel operation in a later `codex_app` schema. The current `codex_app` thread schema does not expose hard cancel, so use `codex_app.send_message_to_thread` with a stop instruction, then poll with `codex_app.read_thread`. Do not archive a worker before recording its last known status, partial artifacts, branch/worktree, and cleanup needs.

Partial worktree cleanup is project work. The Director records the cleanup requirement and dispatches a cleanup/reconciliation worker. The Director does not resolve files, remove branches, or rewrite working trees inline.

## Hooks Adapter

Codex supports lifecycle hooks and loads them from `hooks.json`, inline `[hooks]` config, and plugin-bundled `hooks/hooks.json`. Hooks are enabled by default under the canonical `features.hooks` key, but non-managed hooks still require trust review and can be disabled by runtime policy.

The Director plugin bundles hooks as an optional, scoped advisory layer. Implementation notes live beside the hook files under `plugins/codex-director/hooks/`.

| Event | Director use |
|---|---|
| `SessionStart` | Inject Director/worker role context only for Director-marked starts and compact resumes |
| `UserPromptSubmit` | Inject routing context only when the prompt or recent transcript is Director-marked |
| `Stop` | Emit a structured non-blocking closeout warning for Director-marked turns |
| `SubagentStart` / `SubagentStop` | Remind Director-marked nested helpers to stay worker-internal and roll evidence up |

Hooks do not create threads and are not a substitute for `codex_app.create_thread`. They are lifecycle reminders around the `codex_app` thread adapter: role context, scoped warnings, and state hygiene prompts. Worker briefs, activation reports, monitoring, review gates, and ledger state remain the enforcement surface.

## Worker-Internal Sub-Agent Adapter

Sub-agents and other native delegation helpers sit below Codex worker threads. Most non-trivial Director-started workers should consider themselves packet coordinators, not monolithic executors. Use worker-internal helpers when the active workflow allows packet-internal decomposition and the helper can return concise evidence to the owning thread.

Allowed uses:

- a worker thread decomposes one packet into narrow subtasks
- a worker runs a bounded scout, verification, review, or implementation helper
- a worker uses a helper to select likely models/functions/files/tests before loading broad context
- a worker uses a helper to map context slices, call sites, ownership, or verification surfaces
- a dynamic workflow packet recursively needs its own mini-orchestration
- the helper's output can be rolled up into the worker's result file or evidence summary

Rules:

1. Start non-trivial packets with a helper/context strategy: what can be scouted, what should stay in the owning worker, and what context should be excluded.
2. Only parallelize disjoint work.
3. Tell each sub-agent what sibling helpers are doing and what files/modules to avoid.
4. Assign model/thinking by task shape: Spark/low for narrow probes, Spark/medium for bounded research or mechanical edits, main/high for code-writing/review helpers, and main/xhigh only for risky or final-authority helper work.
5. Use helpers to reduce context load, not to create more transcript mass; ask for file paths, line refs, facts, commands, and confidence.
6. Wait or poll regularly; do not leave helpers unattended.
7. Verify helper output before the owning worker claims its packet is complete.
8. Roll up helper evidence into the worker summary; do not expose helper transcripts as the Director ledger.
9. Do not let a sub-agent create a second top-level dynamic workflow plan. Nested plans must stay under the owning packet.

## Context Engine Adapter

A context engine can implement research, planning, review, or oracle phases. The Director still owns the workflow contract.

Usual mapping:

- Verify workspace: bind to the project root first.
- Broad planning: context builder in plan mode, optionally exported when a durable artifact or handoff is useful.
- Investigation: context builder in question mode, then focused oracle/chat follow-up.
- Review: git survey, then context builder in review mode with explicit comparison scope.
- Oracle: curate selection first, then oracle send in plan/review/chat mode.
- Handoff: export plan/review/oracle responses only when workers need a stable artifact path.

Context-engine oracle turns are worker-internal or Director-owned context helpers. When the oracle is a separate Codex thread, use the Codex Oracle Thread Adapter below; do not let ordinary worker threads message that oracle directly.

Do not document a context engine as part of the Director's `codex_app` thread runtime. It may be adopted later when it is the best context builder, but the Codex Director skill remains Codex-app-native and the worker lifecycle remains `codex_app` threads.

When no context engine is available:

- Have the owning worker use local search and file reads sparingly.
- Prefer structured parsers and repo-local commands over broad manual reading.
- Write a short context note with files read, facts found, assumptions, and unknowns.
- Use a Director-mediated separate worker/reviewer as the oracle lane when possible.

## Codex Oracle Thread Adapter

Use this to replicate RepoPrompt-style oracle behavior with Codex threads when Browser ChatGPT Pro is unavailable, ambiguous, unsafe for the payload, unnecessary, or lower-value than a local source-backed review.

- The Director creates or continues a dedicated oracle/review Codex thread using `codex_app` thread tools and records the thread id in the ledger.
- Default to main/high for ordinary independent critique and main/`xhigh` when this is the ChatGPT Pro-unavailable fallback, high-risk review, final-authority gate, or conflict resolution lane.
- The Director sends curated Oracle Request Packets to the oracle thread: mode, exact question, evidence/artifact paths, concise summary, constraints, requested output, and fallback tolerance.
- Worker threads do not send messages to the oracle thread directly. They return Oracle Request Packets to the Director, and the Director routes, monitors, reads, reconciles, and sends findings back.
- Continue the same oracle thread when follow-up depends on the same evidence lineage. Create a fresh oracle thread when the question, risk level, task, or independence boundary changes.
- Oracle output remains advisory; local evidence, tests, and source-backed facts remain authoritative.

## Browser ChatGPT Pro Oracle Adapter

Browser ChatGPT Pro is an oracle adapter, not the oracle role itself.

Use it when a Pro web-model second opinion is materially valuable, whether or not the user explicitly said Pro: high-ambiguity planning, product/UX/content judgment, broad architecture tradeoffs, conflicting local reviews, final external critique before high-cost work, or user requests for ChatGPT Pro/web. Prefer the local Codex oracle/review lane for sensitive payloads, routine source-backed code review, normal diffs, and fast review loops. Do not open or navigate an in-app Browser just to check whether Pro is available; inspect Pro availability only during a selected Browser Pro oracle run, or in an already-open ChatGPT tab when safe and non-disruptive.

Before Browser work, read any existing local capability sentinel as a routing hint only. Preferred sentinel locations are user state (`$XDG_STATE_HOME/codex-director/chatgpt-pro-capability.json` or `~/.local/state/codex-director/chatgpt-pro-capability.json`), active `.workflow/<slug>/state.json`, repo-local untracked `.codex-director/local-state/`, then Director ledger/thread notes when sandboxed. Missing, stale, or inaccessible sentinel means `unknown` and must not trigger Browser navigation.

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

If authority is unclear, default to `no-commit` for workers and ask the user or Director before committing. Commits must not include secrets, raw private data, generated bulky artifacts, unrelated edits, or unresolved conflict markers.

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

## Installability Adapter

For plugin-package checks:

- Validate `.codex-plugin/plugin.json`.
- Validate the shared `novotnyllc/marketplace` entry when installability changes.
- Validate plugin-bundled `hooks/hooks.json` and run the bundled hook runner against marked and unmarked sample payloads.
- Validate every `SKILL.md` frontmatter.
- Check relative links.
- Verify README commands match the current plugin layout.
- If evaluating quality, run the plugin/skill evaluator before and after changes when available.

For install instructions, use the GitHub marketplace source:

```bash
codex plugin marketplace add novotnyllc/marketplace
codex plugin add codex-director --marketplace novotnyllc
```

Do not publish local checkout install commands in user-facing docs unless the user explicitly asks for development-only instructions.
