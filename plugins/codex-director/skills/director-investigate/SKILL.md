---
name: director-investigate
description: Runs the Codex Director investigate/research lane for read-only diagnosis and evidence gathering. Use when a Director worker brief explicitly invokes $director-investigate for repo or docs reconnaissance, failure diagnosis, external fact checks, regression research, or current-state evidence.
---

# Director Investigate

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions and the owning Director brief.
2. Load [Investigate And Research Workflow](../codex-director/references/investigate-research-workflow.md).
3. Report activation: `workflow-skill-loaded:$director-investigate`, selected workflow/playbook `director-investigate`, top-level control loop, read-only boundary, helper/subagent lane plan, and evidence contract.
4. Gather facts from the narrowest authoritative sources.
5. Separate confirmed evidence, inference, uncertainty, and recommended next actions.

## Workflow

1. Activate: restate the question, read-only boundary, selected workflow, top-level loop, source types, helper policy, and evidence contract.
2. Map sources: identify the smallest authoritative sources: local instructions, code/docs, logs, git history, tests, live read-only endpoints, user-provided artifacts, or official external docs.
3. Gather facts: query/read sources in a traceable order. Prefer primary sources and exact commands/paths over memory or summaries.
4. Use scout lanes: for non-trivial investigations, delegate independent questions such as history, code path, docs/spec, log evidence, or external current facts.
5. Compare evidence: separate confirmed facts, inference, contradictions, stale/unknown areas, and confidence.
6. Diagnose: state likely cause, alternatives considered, what would disprove the hypothesis, and the smallest next verification.
7. Recommend routing: say whether the next step is build, review, deep-plan, dynamic workflow, oracle, or no action.
8. Finish: return findings, evidence paths/commands, confidence, blockers, risks, and cleanup/archive state.

## Evidence Standard

Every material claim should have a source: file path, command/check, artifact, tool result, log line, official source, or explicit inference. If a fact might be time-sensitive and matters, verify it live or label it unverified.

## Required Invariants

- Stay read-only unless the Director explicitly expands authority.
- Use primary sources, live artifacts, logs, tests, docs, or code as appropriate for the question.
- Use helper/subagent scout lanes for non-trivial or parallelizable investigation, or record a blocked helper capability.
- Do not turn investigation into implementation or review acceptance.
- Treat callbacks and final-looking messages as wake signals for Director readback.
- Stop for secrets, private raw data, production writes, destructive actions, or unclear scope.

## Output

Return concise findings with source paths/commands, confidence, contradictions, open questions, recommended workflow for next work, and cleanup/archive state.
