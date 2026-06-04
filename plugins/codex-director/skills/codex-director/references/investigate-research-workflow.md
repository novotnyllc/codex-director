# Investigate And Research Workflow

Use for read-only diagnosis, research before planning, external fact gathering, "how does this work?", regressions, and unclear failures.

## Principle

Separate evidence gathering from implementation. Research should feed planning, not turn into accidental edits. Stop when the question is answered with source-backed confidence or when the remaining blocker is explicit.

## Phase 0: Triage

Confirm the launch contract first: model, thinking level plus rationale, commit authority, required skills/workflows, repo/path, and expected evidence. Discover applicable Codex skills and record skills considered, loaded, skipped, and unavailable in activation.

Classify the request:

- Explanation: answer how something works.
- Diagnosis: identify root cause.
- Research scout: gather facts before planning.
- Prior-art scan: find similar implementations or decisions.
- External facts: current docs, APIs, libraries, standards, product behavior.

Define the expected output:

- Short answer.
- Investigation report.
- Research memo.
- Plan input.
- Blocker summary.

## Phase 1: Evidence Plan

Choose research lanes:

- Repo/code: modules, types, tests, configs.
- Docs/specs/runbooks.
- Memory/prior decisions.
- Git history, issues, PRs, prior plans.
- External web/docs/current facts.
- Logs, traces, generated artifacts supplied by the user.

For each lane, write one narrow question. Avoid broad prompts like "investigate everything."

Classify each fact before relying on it:

- Stable repo fact: verify from source files, tests, docs, or history.
- Project decision: verify from plans, issues, commits, meeting notes, or user-provided context.
- External current fact: verify from primary/current sources before relying on it.
- Sensitive/private fact: inspect locally and report only summary or artifact path.

For unstable external facts such as current APIs, package versions, laws, prices, product behavior, model availability, schedules, or security advisories, browse or use an available current-source adapter. Prefer primary sources and include dates.

## Phase 2: Scout

Use independent scouts when lanes can run in parallel:

```text
Scout <lane>: Answer <specific question>. Return sources, confidence, conflicts, and plan implications. Do not propose implementation unless asked.
```

Possible implementations:

- Codex research worker thread.
- Owning worker local search/read/git.
- Web browsing for current external facts.
- Any available context engine or worker-internal sub-agent that can answer the narrow scout question without bloating the owning thread.

Keep scout output brief. The coordinator synthesizes; scouts do not write the final voice.

Scout result format:

```text
Question:
Sources:
Finding:
Confidence: confirmed / likely / plausible / unknown
Conflicts:
What this changes:
Follow-up needed:
```

## Phase 3: Context Synthesis

Build a coherent model:

- What is known?
- What evidence supports it?
- What conflicts?
- What is inferred rather than directly observed?
- What remains unknown?
- What does this imply for planning or implementation?

If using a context engine, feed it the research notes/report path so prior research informs the selection.

## Phase 4: Main Investigation

For diagnosis or root-cause work:

1. Form hypotheses.
2. Test the highest-probability path first.
3. Rule out alternates with specific evidence.
4. Use an oracle lane for cross-file synthesis when evidence spans modules.
5. Stop when root cause and counter-evidence are concrete.

When this workflow runs inside a Director-managed worker and cross-file synthesis needs oracle judgment, return an Oracle Request Packet with the hypothesis, evidence paths, conflicts, and exact question. The Director routes that packet to the selected oracle lane and reconciles the result.

Use a pair/investigation worker only when multi-step tracing is needed. It should append findings to a report or return concise evidence.

## Phase 5: Report

Report:

- Summary.
- Evidence with file:line or links.
- Root cause or answer.
- Eliminated hypotheses.
- Confidence and remaining unknowns.
- Recommended next action.

For research before planning, include "Plan implications" as the most important section.

For durable investigations, write a report with:

```text
Summary:
Symptoms / question:
Evidence ledger:
Ruled out:
Root cause or best current explanation:
Confidence by claim:
Recommendations:
Remaining unknowns:
```

Do not collapse uncertain claims into a single confident conclusion. Preserve epistemic levels per claim.

## Anti-Patterns

- Implementing from a research thread.
- Huge source dumps.
- External research without dates/sources for unstable facts.
- Treating inference as confirmed fact.
- Running overlapping scouts on the same question.
- Omitting contradictions because they make the answer less tidy.
