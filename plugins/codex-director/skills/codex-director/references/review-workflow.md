# Review Workflow

Use for code review, plan review, worker-output review, branch diffs, PRs, and adversarial gates.

## Principle

Review is an independent challenge pass. Findings lead. Summaries and praise are secondary. A review without a clear scope is not a review yet.

## Phase 0: Confirm Scope

Start by confirming the worker launch contract: model, thinking level plus rationale, commit authority, relevant Codex skills, and the required review workflow. Record skills considered, loaded, skipped, and unavailable in activation.

Determine what is being reviewed:

- Uncommitted changes vs `HEAD`.
- Staged changes.
- Last N commits.
- Branch vs `main`, `master`, or named target.
- Pull request.
- Plan artifact.
- Worker-thread output and claimed evidence.

If the scope is ambiguous and cannot be inferred from the request and git state, ask before reviewing.

Comparison scope examples:

```text
uncommitted: all working-tree changes vs HEAD
staged: staged changes only
back:3: last three commits
main: current branch compared with main
<branch>: current branch compared with a named branch
artifact:<path>: plan/report/worker output review
```

Do not call a review complete until the comparison scope is explicit.

## Phase 1: Survey

For code:

- Check git status.
- Inspect changed files list.
- Check recent commits if branch review.
- Note generated files and unrelated dirty changes.

For broad branch reviews, include changed-file list and comparison target in the review brief. For generated files, decide whether to review source inputs, generated output, or both.

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

When a review-oriented context engine is available, use it before final findings. The instructions must include comparison scope, current branch, changed files, and focus areas. If no context engine is available, do a targeted diff review plus file reads for changed call sites and tests.

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

Examples of gap follow-ups:

- "Previous review covered API handlers but not migrations; review migrations now."
- "Previous review checked correctness but not auth/security; focus on auth edge cases."
- "Plan review covered sequencing but not verification; review test strategy."

## Output Format

Keep it concise:

- **Must-fix**: bugs, regressions, safety issues. Include file:line for code.
- **Suggestions**: useful but not blocking.
- **Questions**: only if answers could change the verdict.
- **Verdict**: approve, approve with nits, block, or insufficient evidence.
- **Residual risk**: tests or paths not covered.

If no issues are found, say that clearly and name remaining test gaps.

## Anti-Patterns

- Reviewing without a comparison scope.
- Reporting summary before findings.
- Treating style nits as must-fix.
- Skipping changed call sites or tests when API behavior changed.
- Saying "looks good" without naming residual risk or unverified surfaces.
