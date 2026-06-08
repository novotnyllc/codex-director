---
name: director-investigate
description: Runs the Codex Director investigate/research lane for read-only diagnosis and evidence gathering. Use when a Director worker brief explicitly invokes $codex-director:director-investigate for repo or docs reconnaissance, failure diagnosis, external fact checks, regression research, or current-state evidence.
metadata:
  short-description: Run read-only research lane
---

# Director Investigate

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

This split workflow skill is worker-side. If its activation marker, skill body, callback text, or readback evidence appears in a parent Director thread, the parent treats it only as routing input or child evidence. It does not load this workflow into the parent and does not permit parent inline browser, repo, provider, or project execution.

1. Read local instructions and the owning Director brief.
2. Load [Investigate And Research Workflow](../codex-director/references/investigate-research-workflow.md).
3. Report activation: `workflow-skill-loaded:$codex-director:director-investigate`, selected workflow/playbook `director-investigate`, top-level control loop, read-only boundary, user-outcome fit, helper/subagent lane plan, and evidence contract.
4. Gather facts from the narrowest authoritative sources.
5. Separate confirmed evidence, inference, uncertainty, and recommended next actions.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, planned RP-style helper profiles, and helper cleanup. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, one narrow hypothesis or evidence question, source boundaries, leave-alone instructions, sibling lanes, model/thinking/fork rationale, expected output, confidence format, and cleanup expectation.
- Use `explore` helpers for one-question scouts such as git archaeology, code-path tracing, docs/spec checks, log checks, or current external facts.
- Use `pair` only for a disjoint deeper hypothesis that needs multi-step reasoning. Cap parallel pair-style helpers to genuinely disjoint hypotheses and avoid duplicating in-flight work.
- V2 evidence counts only after this worker reads the helper output, spot-checks material claims against cited sources, synthesizes contradictions, and records `close_agent` or `close_blocked:<reason>`.

## Workflow

1. Activate: restate the question, read-only boundary, selected workflow, top-level loop, source types, helper policy, and evidence contract.
2. Map sources: identify the smallest authoritative sources: local instructions, code/docs, logs, git history, tests, live read-only endpoints, user-provided artifacts, official external docs, and approved local credential/config sources by key name or presence only.
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
- Do not treat `wait_agent`, `list_agents`, or helper final-status notifications as findings.
- Stop for secrets, private raw data, production writes, destructive actions, or unclear scope.
- For credential/provider questions, check approved project-local sources before recommending dashboard edits or secret rotation: repo-local env/config files by key name and presence, runbooks/docs, service-token paths, hosted env metadata, and branch/ref mappings. If a source requires interactive password/unlock or the user rejects it, record it as unavailable and do not keep probing it.
- Separate confirmed evidence from inference when diagnosing live OAuth/auth flow. A stale authorize page, expired state, redirect check, or provider-exchange log is not proof of app completion.

## Output

Return concise findings with source paths/commands, confidence, contradictions, open questions, user-outcome checkpoint vs remaining proof, recommended workflow for next work, native helper surface, V2 helper paths/evidence/owner verification/cleanup when used, and cleanup/archive state.
