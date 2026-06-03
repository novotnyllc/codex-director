# Runtime Adapters

Use this reference whenever a Director workflow says to create a worker thread, build context, invoke an oracle, manage a worktree, commit, or use a Codex Goal. The workflow contract is stable; adapters are interchangeable implementations.

## Core Rule

Name the role and outcome first, then choose the best available implementation:

```text
Need: independent worker for Packet 02
Role: implementation worker using build workflow
Adapter: Codex thread tool / Agent Mode / local simulated pass
Evidence: activation report, changed files, tests, review verdict
```

Never make a worker brief depend on a private path, a single vendor, or an unstable API name. If a tool is available, use it. If it is not, fall back to the same workflow in the current thread and label it as a simulated lane.

## Adapter Selection

Prefer this order:

1. Native Codex thread tools, when available, for real background worker threads.
2. Agent Mode delegation, when available, for bounded implementation, research, review, design, or orchestration sessions.
3. Tool-specific context engines, when available, for context building, review, oracle, and prompt export.
4. Local shell/git/file tools for direct single-thread execution.
5. Simulated packet passes in the Director thread when no separate worker is available.

Use the first adapter that satisfies the workflow's independence, evidence, and safety needs. Do not block a task merely because the preferred adapter is unavailable.

## Thread Management Adapter

Minimum operations:

| Need | Native Codex thread adapter | Agent Mode adapter | Fallback |
|---|---|---|---|
| Create worker | create thread with title and brief | start agent session | create a ledger item and run a simulated pass |
| Send brief | send message to worker | agent start/steer message | write the brief into the active notes |
| Monitor | read thread status/output | wait/poll session | checkpoint the simulated pass |
| Steer | send follow-up | steer existing session | continue the current pass with the correction |
| Capture evidence | copy summary/artifacts into ledger | record agent output/result path | write concise result notes |
| Archive/cleanup | archive completed thread | cleanup completed session | mark ledger item closed |

Every real worker or simulated pass must start with an activation report. If it does not, steer it once:

```text
Before continuing, return the activation report required by the Director brief:
instructions read, task shape, selected workflow, research lane, oracle lane, review gate, evidence, git/worktree handling, Goal fit, done criteria.
```

If the worker still skips activation or broadens scope, stop that lane and re-brief it.

## Agent Mode Adapter

Use role labels rather than hard-coded model names when possible:

- `explore`: narrow reconnaissance, one question, no edits.
- `engineer`: bounded implementation when the plan is clear.
- `pair`: complex implementation, integration, or ambiguous technical judgment.
- `design`: plan critique, architecture critique, visual/product review, or adversarial design review.

Fresh worker is the default for independent items. Steer an existing worker only when the next item depends on its working memory or the items are tiny and tightly coupled.

Parallel dispatch rules:

1. Only parallelize disjoint work.
2. Tell each worker what siblings are doing and what files/modules to avoid.
3. Wait or poll regularly; do not leave workers unattended.
4. Verify one worker's done criteria before dependent work continues.
5. Clean up completed sessions after their evidence is recorded.

## Context Engine Adapter

A context engine can implement research, planning, review, or oracle phases. The Director still owns the workflow contract.

When RepoPrompt is available, the usual mapping is:

- Verify workspace: bind to the project root first.
- Broad planning: context builder in plan mode, optionally exported.
- Investigation: context builder in question mode, then focused oracle/chat follow-up.
- Review: git survey, then context builder in review mode with explicit comparison scope.
- Oracle: curate selection first, then oracle send in plan/review/chat mode.
- Handoff: export plan/review/oracle responses and pass the path to workers.

When no context engine is available:

- Use local search and file reads sparingly.
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

- `no-commit`: edit/verify only; Director or user commits.
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
- Validate `.agents/plugins/marketplace.json`.
- Validate every `SKILL.md` frontmatter.
- Check relative links.
- Verify README commands match the current plugin layout.
- If evaluating quality, run the plugin/skill evaluator before and after changes when available.

For local install instructions, avoid user-specific paths in generic docs. Prefer:

```bash
codex plugin marketplace add "$PWD"
codex plugin add codex-director --marketplace codex-director
```

For GitHub install instructions, prefer:

```bash
codex plugin marketplace add novotnyllc/codex-director
codex plugin add codex-director --marketplace codex-director
```
