# Director Regression Checklist

Use this checklist when changing Director routing, monitoring, workflow-skill activation, model/thinking defaults, or thread-title behavior. It captures failure patterns observed in long-running Director sessions such as `019e9e8f-cadf-74f3-af42-26b7d69c1f47`.

## Required Checks

1. Runtime identity is recorded.
   - Director setup, resume, heartbeat, and callback turns record plugin version and loaded skill/cache path when visible.
   - If the loaded path/version is older than the expected release, the ledger records `stale-director-runtime:<version-or-path>`.
   - Existing threads are not assumed to reload a newer plugin version unless the loaded path/version proves it.

2. Parent Director effort does not silently downgrade.
   - Director-owned continuations, heartbeats, and worker callbacks into the Director pass `thinking: "xhigh"` when thinking selection is exposed.
   - If the active Director turn is known to be below `xhigh`, it only performs safety bookkeeping: title repair, readback, pending-worktree pickup, monitor recovery, or blocker reporting.
   - A downgraded Director turn records `director-effort-blocked:<effort>` before any planning, dispatch, steering, acceptance, or completion verdict.

3. Parent title is stable and proven.
   - Plugin-link-only `[@codex-director](plugin://codex-director@novotnyllc)`, `$codex-director:codex-director`, plugin/default starter prompts, and plain Director requests all load the main Director skill before ready/loaded prose.
   - A bare plugin-link-only invocation that answers only "Codex Director is available" or asks for the objective before title/pin setup fails this regression.
   - Plugin manifest `defaultPrompt` entries are treated as composer starter prompts, not enforcement instructions; user-visible descriptions remain product copy aligned with startup behavior, and the main Director skill keeps `policy.allow_implicit_invocation: true` for plugin-link and plain-language fallbacks.
   - On a bare invocation with no objective, the Director performs setup before asking for the objective.
   - The stable title is `<Project Display Name> Director`, with workspace title emoji convention when available.
   - The Director calls `codex_app.set_thread_title` when exposed and records `parent-title: verified`, `parent-title: repaired:<old-title>`, or `parent-title-blocked:<reason>`.
   - The Director calls `codex_app.set_thread_pinned` with `pinned: true` when exposed and records `parent-pin: pinned`, `parent-pin-blocked:<reason>`, or `pin-unavailable`.
   - Worker titles, queued worktree focus, local task-title rules, and auto-title updates do not become the parent title.
   - Before checkpoint/final output, the ledger records title and pin status.

4. Workflow skills are hard activation surfaces.
   - Worker briefs say `Invoke $codex-director:director-build` or the exact matching workflow skill, never "if available".
   - Worker activation reports `workflow-skill-loaded:<exact $codex-director:director-* skill>` before substantive work.
   - Failure to load a shipped workflow skill is recorded as `workflow-skill-load-failed:<exact $codex-director:director-* skill>:<stale-runtime|broken-install|wrong-plugin-context|reason>` and blocks work until corrected or relaunched.

5. Pending worktree handles remain monitored.
   - A `pendingWorktreeId` is recorded as an active handle before any final-looking user status.
   - Pickup state includes pending id, lookup query or matching strategy, owning task, next wake mechanism/time, pickup success condition, and stale threshold.
   - The only monitor is not cleared while pending worktree ids, queued workers, or running workers remain active.
   - If monitor creation/update fails, the ledger records and surfaces `monitor_blocked:<reason>`.

6. Callback text is never enough.
   - Callback, expected final text, stale summary, and worker claims are terminal signals only.
   - The Director calls `codex_app.read_thread` and captures the terminal child report before acceptance.
   - Acceptance reconciles done criteria, evidence, review/oracle status, helper/direct-leaf policy, cleanup/archive state, and coordinator continuation state.

7. Coordinator checkpoints continue the workflow.
   - Coordinator-only output is accepted only as checkpoint evidence.
   - The parent then records `next-packet-dispatched`, `monitor-scheduled`, `blocked-on-dispatch:<reason>`, or `awaiting-approval:<reason>`.
   - A final checkpoint with recommended briefs is not task completion.

8. Native helper tooling stays worker-internal.
   - The Director parent still creates only durable Codex worker threads through the exposed `codex_app` contract.
   - Worker briefs require native helper runtime surface reporting: `available:<tools>`, `namespaced:<namespace>`, `v1-only`, `unavailable:<reason>`, or `ambiguous:<reason>`.
   - When V2 helpers are used, worker evidence records RP-style profile (`explore`, `pair`, `engineer`, or `design`), model/thinking/fork rationale when exposed, helper task paths, owner spot-check evidence, and `close_agent` or `close_blocked:<reason>`.
   - `wait_agent`, `list_agents`, helper final-status notifications, and unread helper prose are not accepted as evidence.

## Evidence To Capture

For each regression pass, record:

- plugin version and loaded skill path checked
- parent title status before and after worker creation/title changes
- parent pin status after plugin/default starter invocation
- Director thinking/effort setting used for parent continuations
- one worker brief showing exact `$codex-director:director-*` invocation
- one worker activation showing `workflow-skill-loaded:<exact $codex-director:director-* skill>`
- one worker activation/evidence record showing native helper runtime surface and, when used, V2 helper profile/evidence/cleanup
- one pending-worktree or monitor ledger row when applicable
- one child-thread readback acceptance record
