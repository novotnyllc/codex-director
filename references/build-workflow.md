# Build Workflow

Use for bounded implementation where one Codex worker thread can plan, edit, verify, and report.

## Principle

Do not jump from request to edits. Build enough context to produce a grounded plan, review that plan when the task is non-trivial, then implement directly. Use RepoPrompt `context_builder` when available; otherwise use the same phases with local search, code structure, file reads, and a review-oriented thread when useful.

## Phase 0: Scope And Workspace

1. Confirm repo/path ownership and local instruction files.
2. Check git status before editing.
3. Identify unrelated dirty changes and leave them alone.
4. Decide git handling: main checkout/branch or an isolated worktree.
5. Create a Codex goal if the task is multi-turn, interruption-prone, or requires repeated verification.

## Phase 1: Quick Orientation

Keep this short. The goal is to reformulate the task in the codebase's nouns.

Look for:

- Existing module or feature names.
- Adjacent examples and established patterns.
- Tests or fixtures likely to be extended.
- Runtime/config conventions.
- Risk triggers: data, auth, security, migrations, production behavior, user-facing UI.

Good output:

```text
Task maps to <module/type/function>. Existing pattern appears in <file:line>. Likely tests live in <path>. Need plan review because <risk>.
```

Avoid deep reading before context building; it invites shallow confidence.

## Phase 2: Context Build And Plan

Preferred path:

- Use `context_builder` in plan mode with the reformulated task.
- Include known file/module hints and constraints.
- Ask it for approach, files, edge cases, and verification.

Fallback path:

- Use targeted search/read/code-structure calls.
- Read only files needed to understand the implementation boundary.
- Draft the plan yourself, then send it to an oracle/review thread when non-trivial.

The plan must include:

- Work item or single implementation step.
- Files/modules expected to change.
- Done criteria.
- Verification commands.
- Risks and rollback considerations.
- Commit boundary.

## Phase 3: Plan Review Gate

Skip only for tiny mechanical changes.

Review questions:

- Does this satisfy the user request exactly?
- Is the scope narrow enough?
- Are there hidden data/auth/security/production risks?
- Are tests/checks sufficient?
- Are unrelated changes excluded?
- Is the commit boundary coherent?

Use RepoPrompt Oracle, a review Codex worker thread, or a local adversarial self-review depending on risk.

## Phase 4: Implementation

Implement the reviewed plan directly.

Rules:

- Prefer local patterns over new abstractions.
- Keep edits scoped.
- Add tests where risk warrants it.
- Do not broaden scope silently.
- If a plan assumption breaks, pause and report before widening.
- Commit after a coherent work item passes verification.

If a task becomes multi-item or cross-domain, escalate to the orchestration workflow.

## Phase 5: Verification

Run the strongest practical verification:

- Unit/integration/e2e tests for changed behavior.
- Typecheck/lint/build if relevant.
- Screenshots for UI.
- Migration dry-runs or schema checks for database work.
- Manual command output only as a concise pass/fail summary.

If verification is blocked, report the exact blocker and what remains unverified.

## Phase 6: Adversarial Review

Default review gate for worker-thread tasks:

- Separate Codex review thread, RepoPrompt review mode, Oracle critique, or worker-internal review agent.
- Ask the reviewer to find bugs, missed requirements, unsafe assumptions, insufficient tests, and scope drift.
- Fix must-fix findings before reporting complete.

## Final Evidence

Return 5-10 bullets:

- Changed files or artifacts.
- Branch and commit hash if committed.
- Commands/tests run with pass/fail.
- Review gate used and verdict.
- Done criteria satisfied.
- Known gaps, skipped checks, or blockers.
