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

## Output

Return verdict, must-fix/should-fix findings, quoted source limits observed, submitted context summary, model/tier availability, privacy notes, fallback status, and cleanup/archive state.
