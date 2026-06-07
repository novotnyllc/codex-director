# Build Workflow

Use for bounded implementation where one Codex worker thread can plan, edit, verify, and report.

## Principle

Do not jump from request to edits. Build enough context to produce a grounded plan, review that plan when the task is non-trivial, then implement directly. Use any available context engine, local search, code structure, file reads, helper/subagent lane, and review lane that satisfies the workflow contract.

A Director-created build worker is a coordinator for non-trivial work: it must use at least one real helper/subagent lane for context, implementation support, verification, or review before final evidence. Direct leaf is worker-internal only and requires separate tiny, mechanical, and low-risk rationale.

## Phase 0: Scope And Workspace

1. Confirm repo/path ownership and local instruction files.
2. Check git status before editing.
3. Identify unrelated dirty changes and leave them alone.
4. Decide git handling: main checkout/branch or an isolated worktree.
5. Confirm commit authority from the worker brief.
6. Discover applicable Codex skills and workflow references; record skills considered, loaded, skipped, and not loaded in activation.
7. Confirm model and thinking level plus rationale from the launch contract.
8. Record worker role, helper/subagent lanes, native helper runtime surface, blocked helper capability if any, or direct-leaf tiny/mechanical/low-risk rationale.
9. Create a Codex goal if the task is multi-turn, interruption-prone, or requires repeated verification.

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

- Start by deciding the helper/context strategy from the worker brief: which facts/files/functions/tests can be scouted by narrow helpers, which context belongs in the owning thread, and what should be excluded. For non-trivial Director-created builds this is mandatory; if no helper/subagent lane is available, report `blocked:<reason>` or ask the Director for direction instead of continuing monolithically.
- Use a context engine when one can cheaply map files, patterns, edge cases, and verification.
- Otherwise use targeted search/read/code-structure calls.
- Use worker-internal sub-agents for independent context mapping, model/function selection, call-site discovery, verification surface discovery, or narrow review when that keeps the owning thread smaller and the work disjoint. When native `multi_agent_v2` is exposed, map those lanes to `explore` for scouts, `engineer` for clear bounded sub-edits after planning, `pair` for complex implementation reasoning, and `design` only for bounded UX/copy/design critique.
- Read only files needed to understand the implementation boundary.
- Draft the plan, then use the plan review gate when non-trivial. In a Director-managed worker, return an Oracle Request Packet to the Director instead of contacting an oracle/review thread directly.

When a context engine is available, prefer a plan pass before editing. Use that tool's "build context and propose a plan" operation, then keep the selected context narrow enough for the task. For no engine, write a compact local plan after targeted reads.

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

Skip only for tiny mechanical changes. In a Director-created worker, skipping must be paired with direct-leaf rationale that separately proves the task is tiny, mechanical, and low-risk; missing or weak rationale should be reported as `insufficient-evidence` for Director reconciliation.

Review questions:

- Does this satisfy the user request exactly?
- Is the scope narrow enough?
- Are there hidden data/auth/security/production risks?
- Are tests/checks sufficient?
- Are unrelated changes excluded?
- Is the commit boundary coherent?

Use the plan review gate from `REFERENCE.md`: fast self-check for tiny low-risk changes, a Director-mediated review Codex worker thread or oracle lane for non-trivial work, and main/high or `xhigh` escalation for risky architecture/data/auth/security decisions. If this worker needs that lane, return an Oracle Request Packet to the Director with the plan, evidence, risks, and exact questions.

## Phase 4: Implementation

Implement the reviewed plan directly.

Rules:

- Prefer local patterns over new abstractions.
- Keep edits scoped.
- Add tests where risk warrants it.
- Do not broaden scope silently.
- If a plan assumption breaks, pause and report before widening.
- Commit after a coherent work item passes verification.

If a task becomes multi-item or cross-domain, escalate to the orchestration workflow. If it remains one bounded work item but has independent context/review/verification questions, keep ownership in this worker and use worker-internal helpers rather than bloating the owning thread.

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
- In a Director-managed worker, request separate review/oracle lanes by returning an Oracle Request Packet to the Director; do not create or message oracle threads directly.
- Ask the reviewer to find bugs, missed requirements, unsafe assumptions, insufficient tests, and scope drift.
- Fix must-fix findings before reporting complete.

## Final Evidence

Return 5-10 bullets:

- Changed files or artifacts.
- Branch and commit hash if committed.
- Commands/tests run with pass/fail.
- Review gate used and verdict.
- Helper/subagent lanes used, native helper surface, V2 helper role/model/thinking/fork rationale when used, owner spot-check evidence, and cleanup/close status; or direct-leaf rationale with separate tiny, mechanical, and low-risk detail.
- Done criteria satisfied.
- Known gaps, skipped checks, or blockers.
- Cleanup/archive expectation and any worktree/branch reconciliation state.

For Director acceptance, final build evidence is not accepted from a callback, expected final, or stale summary alone. The Director must read the worker thread with `codex_app.read_thread`, capture this terminal report from the child thread itself, reconcile done criteria/review/helper status, and record archive/cleanup state before marking `accepted`.

## Anti-Patterns

- Editing before a plan exists for non-trivial work.
- Reading the whole repo manually before using a context engine or scout.
- Committing without named authority mode.
- Treating partial tests as complete verification without saying what is unverified.
- Expanding a single-worker task into orchestration without updating the Director.
- Treating ordinary tool use, self-checks, or “helpers considered” as satisfying the non-trivial helper/subagent gate.
- Reporting build completion without helper/direct-leaf evidence, review/oracle status, and cleanup/archive expectations.
- Treating V2 `wait_agent`, `list_agents`, or helper final-status notifications as code evidence without reading, spot-checking, and closing the helper.
- Accepting callback-only or unread worker finals as complete.
