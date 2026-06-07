---
name: director-browser-oracle
description: Runs the Codex Director Browser ChatGPT Pro oracle lane for external second-opinion review through the signed-in browser. Use when a Director brief explicitly invokes $director-browser-oracle for delegated oracle review, Pro-only comparison, external critique, or Browser-mediated plan/result validation.
---

# Director Browser Oracle

## Quick Start

Use only when explicitly invoked by a Director brief or by the user.

1. Read local instructions, the Oracle Request Packet, and the owning Director brief.
2. Load [Browser ChatGPT Pro Oracle Workflow](../codex-director/references/browser-chatgpt-oracle-workflow.md).
3. Report activation: `workflow-skill-loaded:$director-browser-oracle`, selected workflow/playbook `director-browser-oracle`, top-level control loop, privacy classification, fallback plan, and evidence contract.
4. Confirm Browser/Pro suitability before submitting anything externally.
5. Return the oracle result, confidence, and reconciliation notes without exposing secrets or raw private data.

## Native Helper Mapping

During activation, report `native helper runtime surface`, `V2 helper policy`, and cleanup expectations. `multi_agent_v2` is the worker-internal equivalent of RP `agent_run`/`agent_manage`, not a substitute for Director-created top-level worker threads or Director-mediated oracle routing.

When V2 is available:

- Treat `spawn_agent` as RP `agent_run op=start`: choose a stable lowercase `task_name`, set `agent_type`, `model`, `reasoning_effort`, `service_tier`, and `fork_turns` when exposed, and otherwise state those choices in the helper prompt.
- Treat `wait_agent` as RP wait/poll: it is only a mailbox wake signal. Use `send_message` for queued context, `followup_task` to steer or continue a helper turn, `list_agents` for status/path checks, and `close_agent` for cleanup after evidence is consumed.
- Helper briefs must include role/profile, oracle packet path or question, privacy boundary, do/do-not data rules, model/thinking/fork rationale, expected output, evidence standard, and cleanup expectation.
- V2 helpers may support local fallback review, packet preparation, or reconciliation inside this worker. Map `explore` to source/fallback evidence checks, `engineer` to mechanical prompt artifact preparation, `pair` to reconciliation, and `design` to critique-shape/polish.
- V2 helpers must not bypass Browser/Pro suitability, privacy approval, model/tier checks, or Director-mediated oracle routing.
- If used, record helper paths, RP-style profile, model/effort rationale when exposed, owner verification, and `close_agent` or `close_blocked:<reason>`.

## Workflow

1. Activate: restate oracle question, mode, selected workflow, top-level loop, privacy class, Browser/Pro requirement, fallback lane, and evidence contract.
2. Review packet: confirm exact question, why oracle is needed, evidence to provide, requested output, constraints, and alternative lane tolerance.
3. Privacy gate: redact or omit secrets, credentials, invite links, raw private data, bulky transcripts, and sensitive customer/user data. Stop if approval is needed.
4. Suitability check: confirm Browser access, signed-in state, and whether a Pro-capable model/tier is available before external submission.
5. Submit concise context: provide only the evidence needed for the oracle judgment, with source paths or summaries rather than unnecessary transcript dumps.
6. Capture result: record model/tier if visible, verdict, must-fix/should-fix findings, confidence, caveats, and any questions.
7. Reconcile lightly: compare oracle result against the packet question and local evidence. Flag conflicts for the Director rather than deciding acceptance yourself.
8. Finish: return oracle evidence, fallback status, privacy notes, cleanup/archive state, and recommended Director action.

## Fallbacks

If Browser, auth, Pro access, or privacy approval is blocked, return `oracle_blocked:<reason>` plus the best safe fallback: local latest-main/xhigh review, separate Codex review worker, or user approval request.

## Required Invariants

- Use this lane only when explicitly delegated; ordinary workers request oracle help from the Director rather than opening ChatGPT themselves.
- Redact secrets, credentials, invite links, private raw data, and bulky transcripts before external submission.
- If Pro access, Browser auth, or privacy approval is missing, report the blocker and fallback lane.
- Do not implement, patch, or accept the task; this lane returns oracle evidence for Director reconciliation.
- Treat the oracle output as advice until the Director reconciles it against local evidence.
- Treat V2 helper output as candidate local evidence only after this worker spot-checks it and records helper cleanup.

## Output

Return verdict, must-fix/should-fix findings, quoted source limits observed, submitted context summary, model/tier availability, privacy notes, fallback status, native helper surface, V2 helper evidence/cleanup when used, and cleanup/archive state.
