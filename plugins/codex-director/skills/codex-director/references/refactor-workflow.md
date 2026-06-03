# Refactor Workflow

Use for behavior-preserving simplification, duplication removal, organization, boundary cleanup, or code health improvements.

## Principle

Refactoring preserves behavior. If behavior changes are needed, name them as bug fixes and separate them from the refactor commits.

## Phase 0: Scope And Safety

1. Confirm target area and local instructions.
2. Check git status and unrelated changes.
3. Decide branch/worktree.
4. Confirm commit authority from the worker brief.
5. Discover applicable Codex skills and workflow references; record skills considered, loaded, skipped, and unavailable in activation.
6. Confirm model and thinking level from the launch contract.
7. Identify tests that prove behavior is preserved.
8. Define "out of scope" explicitly.

Do not start broad cleanup from a vague request. Narrow the target first.

## Phase 1: Scout Structure

Map the territory before proposing changes.

Scout questions:

- What are the key types/functions and responsibilities?
- Where is duplication or scattered logic?
- Which patterns already exist nearby?
- Which tests cover the behavior?
- Which public APIs or data contracts must not change?

Use explore workers or local code-structure/search. Keep each scout to one area.

## Phase 2: Analyze Opportunities

Preferred path:

- Use review/context tooling to identify redundancies, coupling, complexity, or misplaced responsibilities.

Fallback path:

- Compare adjacent modules, call sites, tests, and shared helpers.

Rank opportunities by:

- behavior safety
- value
- blast radius
- test coverage
- dependency order

Reject aesthetic-only rewrites unless the user asked for them.

Use two passes for non-trivial refactors:

1. Opportunity review: find duplication, complexity, ownership boundaries, and risk.
2. Execution plan: choose ordered refactor items with done criteria and verification.

Do not combine analysis and editing unless the change is tiny and mechanical.

## Phase 3: Refactor Plan

The plan must include:

- refactor items in safe order
- behavior invariants
- files/modules touched
- tests/checks per item
- commit boundaries
- rollback strategy

Most refactors should be sequential. Later items often depend on earlier structure.

Parallelize only when modules do not overlap and verification can prove behavior preservation independently.

## Phase 4: Plan Review

Run adversarial review before edits.

Challenge:

- Does this actually reduce complexity?
- Is behavior preserved?
- Are public contracts stable?
- Are item boundaries reviewable?
- Are tests enough to detect accidental behavior change?
- Is any cleanup unrelated?

## Phase 5: Implement Sequentially

Implement one item at a time:

1. Apply the smallest coherent structural change.
2. Run targeted tests/checks.
3. Commit if the item passes.
4. Review before moving to the next item when risk is non-trivial.

If a behavior ambiguity appears, pause. Do not "fix" it inside a refactor unless re-scoped.

If a refactor exposes a behavior bug, stop and reclassify the work. Either fix the bug under a build workflow item with tests, or keep the refactor behavior-preserving and file the bug separately.

## Phase 6: Final Review

Reviewer checks:

- behavior equivalence
- test adequacy
- contract compatibility
- no unrelated churn
- simpler structure is actually clearer
- commits are coherent

## Evidence

Report:

- refactor items completed
- behavior invariants preserved
- tests/checks run
- changed files
- commit hashes
- review verdict
- residual risk

## Anti-Patterns

- Refactoring and changing behavior without saying so.
- Creating abstractions before proving duplication or complexity warrants them.
- Parallelizing overlapping refactors.
- Skipping tests because the change "should be mechanical."
- Leaving the code in a half-migrated style.
