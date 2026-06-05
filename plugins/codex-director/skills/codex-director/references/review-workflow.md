# Review Workflow

Use for code review, plan review, worker-output review, branch diffs, PRs, and adversarial gates.

## Principle

Review is an independent challenge pass. Findings lead. Summaries and praise are secondary. A review without a clear scope is not a review yet.

When reviewing Director-created worker output, the review must challenge the Director acceptance path itself: unread child finals, missing `readback_status`, missing helper/subagent evidence, invalid direct-leaf rationale, and missing cleanup/archive state are review findings, not administrative nits.

## Phase 0: Confirm Scope

Start by confirming the worker launch contract: model, thinking level plus rationale, commit authority, relevant Codex skills, and the required review workflow. Record skills considered, loaded, skipped, and not loaded in activation.

Determine what is being reviewed:

- Uncommitted changes vs `HEAD`.
- Staged changes.
- Last N commits.
- Branch vs `main`, `master`, or named target.
- Pull request.
- Plan artifact.
- Worker-thread output and claimed evidence, including child-thread readback state and helper/direct-leaf acceptance.

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
- Confirm the Director or owning orchestrator read the child thread with `codex_app.read_thread` after the terminal signal and captured the terminal report from the child thread itself.
- Check `read_cursor` or `last_turn_seen`, `readback_status`, `final_report_captured`, `evidence_reconciled`, `helper_policy_accepted`, `acceptance_status`, and cleanup/archive state when the output came from a Director-created worker.
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
- Callback-only, expected-final-only, or stale-summary-only acceptance without child-thread readback.
- Missing, weak, or implausible helper/subagent evidence for non-trivial Director-created work.
- Direct-leaf claims that do not separately justify tiny, mechanical, and low-risk.
- Missing archive/cleanup state for accepted, stale, superseded, review, oracle, verification, or cleanup workers.

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
- **Acceptance gate**: for Director-created worker output, state whether child-thread readback, evidence reconciliation, helper/direct-leaf acceptance, review/oracle status, and cleanup/archive state are present.
- **Residual risk**: tests or paths not covered.

## Review Worker Evidence

When this review workflow is itself run by a Director-created review worker, its final report must include:

- explicit review scope and comparison/artifact reviewed;
- findings/verdict and residual risk;
- helper/subagent lanes used, or direct-leaf rationale with separate tiny, mechanical, and low-risk detail;
- review/oracle status if another lane was used or requested;
- cleanup/archive expectation.

For Director acceptance, the review worker's verdict is only candidate evidence until the Director reads the review worker thread with `codex_app.read_thread`, captures the terminal report from the child thread itself, reconciles scope/findings/helper/direct-leaf status, and records cleanup/archive state. A callback, expected final, or verdict alone must not be accepted.

If no issues are found, say that clearly and name remaining test gaps.

## Anti-Patterns

- Reviewing without a comparison scope.
- Reporting summary before findings.
- Treating style nits as must-fix.
- Skipping changed call sites or tests when API behavior changed.
- Saying "looks good" without naming residual risk or unverified surfaces.
- Approving Director-created worker output when it is still `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, missing helper/direct-leaf acceptance, or missing cleanup/archive state.
- Treating ordinary tool use or self-checks as the mandatory helper/subagent lane for non-trivial work.
