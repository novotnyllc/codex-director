# Director Worker Readback And Helper Enforcement: Plan

## Goal
Fix the Director workflow so a Director-created worker cannot be treated as complete until the Director reads the child thread and reconciles its final evidence, and so non-trivial Director-created workers must use helper/subagent lanes unless the worker explicitly classifies its own execution as tiny, mechanical, and low-risk.

The triggering regression is the Director thread `019e9694-a460-70f2-8027-4c6b43a27a4a`: it created child thread `019e96a8-50f5-7790-923f-b2b27c228f88`, but did not reliably read and reconcile the child final report before accepting completion, and the child appeared to operate as a monolithic executor for non-trivial planning work.

## User Decisions
- Child-thread readback is mandatory. A callback, expected final message, or stale summary is only a wake signal until the Director reads the child thread.
- Helper/subagent lanes are mandatory for non-trivial Director-created workers.
- A ledger is acceptable only when it is deterministic and reliable. Hidden memory notes or best-effort state are not acceptable.
- Hook-based enforcement is out of scope because plugin hooks may affect all threads, not only Director-created ones.

## Background
- Current Director boundary: `plugins/codex-director/skills/codex-director/SKILL.md:20-24`, `README.md:47-53`, `plugins/codex-director/skills/codex-director/references/runtime-adapters.md:20-26`, and `plugins/codex-director/skills/codex-director/references/execution-mode-stack.md:23-36` define the Director as coordination-only while repo/docs/code/prod work belongs to Codex worker threads or dynamic workflow packets.
- Worker lifecycle seam: `plugins/codex-director/skills/codex-director/SKILL.md:47-59`, `plugins/codex-director/skills/codex-director/REFERENCE.md:35-87`, and `plugins/codex-director/skills/codex-director/references/runtime-adapters.md:122-164` define launch contracts, project targets, callback policy, evidence, activation, and archive/cleanup requirements for workers.
- Callback/readback seam: `plugins/codex-director/skills/codex-director/REFERENCE.md:217-230` and `plugins/codex-director/skills/codex-director/references/runtime-adapters.md:197-204` say callbacks are only terminal/blocking wake signals; the Director must poll/read the worker thread before accepting evidence. `runtime-adapters.md:88`, `runtime-adapters.md:132`, and `runtime-adapters.md:189-193` name `codex_app.read_thread`, `read_cursor`, and `last_turn_seen` as the concrete readback mechanism/state.
- Watchdog seam: `plugins/codex-director/skills/codex-director/REFERENCE.md:225-239` and `plugins/codex-director/skills/codex-director/references/runtime-adapters.md:205-219` define callback-first monitoring plus heartbeat/watchdog fallback, including one active monitor per task, cadence, and cleanup when no active worker handles remain.
- Completion/evidence seam: `plugins/codex-director/skills/codex-director/SKILL.md:63-65`, `plugins/codex-director/skills/codex-director/REFERENCE.md:241-252`, and `plugins/codex-director/skills/codex-director/references/orchestrate-workflow.md:220-234` require terminal worker evidence, review/oracle status, done-criteria checks, and ledger/workflow reconciliation before completion.
- Archive/cleanup seam: `plugins/codex-director/skills/codex-director/REFERENCE.md:200-203`, `plugins/codex-director/skills/codex-director/references/runtime-adapters.md:226-234`, and `plugins/codex-director/skills/codex-director/references/orchestrate-workflow.md:237-264` make archive/cleanup state part of completion, but cleanup can mean thread archive, stale worker handling, scratch artifacts, or worktree cleanup, so terminology must be precise.
- Helper/subagent seam: `plugins/codex-director/skills/codex-director/REFERENCE.md:60-61`, `REFERENCE.md:79-84`, and `REFERENCE.md:109-135` require a work-item coordination policy and activation fields for skills, research lane, helper policy, oracle/review, and direct-leaf rationale. `plugins/codex-director/skills/codex-director/references/runtime-adapters.md:262-287` and `execution-mode-stack.md:170-188` make helpers/subagents worker-internal lanes below the owning worker or packet.
- Direct-leaf ambiguity: `plugins/codex-director/skills/codex-director/references/execution-mode-stack.md:99-102` says tiny work still gets a tiny worker brief, while `REFERENCE.md:79-84` permits direct leaf execution inside a worker only for tiny/mechanical/low-risk work with justification. The plan must make clear that direct leaf never means Director-inline execution and that non-trivial workers require helper/subagent lanes.
- Hook scope seam: current `plugins/codex-director/hooks/hooks.json:1-3` is empty, and `plugins/codex-director/hooks/README.md:3-23` says no plugin-bundled lifecycle hooks or hook runner are registered. `runtime-adapters.md:252-261` says hooks may be globally loaded and Director role context should live in briefs, activation reports, monitoring, review gates, and ledger state instead. Therefore this fix must not add hook enforcement.
- Dynamic workflow artifact seam: `plugins/codex-director/skills/codex-director/references/dynamic-workflow-integration.md:49-55` maps worker briefs to `packets/`, worker outputs to `results/`, and final status to `final-report.md`; `REFERENCE.md:205-215` says to escalate from in-thread ledger to `.workflow/<slug>/` once multiple workers, worktrees, approvals, dependencies, oracle outputs, stale/cancel state, or span-turn work exist.
- Stale evidence to avoid overfitting: `docs/investigations/director-thread-operation-2026-06-04.md` remains useful as a regression narrative but has stale hook/default-prompt claims relative to the current tree, so the implementation should update current canonical docs rather than treating that report as the source of truth.

## Recommended Approach
Add explicit gates and boundaries across the Director docs, templates, and workflow references. This is a docs/template/playbook fix, not a hook or runtime-code fix.

### 1. Readback Acceptance Gate
A Director-created worker is not complete until the Director has:

1. Recorded the worker handle, including `thread_id`, `read_cursor` or `last_turn_seen`, and callback policy.
2. Treated any callback as a wake signal only.
3. Called `codex_app.read_thread` for the child thread before accepting completion under any path: callback, poll, heartbeat, resume, expected final, or stale summary.
4. Captured the child terminal report from the child thread itself.
5. Reconciled that report against done criteria, evidence requirements, review/oracle gates, and helper/direct-leaf policy.
6. Recorded an explicit acceptance state.
7. Recorded lifecycle closure separately from evidence acceptance, using archive/cleanup state such as `archive_ready`, `archived`, or `archive_blocked:<reason>`.

If readback fails or has not happened, the worker state must be `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, `stale`, or `blocked`; it must not be `complete` or `accepted`.

Recommended state transition:

```text
launched -> activation-read -> running -> terminal-signal -> pending-readback -> readback_complete -> accepted | insufficient-evidence | blocked | stale -> archive_ready | archived | archive_blocked:<reason>
```

`readback_complete` is not a final status by itself. It only means the Director has read the child thread; acceptance still requires evidence reconciliation.

### 2. Non-trivial Worker Helper Gate
A non-trivial Director-created worker must act as a work-item coordinator and use at least one real helper/subagent lane before final evidence. High-risk or non-trivial planning work should require both a scout/context lane and a critique/review lane. Ordinary tool use, self-checks, or saying "I considered helpers" do not satisfy this gate.

A worker may execute as a direct leaf only when all of these are true:

1. The worker, not the Director, is doing the project work.
2. The task is explicitly tiny.
3. The task is explicitly mechanical.
4. The task is explicitly low-risk.
5. The activation report and final evidence include separate rationale for all three properties: tiny, mechanical, and low-risk.

During readback reconciliation, the Director must reject implausible direct-leaf claims. Missing or weak rationale for any one of tiny, mechanical, or low-risk makes the worker `insufficient-evidence` or `blocked`, not accepted.

If a non-trivial worker lacks helper/subagent capability, it must report blocked or request Director/user direction. It must not silently continue as a monolithic executor.

### 3. Reliable State Gate
Do not add a best-effort hidden ledger. Use explicit state in the visible Director monitor/ledger template for simple single-worker cases, and require `.workflow/<slug>/` artifacts when durability is needed.

For a single short worker, the Director thread state is acceptable only if it is explicitly written into the durable conversation transcript, recoverable on resume, and visibly records:

```text
Director-created worker: yes
Director thread id:
Owning Director task id:
Thread id:
Read cursor:
Last turn seen:
Terminal signal: none | callback:final | callback:blocked | callback:needs_user | callback:oracle_request | callback:handoff | poll:final
Readback status: not-started | pending-readback | readback_complete | readback_blocked:<reason>
Terminal thread read at:
Final report captured: yes | no
Evidence reconciled: yes | no
Helper policy accepted: yes | no | direct-leaf:<rationale> | blocked:<reason>
Acceptance status: running | pending-readback | insufficient-evidence | accepted | blocked | stale | archived
Cleanup/archive status:
```

Use `.workflow/<slug>/` or another explicit durable artifact path when any of these are true:

- More than one worker handle exists.
- The task spans turns, interruptions, or resumptions.
- Callback/watchdog monitoring must survive beyond the current Director turn.
- Stale, cancel, archive, or blocked state matters.
- Review/oracle outputs must be preserved.
- Worktrees, approvals, packet dependencies, integration order, or multiple deliverables exist.
- Existing dynamic workflow thresholds in `REFERENCE.md` or `dynamic-workflow-integration.md` are met.

The durable artifact should hold packet/worker ids, Director thread id, owning task id, `thread_id`, `read_cursor` or `last_turn_seen`, terminal signal, readback status, captured final report path, helper/direct-leaf acceptance, review/oracle status, and final acceptance state.

Any worker expected to finish after the Director stops must have either durable transcript state that can be recovered on resume or `.workflow/<slug>/` artifacts.

### 4. Minimum Terminal Report Gate
A child final report is insufficient unless it includes:

- Done criteria result.
- Evidence and artifact references.
- Verification performed, or explicit verification not performed with reason.
- Helper/subagent lanes used, or direct-leaf rationale with tiny/mechanical/low-risk detail.
- Review/oracle status when required by the workflow.
- Risks, blockers, and residual uncertainty.
- Cleanup/archive expectations.

### 5. No Hook Enforcement
Keep hook enforcement out of the design. `hooks/hooks.json` should remain empty, and hook docs may only reaffirm that Director-scoped enforcement belongs in briefs, activation reports, monitoring state, review gates, and workflow artifacts.

## Ordered Work Items

### 1. Update the compact Director contract
Files:
- `plugins/codex-director/skills/codex-director/SKILL.md`

Changes:
- Add a compact readback rule under monitoring/evidence: callbacks and worker claims are terminal signals only until `codex_app.read_thread` has read the child thread.
- Add worker launch minimum language requiring helper/subagent lanes for non-trivial Director-created workers.
- State direct leaf is worker-internal only and requires tiny/mechanical/low-risk rationale.
- Add a completion gate that forbids final user status while any worker is `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, or missing helper/direct-leaf acceptance.

Reason:
- `SKILL.md` is the short contract most likely to be loaded up front. The non-negotiable rules need to appear there, not only in long references.

### 2. Update canonical templates and acceptance semantics
Files:
- `plugins/codex-director/skills/codex-director/REFERENCE.md`

Changes:
- Extend the worker thread brief template with mandatory helper policy for non-trivial work and direct-leaf exception fields for tiny/mechanical/low-risk work.
- Extend the activation report with `worker role: coordinator | direct-leaf`, helper lanes, blocked helper capability, and direct-leaf rationale.
- Extend the Director ledger/thread-handle template with readback and acceptance fields from the Reliable State Gate, including `Director-created worker: yes`, `Director thread id`, and `Owning Director task id`.
- Add a named Completion Acceptance Gate: callback/poll signal -> `read_thread` -> capture child report -> reconcile -> accept/block.
- Add anti-patterns for callback-only acceptance, unread worker completion, non-trivial worker with `helper policy: none`, and Director-inline project work disguised as direct leaf.

Reason:
- `REFERENCE.md` owns the operational templates and is the best place to make the gates executable.

### 3. Make runtime semantics concrete
Files:
- `plugins/codex-director/skills/codex-director/references/runtime-adapters.md`

Changes:
- Add a concrete callback-to-readback sequence.
- Extend required thread handle fields with `read_cursor`, `last_turn_seen`, terminal signal, readback status, final report captured, evidence reconciled, helper policy accepted, and acceptance status.
- Specify duplicate/out-of-order callback behavior: update terminal signal, then read only unread child turns by cursor, and do not downgrade accepted evidence without a new terminal child update.
- Specify `read_thread` failure behavior: mark `readback_blocked:<reason>` or `pending-readback`, never `accepted`.
- Strengthen the worker-internal helper layer from opportunistic to mandatory for non-trivial Director-created work.
- Reaffirm hooks are not the enforcement mechanism.

Reason:
- This file maps policy to concrete `codex_app` operations.

### 4. Resolve direct-leaf ambiguity in the execution hierarchy
Files:
- `plugins/codex-director/skills/codex-director/references/execution-mode-stack.md`

Changes:
- State that tiny project work still gets a worker brief when it involves repo/docs/code/prod inspection or execution.
- Define direct leaf as worker-internal only.
- State direct leaf cannot authorize Director-inline project work.
- Add readback acceptance to the completion rule.

Reason:
- The hierarchy needs one unambiguous meaning for direct leaf.

### 5. Strengthen worker/helper routing policy
Files:
- `plugins/codex-director/skills/codex-director/references/agent-profiles-and-model-routing.md`

Changes:
- Replace soft wording such as "most non-trivial workers should" with mandatory coordinator behavior for non-trivial Director-created workers.
- Define acceptable helper lanes: research scout, code/context scout, verification helper, critique/review helper, implementation helper, oracle/review lane when required.
- State helper outputs are advisory until the owning worker verifies and reports final evidence, and until the Director reads back and accepts the child thread.

Reason:
- This file controls the mental model for when workers delegate below themselves.

### 6. Align workflow-specific playbooks
Files:
- `plugins/codex-director/skills/codex-director/references/deep-plan-workflow.md`
- `plugins/codex-director/skills/codex-director/references/build-workflow.md`
- `plugins/codex-director/skills/codex-director/references/review-workflow.md`
- `plugins/codex-director/skills/codex-director/references/orchestrate-workflow.md`
- `plugins/codex-director/skills/codex-director/references/investigate-research-workflow.md`
- `plugins/codex-director/skills/codex-director/references/refactor-workflow.md`
- `plugins/codex-director/skills/codex-director/references/optimize-workflow.md`
- `plugins/codex-director/skills/codex-director/references/goals-integration.md`
- `plugins/codex-director/skills/codex-director/references/browser-chatgpt-oracle-workflow.md`

Changes:
- `deep-plan-workflow.md`: require scout/helper lanes and critique/review lanes for non-trivial planning; final plan evidence must state helper/direct-leaf status.
- `build-workflow.md`: require helper/subagent/context/review lanes for non-trivial builds; final evidence must include helper/direct-leaf status.
- `review-workflow.md`: add checks for unread child finals, missing readback state, missing helper/subagent evidence, and invalid direct-leaf rationale.
- `orchestrate-workflow.md`: block item verification and final rollup while any worker is `pending-readback`, `readback_blocked:<reason>`, `insufficient-evidence`, missing helper/direct-leaf acceptance, or lacking cleanup/archive state.
- `investigate-research-workflow.md`, `refactor-workflow.md`, `optimize-workflow.md`, `goals-integration.md`, and `browser-chatgpt-oracle-workflow.md`: scan and align any completion, oracle, helper, or evidence language so they cannot bypass readback/helper gates.

Reason:
- The gates need to survive each common workflow, not just the central reference or the initially observed planning path.

### 7. Define deterministic durable workflow escalation
Files:
- `plugins/codex-director/skills/codex-director/references/dynamic-workflow-integration.md`

Changes:
- State worker outputs become `results/` only after Director readback and reconciliation, not merely after callback.
- Add durable state triggers from the Reliable State Gate.
- Extend completion audit with readback status, captured final report, helper/direct-leaf acceptance, review/oracle status, and cleanup/archive state.

Reason:
- This is the reliable path for span-turn or multi-worker state. It satisfies the user's ledger constraint without inventing a fragile hidden ledger.

### 8. Align public/default prompt surfaces
Files:
- `README.md`
- `plugins/codex-director/.codex-plugin/plugin.json`
- `plugins/codex-director/skills/codex-director/agents/openai.yaml`

Changes:
- Add concise invariant language only where it fits:
  - Director-created workers are accepted only after child-thread readback and evidence reconciliation.
  - Non-trivial Director-created workers use helper/subagent lanes.
  - Direct leaf is worker-internal only for tiny/mechanical/low-risk work.
- Keep the prompt short enough that it does not crowd out existing coordination-only boundaries.
- If the implementation changes the Codex Director plugin version in `plugins/codex-director/.codex-plugin/plugin.json`, also update `/Users/claire/dev/marketplace/.agents/plugins/plugin-versions.json` per `AGENTS.md`.

Reason:
- The first activation surface should not drift from the canonical docs.

### 9. Preserve hook boundary
Files:
- `plugins/codex-director/hooks/README.md`
- `plugins/codex-director/hooks/hooks.json`

Changes:
- Do not add hooks.
- Leave `hooks/hooks.json` empty.
- Touch `hooks/README.md` only if useful to reaffirm that hook scope is too broad for Director-created-thread-only enforcement.

Reason:
- User explicitly rejected hook-based enforcement, and current docs already say hooks are intentionally empty.

## Sequencing
1. Patch `SKILL.md` and `REFERENCE.md` first so the compact and canonical contracts agree.
2. Patch `runtime-adapters.md` next so the readback gate has concrete `codex_app` semantics.
3. Patch `execution-mode-stack.md` and `agent-profiles-and-model-routing.md` to remove helper/direct-leaf ambiguity.
4. Patch workflow-specific references so planning, build, review, and orchestration all enforce the same gates.
5. Patch `dynamic-workflow-integration.md` for reliable durable-state escalation.
6. Patch public/default prompt surfaces last, using concise language copied from the now-canonical docs.
7. Verify `hooks/hooks.json` remains empty and no hook enforcement was introduced.

## Validation Plan
Run these checks after the implementation pass:

```bash
rg -n "callback|read_thread|read_cursor|last_turn_seen|pending-readback|readback_complete|readback_blocked|insufficient-evidence|accepted" plugins/codex-director/skills/codex-director README.md plugins/codex-director/.codex-plugin/plugin.json
rg -n "helper policy|subagent|sub-agent|direct leaf|direct-leaf|tiny|mechanical|low-risk" plugins/codex-director/skills/codex-director README.md plugins/codex-director/.codex-plugin/plugin.json
rg -n "hook|hooks" plugins/codex-director/skills/codex-director README.md plugins/codex-director/hooks plugins/codex-director/.codex-plugin/plugin.json
jq '.hooks' plugins/codex-director/hooks/hooks.json
```

Manual regression checks:
- Callback-only final: a worker sends `callback:final`, but the Director has not called `read_thread`. Expected state is `pending-readback`, not `accepted`.
- Readback failure: `read_thread` is unavailable or returns no terminal child report. Expected state is `readback_blocked:<reason>` or `insufficient-evidence`, not `accepted`.
- Non-trivial planning worker with no helper lanes. Expected outcome is rejected activation or blocked/requested clarification, not accepted completion.
- Tiny direct-leaf worker with clear rationale. Expected outcome can be accepted only after child-thread readback and evidence reconciliation.
- Multi-worker or span-turn task. Expected outcome requires `.workflow/<slug>/` or equivalent explicit durable artifacts with per-worker readback state.
- Resume after Director turn ends. Expected outcome requires recoverable durable transcript state or `.workflow/<slug>/`; otherwise the worker remains `pending-readback` or `readback_blocked:<reason>`.
- Hook boundary. Expected outcome: no hooks added; enforcement lives in prompts, templates, monitoring state, review gates, and workflow artifacts.

## Failure Modes To Guard Against
- Treating a callback payload as final evidence without child-thread readback.
- Marking a worker complete because the Director remembers creating it, but never reading the child.
- Letting a worker final omit whether it used helper/subagent lanes or qualified for direct leaf.
- Treating ordinary tool use, self-checks, or "I considered helpers" as satisfying the helper/subagent gate.
- Letting `direct leaf` become a loophole for Director-inline project inspection or execution.
- Creating a ledger that only works while the current chat context remains intact.
- Adding hook-based checks that affect ordinary non-Director-created threads.
- Updating only `REFERENCE.md` while leaving `SKILL.md` and default prompt surfaces soft.

## Non-goals
- Do not add lifecycle hooks for enforcement.
- Do not implement a global hook runner.
- Do not add runtime code unless a later build pass finds existing code paths that consume these docs/templates.
- Do not treat `docs/investigations/director-thread-operation-2026-06-04.md` as canonical over the current plugin docs.
- Do not make every tiny worker use full `.workflow/<slug>/` ceremony.

## Residual Questions
No blocking question remains. The ledger question is resolved as a conditional rule: visible structured monitor state is sufficient for a single short worker, while `.workflow/<slug>/` is required whenever durable, multi-worker, span-turn, stale/cancel, review/oracle, worktree, approval, or dependency state must survive reliably.

## References
- `plugins/codex-director/skills/codex-director/SKILL.md`
- `plugins/codex-director/skills/codex-director/REFERENCE.md`
- `plugins/codex-director/skills/codex-director/references/runtime-adapters.md`
- `plugins/codex-director/skills/codex-director/references/execution-mode-stack.md`
- `plugins/codex-director/skills/codex-director/references/agent-profiles-and-model-routing.md`
- `plugins/codex-director/skills/codex-director/references/deep-plan-workflow.md`
- `plugins/codex-director/skills/codex-director/references/build-workflow.md`
- `plugins/codex-director/skills/codex-director/references/review-workflow.md`
- `plugins/codex-director/skills/codex-director/references/orchestrate-workflow.md`
- `plugins/codex-director/skills/codex-director/references/investigate-research-workflow.md`
- `plugins/codex-director/skills/codex-director/references/refactor-workflow.md`
- `plugins/codex-director/skills/codex-director/references/optimize-workflow.md`
- `plugins/codex-director/skills/codex-director/references/goals-integration.md`
- `plugins/codex-director/skills/codex-director/references/browser-chatgpt-oracle-workflow.md`
- `plugins/codex-director/skills/codex-director/references/dynamic-workflow-integration.md`
- `plugins/codex-director/hooks/README.md`
- `plugins/codex-director/hooks/hooks.json`
- `README.md`
- `plugins/codex-director/.codex-plugin/plugin.json`
- `plugins/codex-director/skills/codex-director/agents/openai.yaml`
- `docs/investigations/director-thread-operation-2026-06-04.md`
