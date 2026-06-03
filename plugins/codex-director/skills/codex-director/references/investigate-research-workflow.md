# Investigate And Research Workflow

Use for read-only diagnosis, research before planning, external fact gathering, "how does this work?", regressions, and unclear failures.

## Principle

Separate evidence gathering from implementation. Research should feed planning, not turn into accidental edits. Stop when the question is answered with source-backed confidence or when the remaining blocker is explicit.

## Phase 0: Triage

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

## Phase 2: Scout

Use independent scouts when lanes can run in parallel:

```text
Scout <lane>: Answer <specific question>. Return sources, confidence, conflicts, and plan implications. Do not propose implementation unless asked.
```

Possible implementations:

- Codex research worker thread.
- Local search/read/git.
- Web browsing for current external facts.
- Any available context or delegation runner that can answer the narrow scout question without bloating the main thread.

Keep scout output brief. The coordinator synthesizes; scouts do not write the final voice.

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

## Anti-Patterns

- Implementing from a research thread.
- Huge source dumps.
- External research without dates/sources for unstable facts.
- Treating inference as confirmed fact.
- Running overlapping scouts on the same question.
