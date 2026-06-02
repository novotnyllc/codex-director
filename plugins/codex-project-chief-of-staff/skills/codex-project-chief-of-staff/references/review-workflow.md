# Review Workflow

Use for code review, plan review, worker-output review, branch diffs, PRs, and adversarial gates.

## Principle

Review is an independent challenge pass. Findings lead. Summaries and praise are secondary. A review without a clear scope is not a review yet.

## Phase 0: Confirm Scope

Determine what is being reviewed:

- Uncommitted changes vs `HEAD`.
- Staged changes.
- Last N commits.
- Branch vs `main`, `master`, or named target.
- Pull request.
- Plan artifact.
- Worker-thread output and claimed evidence.

If the scope is ambiguous and cannot be inferred from the request and git state, ask before reviewing.

## Phase 1: Survey

For code:

- Check git status.
- Inspect changed files list.
- Check recent commits if branch review.
- Note generated files and unrelated dirty changes.

For plans/workers:

- Read the task brief.
- Read done criteria.
- Read claimed evidence.
- Identify unverified claims.

## Phase 2: Build Review Context

Build review context with the lightest adequate path:

- Include the confirmed comparison scope and changed files.
- Use git diff, targeted reads, code structure, tests, and local instructions.
- Use a review-oriented context engine if available and useful.
- If the change is broad, create a separate review-oriented Codex worker thread.

Do not manually deep-read the whole repo before review context is built.

## Phase 3: Adversarial Checklist

Challenge:

- Correctness and edge cases.
- Security, privacy, data handling, auth, and production risks.
- API/contract compatibility.
- Error handling and resilience.
- Tests and verification.
- Migration/rollback safety.
- UI/UX regressions if user-facing.
- Scope creep and unrelated changes.
- Commit coherence.

For plan review, also challenge:

- Missing research.
- Bad sequencing.
- Over-large or under-specified work items.
- Unclear done criteria.
- Missing stop/review points.

## Phase 4: Fill Gaps

If the first review misses a material area:

1. State what was covered.
2. State what was not covered.
3. Run a focused follow-up review for the gap.

Do not pretend a partial review is complete.

## Output Format

Keep it concise:

- **Must-fix**: bugs, regressions, safety issues. Include file:line for code.
- **Suggestions**: useful but not blocking.
- **Questions**: only if answers could change the verdict.
- **Verdict**: approve, approve with nits, block, or insufficient evidence.
- **Residual risk**: tests or paths not covered.

If no issues are found, say that clearly and name remaining test gaps.
