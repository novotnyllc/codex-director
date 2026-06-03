# Build Workflow

Use for bounded implementation where one Codex worker thread can plan, edit, verify, and report.

## Principle

Do not jump from request to edits. Build enough context to produce a grounded plan, review that plan when the task is non-trivial, then implement directly. Use any available context engine, local search, code structure, file reads, and review lane that satisfies the workflow contract.

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

Build context with the lightest adequate path:

- Use a context engine when one can cheaply map files, patterns, edge cases, and verification.
- Otherwise use targeted search/read/code-structure calls.
- Read only files needed to understand the implementation boundary.
- Draft the plan, then send it to an oracle/review lane when non-trivial.

When a context engine is available, prefer a plan pass before editing. Use the adapter's "build context and propose a plan" operation, then keep the selected context narrow enough for the task. For no engine, write a compact local plan after targeted reads.

The plan must include:

- Work item or single implementation step.
- Files/modules expected to change.
- Done criteria.
- Verification commands.
- Risks and rollback considerations.
- Commit boundary.

Plan format:

```text
Implementation boundary:
Files likely to change:
Steps:
Done when:
Verification:
Review gate:
Commit authority:
Fallback if assumption breaks:
```

## Phase 3: Plan Review Gate

Skip only for tiny mechanical changes.

Review questions:

- Does this satisfy the user request exactly?
- Is the scope narrow enough?
- Are there hidden data/auth/security/production risks?
- Are tests/checks sufficient?
- Are unrelated changes excluded?
- Is the commit boundary coherent?

Use the plan review gate from `REFERENCE.md`: fast self-check for tiny low-risk changes, a review Codex worker thread or oracle lane for non-trivial work, and main/high or `xhigh` escalation for risky architecture/data/auth/security decisions.

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

If using a delegated worker, the worker may make tactical implementation decisions inside the reviewed boundary. It must report before changing public API shape, schema, auth/security behavior, production config, data migration strategy, or branch/worktree plan.

## Phase 5: Verification

Run the strongest practical verification:

- Unit/integration/e2e tests for changed behavior.
- Typecheck/lint/build if relevant.
- Screenshots for UI.
- Migration dry-runs or schema checks for database work.
- Manual command output only as a concise pass/fail summary.

If verification is blocked, report the exact blocker and what remains unverified.

Verification evidence should name commands and outcomes, not paste full logs. If a command failed because of environment state, distinguish environment blocker from code failure.

## Phase 6: Adversarial Review

Default review gate for worker-thread tasks:

- Separate Codex review thread, oracle critique, self-contained review workflow, or worker-internal review lane.
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

## Anti-Patterns

- Editing before a plan exists for non-trivial work.
- Reading the whole repo manually before using a context engine or scout.
- Committing without named authority mode.
- Treating partial tests as complete verification without saying what is unverified.
- Expanding a single-worker task into orchestration without updating the Director.
