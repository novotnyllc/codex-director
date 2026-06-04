# Runtime Adapters

Use this reference whenever a Director workflow says to create a Codex worker thread, build context, invoke an oracle, manage a worktree, commit, or use a Codex Goal. The workflow contract is stable; adapters are interchangeable implementations, but they do not all live at the same layer.

## Core Rule

Name the role and outcome first, then choose the best available implementation:

```text
Need: independent worker for Packet 02
Role: implementation worker using build workflow
Adapter: native Codex thread tool
Evidence: activation report, changed files, tests, review verdict
```

Never make a worker brief depend on a private path, a single vendor, or an unstable API name. Codex worker thread lifecycle belongs to native Codex thread tools. Sub-agent APIs are worker-internal execution helpers, not substitutes for Director-managed Codex worker threads. Context engines are context builders, reviewers, or oracle helpers, not thread adapters.

RepoPrompt `agent_run` and RepoPrompt agents are context/review/oracle lower-layer helpers only. When native Codex thread tools such as `create_thread`, `send_message_to_thread`, `read_thread`, `list_threads`, `set_thread_title`, `set_thread_pinned`, or `set_thread_archived` are available, do not use RepoPrompt agents as the Director worker-thread dispatch mechanism. If native thread tools are unavailable, record that limitation, use `simulated-unavailable`, and ask or continue locally only for coordination work instead of silently swapping in RepoPrompt agents.

The Director thread is coordination-only. It may triage, brief, check in, steer, reconcile evidence, update workflow state, and answer coordination/status questions. It must not implement, investigate, edit, test, or otherwise execute project work in its own thread. If no real worker thread is available, report the runtime blocker instead of doing the work inline.

## Adapter Selection

Prefer this order:

1. Native Codex thread tools for real background worker threads.
2. Native sub-agent tools, when allowed by the active workflow, for worker-internal decomposition, verification, or bounded helper tasks.
3. Tool-specific context engines for context building, review, oracle, and prompt export.
4. Local shell/git/file tools only for Director-owned coordination chores such as reading ledger files, inspecting worker evidence, checking git status before dispatch, or recording reconciliation state. Do not use them to perform project work in the Director thread.
5. Runtime blocker reporting when no separate worker thread is available.

Use the first adapter that satisfies the workflow's layer, independence, evidence, and safety needs. Do not block context building merely because a preferred context engine is unavailable. Do block project execution when no real Codex worker thread can own the work.

## Capability Detection

At Director setup and before the first worker dispatch in a session, inspect the active tool metadata for native Codex thread tools. Record the result in the ledger:

```text
Thread adapter: native-codex | simulated-unavailable
Capability source: active tool metadata
Searched terms: thread, session, conversation, chat, tab, fork, pin, title, archive, create, switch, list, close, send, wait, poll
Available ops:
Missing ops:
Excluded hits:
```

`simulated-unavailable` means a brief or ledger item exists without an executing worker. It is a blocked state, not permission for the Director to perform the work inline.

Exclude these hits from native thread detection:

- Gmail or Outlook email threads
- GitHub review/comment threads
- Notion or app discussion threads
- RepoPrompt agent sessions, compose tabs, workspace tabs, or context chats
- `multi_agent_v1` sub-agents
- Browser or Chrome tabs

## Thread Management Adapter

Found native Codex thread tools:

| Operation | Native Codex tool | Parameters that matter |
|---|---|---|
| Create worker | `codex_app.create_thread` | `prompt`, `target`, optional `model`, optional `thinking` |
| Send initial brief | `codex_app.create_thread` | `prompt` is the full launch brief |
| Send follow-up / steer | `codex_app.send_message_to_thread` | `threadId`, `prompt`, optional `model`, optional `thinking` |
| List workers | `codex_app.list_threads` | optional `query`, optional `limit` |
| Read / poll worker | `codex_app.read_thread` | `threadId`, optional `cursor`, `turnLimit`, `includeOutputs`, `maxOutputCharsPerItem` |
| Set title | `codex_app.set_thread_title` | `threadId`, `title` |
| Pin / unpin | `codex_app.set_thread_pinned` | `threadId`, `pinned` |
| Archive / unarchive | `codex_app.set_thread_archived` | `threadId`, `archived` |

Lifecycle mapping:

| Need | Native behavior |
|---|---|
| Create new thread | `create_thread` with `target.type = "project"` or `"projectless"` |
| Select project/worktree | For project targets, choose `environment.type = "local"` or `"worktree"`; worktree can start from the current working tree or a named branch |
| Send initial brief | Put the full self-contained launch contract in `create_thread.prompt` |
| Fork existing conversation context | No native thread-context fork is exposed in the current tool metadata; pass an artifact path or self-contained context in the prompt |
| List active threads | `list_threads` with a project/task query and limit |
| Switch/bind UI to thread | No native switch/bind operation is exposed; keep `threadId` in the ledger and use read/send by id |
| Send follow-up | `send_message_to_thread` |
| Poll/wait | No blocking wait operation is exposed; poll with `read_thread` and record cursor/last turn seen |
| Cancel/stop | No native hard cancel operation is exposed; send a stop request, record `cancel_requested`, poll for acknowledgment or staleness, then archive after evidence/cancel note is captured |
| Archive/close | `set_thread_archived` |
| Set title/pin | `set_thread_title`, `set_thread_pinned` |

### Launch Contract

Before calling `codex_app.create_thread`, define:

- worker title
- starting prompt
- target project/worktree or projectless directory
- model and thinking level
- required skills or workflow references
- context artifacts or source files to read first
- git/worktree handling and commit authority
- done criteria
- evidence format and verbosity limit

Use `create_thread.prompt` for the full launch prompt. Use `create_thread.model` with an exact model id such as `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, or `gpt-5.3-codex-spark` when the selected worker profile calls for an override. Use `create_thread.thinking` as `low`, `medium`, `high`, or `xhigh`. Otherwise mark the brief as inheriting the default runtime settings. After creation, title and pin important project/packet workers when useful.

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
adapter: native-codex | simulated-unavailable
status: queued | running | needs_input | blocked | cancel_requested | stale | completed | archived
project_id:
target: local | worktree | projectless
repo_path:
worktree_path:
branch:
base_ref:
model:
thinking:
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
2. Ask the user when the answer changes outcome, expands scope, exposes sensitive data, requires production/destructive action, or changes commit authority.
3. Record the decision in the ledger or `.workflow/<slug>/state.json`.

A worker is stale when it misses the expected check-in window, stops making observable progress, or no longer matches the active brief. Steer once with the original boundary or stop request. If it remains stale, mark `stale`, archive after capturing the last readable state, and dispatch a replacement worker with a clean brief.

### Cancel And Cleanup Semantics

Cancellation is a state transition in the Director ledger:

```text
running -> cancel_requested -> stale | completed-cancelled -> archived
```

Adapter discovery may add a native hard-cancel operation in a later runtime. The current native Codex thread metadata does not expose hard cancel, so use `send_message_to_thread` with a stop instruction, then poll with `read_thread`. Do not archive a worker before recording its last known status, partial artifacts, branch/worktree, and cleanup needs.

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

Hooks do not create threads and are not a substitute for `codex_app.create_thread`. They are lifecycle reminders around the native thread adapter: role context, scoped warnings, and state hygiene prompts. Worker briefs, activation reports, monitoring, review gates, and ledger state remain the enforcement surface.

## Worker-Internal Sub-Agent Adapter

Sub-agents and other native delegation helpers sit below Codex worker threads. Use them only when the active workflow allows worker-internal decomposition and the helper can return concise evidence to the owning thread.

Allowed uses:

- a worker thread decomposes one packet into narrow subtasks
- a worker runs a bounded scout, verification, review, or implementation helper
- a dynamic workflow packet recursively needs its own mini-orchestration
- the helper's output can be rolled up into the worker's result file or evidence summary

Rules:

1. Only parallelize disjoint work.
2. Tell each sub-agent what sibling helpers are doing and what files/modules to avoid.
3. Wait or poll regularly; do not leave helpers unattended.
4. Verify helper output before the owning worker claims its packet is complete.
5. Roll up helper evidence into the worker summary; do not expose helper transcripts as the Director ledger.
6. Do not let a sub-agent create a second top-level dynamic workflow plan. Nested plans must stay under the owning packet.

## Context Engine Adapter

A context engine can implement research, planning, review, or oracle phases. The Director still owns the workflow contract.

Usual mapping:

- Verify workspace: bind to the project root first.
- Broad planning: context builder in plan mode, optionally exported.
- Investigation: context builder in question mode, then focused oracle/chat follow-up.
- Review: git survey, then context builder in review mode with explicit comparison scope.
- Oracle: curate selection first, then oracle send in plan/review/chat mode.
- Handoff: export plan/review/oracle responses and pass the path to workers.

Do not document a context engine as part of the Director's native thread runtime. It may be adopted later when it is the best context builder, but the Codex Director skill remains Codex-native and the worker lifecycle remains native Codex threads.

When no context engine is available:

- Have the owning worker use local search and file reads sparingly.
- Prefer structured parsers and repo-local commands over broad manual reading.
- Write a short context note with files read, facts found, assumptions, and unknowns.
- Use a separate worker/reviewer as the oracle lane when possible.

## Browser Oracle Adapter

Browser ChatGPT is an oracle adapter, not the oracle role itself.

Use it when the user asks for ChatGPT/Pro, when a web-model second opinion is materially valuable, or when local oracle/context tools are unavailable. Before sending anything:

1. Check for secrets, credentials, raw private data, transcripts, tokens, invite links, regulated data, or proprietary exports.
2. Redact or summarize sensitive payloads unless the user explicitly approves the exact external submission.
3. Save the prompt and result as local artifacts.
4. Report only verdict, must-fix findings, and artifact paths unless more detail is needed.

If Browser, sign-in, upload, or model selection fails:

- When the user explicitly requested Browser, ChatGPT, ChatGPT Pro, or a named web model, report the blocker and ask before substituting another oracle.
- When Browser was selected opportunistically as one acceptable oracle adapter, fall back to a local oracle/review lane and record the substitution.

Never silently pretend ChatGPT reviewed the work.

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
