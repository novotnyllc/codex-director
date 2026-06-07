# Director Multi-Agent V2 Adoption: Plan

## Goal
Update the Codex Director plugin so Director-created worker threads can use Codex `multi_agent_v2` as a worker-internal helper layer when the active runtime exposes it.

The Director itself still creates durable Codex threads for top-level work. This plan is about what those threads do after dispatch: how they detect V2 tools, use V2 helper agents for scouting/review/verification/decomposition, roll up helper evidence, and report back through the existing Director readback and evidence gates.

## User Decisions
- The Director should still only create durable Codex threads for top-level delegated work.
- `multi_agent_v2` belongs inside those created worker threads as an optional helper/subagent lane, not as a replacement for Director-managed worker threads.
- Director completion semantics do not change: the Director accepts work only after reading the owning worker thread and reconciling terminal evidence.

## Background
- Local `/Users/claire/dev/codex` is clean on `main` and aligned with upstream `openai/codex/main` at `e093d819826127be01354e2885c86d7fcbfb2897`; the upstream commits page shows `e093d81` as the latest `main` commit on June 7, 2026.
- Upstream `openai/codex` contains `codex-rs/core/src/tools/handlers/multi_agents_v2/` on `main`, including `close_agent.rs`, `followup_task.rs`, `list_agents.rs`, `message_tool.rs`, `send_message.rs`, `spawn.rs`, and `wait.rs`.
- `multi_agent_v2` is task-path-based and still under development/default-disabled: `codex-rs/features/src/lib.rs:137-139` and `codex-rs/features/src/lib.rs:963-967`.
- V2 config includes concurrency, wait timeout, usage hint, namespace, metadata hiding, and non-code-mode-only controls: `codex-rs/features/src/feature_configs.rs:27-58` and `codex-rs/core/src/config/mod.rs:1043-1076`.
- V2 exposes `spawn_agent`, `send_message`, `followup_task`, `wait_agent`, `close_agent`, and `list_agents` when selected: `codex-rs/core/src/tools/spec_plan.rs:696-748`.
- `spawn_agent` V2 requires `task_name` and `message`: `codex-rs/core/src/tools/handlers/multi_agents_spec.rs:82-129`. `wait_agent` is a mailbox-update wait, not final content: `codex-rs/core/src/tools/handlers/multi_agents_spec.rs:248-259`.
- V2 children use canonical paths rooted at `/root`: `codex-rs/protocol/src/agent_path.rs:15-66`. Child completion routes to the direct parent as inter-agent communication with `trigger_turn=false`: `codex-rs/core/src/agent/control.rs:407-434`.
- Current Director docs use `codex_app` thread lifecycle for top-level workers: `plugins/codex-director/skills/codex-director/references/runtime-adapters.md:77-96`. Completion still requires `codex_app.read_thread`, terminal report capture, evidence reconciliation, helper/direct-leaf acceptance, archive state, and title/pin state: `plugins/codex-director/skills/codex-director/REFERENCE.md:316-339`.
- Current Director worker launch already requires helper/subagent lanes for non-trivial workers: `plugins/codex-director/skills/codex-director/SKILL.md:69-90`.
- The plugin ships split workflow skills as activation surfaces: `$director-orchestrate`, `$director-build`, `$director-review`, `$director-investigate`, `$director-deep-plan`, `$director-refactor`, `$director-optimize`, `$director-dynamic-workflow`, and `$director-browser-oracle`: `plugins/codex-director/skills/codex-director/SKILL.md:14` and `plugins/codex-director/skills/codex-director/SKILL.md:98-99`.
- Those split skills already contain helper/subagent activation and evidence language, so implementation must patch their `SKILL.md` files directly, not only the shared reference playbooks.
- The RP skills are role-specific delegation playbooks, not just generic "use subagents" guidance. They map work to `explore` scouts, `pair` deep/default helpers, `engineer` bounded execution helpers, and `design` critique/report helpers, with explicit detach/wait/poll/cleanup behavior.
- RP delegation briefs also carry model/thinking/forking implications: narrow read-only scouts use low/medium effort and minimal context; complex synthesis defaults to pair/latest-main/high; risky/final authority escalates to xhigh; clear implementation uses engineer/latest-main/high; mechanical low-risk helper work may use Spark/medium when the active schema exposes that choice.
- RP workflow detail is operational: briefs name scope, leave-alone areas, plan/export paths, sibling lanes, expected output, evidence standard, and cleanup; detached fan-out must be followed by wait/poll; completed sessions are cleaned up after evidence is recorded.
- RP build/review/export workflows also enforce context discipline: use context-building/review surfaces for broad work, avoid extended manual reading before delegation, do not ask oracle/export lanes to do implementation, and trust generated exports unless there is a concrete coverage issue.
- Before this adoption work, the plugin had no references to `multi_agent_v2`, `multi_agents_v2`, `spawn_agent`, `wait_agent`, `followup_task`, `list_agents`, or `close_agent`.
- Hook enforcement remains out of scope: `plugins/codex-director/hooks/README.md:1-23`.

## Approach
Keep a two-layer model and make it explicit everywhere the plugin discusses workers, helpers, evidence, and workflow packets:

```text
Director thread
  -> durable top-level Codex worker threads via codex_app
      -> optional worker-internal multi_agent_v2 helper agents
```

The Director parent may route, brief, create, steer, monitor, read back, reconcile, and archive top-level worker threads. It should not use `spawn_agent`, `followup_task`, `wait_agent`, `list_agents`, or `close_agent` as its own substitute for project workers. The created worker thread may use those V2 tools internally when the active tool schema exposes them.

Use V2 helpers inside a worker when all are true:

- the owning durable worker thread already exists;
- the worker's active tool schema exposes V2 or equivalent native helper tools;
- the subtask is helper-shaped: scout, context map, critique, verification, narrow review, or bounded disjoint subwork;
- the owning worker can spot-check the helper claim against the cited file, command, artifact, or transcript evidence before it appears in terminal evidence;
- the owning worker can close completed helper agents or record a close blocker after a real close attempt.

Use a separate Director-created `codex_app` worker thread when the work needs a saved project target, repo/path ownership, worktree or branch lifecycle, callback/readback/archival state, dynamic workflow packet ownership, multi-turn resumability, or user-visible terminal evidence.

Map RP role semantics to V2 helpers inside the owning worker:

| RP role | V2 use | Default routing |
| --- | --- | --- |
| `explore` | one-question scouts for code, docs, git, tests, prior art, or current external facts | Spark or latest-main at low/medium; prefer minimal forked context |
| `pair` | complex/default helper for ambiguous synthesis, root cause, baseline loops, or reconciliation | latest-main/high; xhigh when the helper may affect final authority |
| `engineer` | clear bounded implementation/refactor/helper slice after the plan is known | latest-main/high; Spark/medium only for mechanical low-risk work |
| `design` | bounded critique, plan review, UX/copy/design review, or report lane | latest-main/high or xhigh for high-impact critique |

This avoids two failure modes: treating V2 helpers as durable Director workers, and treating `wait_agent`/mailbox notifications as accepted evidence. V2 helper output is only candidate evidence until the owning worker spot-checks it and returns a terminal report; that terminal report is still accepted only through Director `codex_app.read_thread` readback. If any V2 helper is still running, unread, or unsummarized, the owning worker is not ready for accepted final evidence. A terminal report may include `close_blocked:<reason>` only after helper evidence has been consumed, no helper work remains active, and the worker attempted cleanup.

## Work Items
1. **Patch the compact Director contract.**

   Files:
   - `plugins/codex-director/skills/codex-director/SKILL.md`

   Changes:
   - Add the two-layer rule near the worker lifecycle boundary: Director creates durable top-level Codex worker threads; `multi_agent_v2` is optional worker-internal helper tooling.
   - Add a hard parent-thread prohibition: the Director must not replace a top-level worker launch with `spawn_agent` or other V2 helper tools.
   - Extend Worker Launch Minimum with `native helper runtime surface` and `V2 helper policy` fields.
   - Extend Monitoring And Evidence with: `wait_agent`, `list_agents`, and V2 final notifications are not accepted evidence; only the owning worker's terminal report, read by the Director, can satisfy completion.

2. **Add the canonical V2 helper lane to the reference.**

   Files:
   - `plugins/codex-director/skills/codex-director/REFERENCE.md`

   Changes:
   - Add a `Native multi_agent_v2 helper lane` section.
   - Define V2 as worker-internal only, feature/schema-detected, and default-fallback safe.
   - Update the worker brief template with helper-runtime detection, V2 task-path policy, `fork_turns` choice, and closure expectations.
   - Update the activation report with `multi_agent_v2 surface` and `V2 helper plan`.
   - Update the evidence contract so any worker that used V2 reports helper path, purpose, status, evidence received, owner verification, and closure/close blocker.
   - Add anti-patterns for Director-parent V2 use, accepting `wait_agent` as content, accepting unverified helper output, leaving helpers open, and treating V2 helpers as packet owners.

3. **Update runtime adapter guidance with exact V2 semantics first.**

   Files:
   - `plugins/codex-director/skills/codex-director/references/runtime-adapters.md`

   Changes:
   - Add `Optional multi_agent_v2 helper tooling` under the worker-internal helper layer. This is the canonical detection and semantics section; compact docs and playbooks should point here instead of repeating the full rule.
   - Include a recognition table for `spawn_agent`, `send_message`, `followup_task`, `wait_agent`, `list_agents`, and `close_agent`, including namespaced-tool handling. Detection is from the worker's active tool schema, not from local config assumptions.
   - Define `unavailable` as no V2-shaped helper tools exposed, `v1-only` as only legacy collaboration/helper tooling exposed, and `ambiguous:<reason>` as partial or conflicting schema evidence such as missing `task_name`, renamed wait/follow-up tools, or namespace uncertainty.
   - Document `/root` task-path naming, `task_name` constraints, and suggested names such as `context_scout`, `plan_critique`, and `verify_tests`.
   - Specify `fork_turns`: prefer `none` for self-contained helper prompts, a small number when recent worker context matters, and `all` only when inherited context is genuinely needed.
   - Clarify `send_message` queues context, `followup_task` wakes a child turn, `wait_agent` is only a mailbox wake signal, and `close_agent` is part of cleanup/concurrency hygiene.
   - Add fallback states: `multi_agent_v2 surface: unavailable | available:<tools> | namespaced:<namespace> | v1-only | ambiguous:<reason>` and `v2 helper policy: not-needed | planned:<lanes> | used:<paths> | unavailable:<reason> | failed:<reason>`.

4. **Align the execution stack and dynamic workflow model.**

   Files:
   - `plugins/codex-director/skills/codex-director/references/execution-mode-stack.md`
   - `plugins/codex-director/skills/codex-director/references/dynamic-workflow-integration.md`

   Changes:
   - Show V2 below the owning worker thread, not beside the Director worker thread layer.
   - State that dynamic workflow packets are still owned by durable Director-created worker threads.
   - State that V2 helper outputs become `results/` only through owning worker terminal evidence plus Director readback/reconciliation.
   - Keep packet ownership, approvals, parent workflow criteria, and integration records out of V2 helpers.

5. **Patch every shipped worker skill activation surface.**

   Files:
   - `plugins/codex-director/skills/director-orchestrate/SKILL.md`
   - `plugins/codex-director/skills/director-build/SKILL.md`
   - `plugins/codex-director/skills/director-review/SKILL.md`
   - `plugins/codex-director/skills/director-investigate/SKILL.md`
   - `plugins/codex-director/skills/director-deep-plan/SKILL.md`
   - `plugins/codex-director/skills/director-refactor/SKILL.md`
   - `plugins/codex-director/skills/director-optimize/SKILL.md`
   - `plugins/codex-director/skills/director-dynamic-workflow/SKILL.md`
   - `plugins/codex-director/skills/director-browser-oracle/SKILL.md`
   - matching `plugins/codex-director/skills/director-*/agents/openai.yaml` files where they restate activation or final-evidence policy.

   Changes:
   - Add a compact activation rule to each split skill: report the native helper runtime surface and use V2 only as worker-internal helper tooling when exposed.
   - Update helper/subagent lane language in each split skill so V2 can satisfy the helper lane only when helper evidence is read, spot-checked, summarized by the owning worker, and closed or recorded with an acceptable close blocker.
   - Preserve lane-specific boundaries: build/refactor/optimize still own edits and verification, investigate remains read-only, review remains adversarial, deep-plan remains plan-only, dynamic-workflow owns packet artifacts, orchestrate owns worker-internal decomposition, and browser-oracle remains Director-delegated oracle work rather than a generic V2 helper.
   - Add final-evidence fields where missing: `multi_agent_v2 surface`, `V2 helper paths`, `owner verification`, and `helper cleanup`.
   - Keep the wording short in `agents/openai.yaml`; those files should point workers toward the canonical runtime adapter semantics rather than copy the full V2 tool table.

6. **Teach shared worker playbooks how to use V2 helpers without copying the full spec.**

   Files:
   - `plugins/codex-director/skills/codex-director/references/orchestrate-workflow.md`
   - `plugins/codex-director/skills/codex-director/references/build-workflow.md`
   - `plugins/codex-director/skills/codex-director/references/review-workflow.md`
   - `plugins/codex-director/skills/codex-director/references/deep-plan-workflow.md`
   - `plugins/codex-director/skills/codex-director/references/investigate-research-workflow.md`
   - `plugins/codex-director/skills/codex-director/references/refactor-workflow.md`
   - `plugins/codex-director/skills/codex-director/references/optimize-workflow.md`
   - `plugins/codex-director/skills/codex-director/references/browser-chatgpt-oracle-workflow.md`
   - `plugins/codex-director/skills/codex-director/references/goals-integration.md`
   - `plugins/codex-director/skills/codex-director/references/director-regression-checklist.md`

   Changes:
   - Add at most one pointer from each existing helper/scout/review/final-evidence section to the runtime adapter V2 section.
   - For orchestrate/build/deep-plan/investigate, allow V2 helpers for context scouts, file/test mapping, independent verification, and critique lanes only where the playbook already has helper-lane language.
   - For review, add checks that V2 helper claims include evidence, owner verification, and close status.
   - For browser-oracle, clarify that V2 helpers may support local fallback/review work inside a worker, but must not bypass Director-mediated privacy approval or oracle routing.
   - For goals/regression checklist, add only acceptance-gate checks: Director still creates threads; V2 is worker-internal; no `wait_agent`-as-evidence; helpers closed or blocker recorded.
   - Skip refactor/optimize if there is no existing helper/final-evidence section to patch.

7. **Update model/helper routing guidance with RP-to-V2 role mapping.**

   Files:
   - `plugins/codex-director/skills/codex-director/references/agent-profiles-and-model-routing.md`

   Changes:
   - Add a role table that maps Director profiles and RP role labels to native V2 helper shapes.
   - Capture model/thinking/fork guidance for `explore`, `pair`, `engineer`, and `design`.
   - Keep final authority with the owning worker or the Director/oracle/review gate, not the V2 child.
   - Avoid duplicating the runtime adapter tool table; model routing owns role/model choice while `runtime-adapters.md` owns concrete V2 lifecycle semantics.

8. **Update public/default prompt surfaces only where needed.**

   Files:
   - `plugins/codex-director/skills/codex-director/agents/openai.yaml`
   - `plugins/codex-director/.codex-plugin/plugin.json`
   - `README.md`

   Changes:
   - Add one concise invariant to default prompt surfaces if they mention helper/subagent lanes: Director creates durable worker threads; workers may use active-schema native helper/subagent tooling such as `multi_agent_v2` internally when exposed.
   - Preserve current child-thread readback/evidence wording.
   - Do not make V2 user-facing in README unless the current README already describes worker internals in that section.
   - Do not bump `plugin.json` for reference-doc-only changes. If implementation edits `plugin.json` metadata/defaultPrompt for a release, bump the patch version and update `/Users/claire/dev/marketplace/.agents/plugins/plugin-versions.json` per repo instructions before committing/pushing.

9. **Leave hooks empty.**

   Files:
   - `plugins/codex-director/hooks/hooks.json`
   - `plugins/codex-director/hooks/README.md`

   Changes:
   - Do not add hook enforcement.
   - Optionally add one sentence that V2 helper enforcement belongs in briefs, activation reports, ledgers, workflow artifacts, and review/readback gates, not hooks.
   - Verify `hooks/hooks.json` remains empty.

## Validation
Run these checks after implementation:

```bash
rg -n "multi_agent_v2|spawn_agent|wait_agent|followup_task|list_agents|close_agent|/root" plugins/codex-director README.md docs/plans
rg -n "native helper runtime surface|V2 helper|helper cleanup|owner verification" plugins/codex-director/skills/*/SKILL.md plugins/codex-director/skills/*/agents/openai.yaml
rg -n "codex_app.create_thread|codex_app.read_thread|pending-readback|readback_complete|helper_policy_accepted" plugins/codex-director/skills/codex-director
rg -n "Director.*spawn_agent|spawn_agent.*Director|wait_agent.*accepted|wait_agent.*final" plugins/codex-director README.md docs/plans
python3 -m json.tool plugins/codex-director/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/codex-director/hooks/hooks.json >/dev/null
```

Manual acceptance scenarios:

- **V2 unavailable:** a worker records `multi_agent_v2 surface: unavailable` and either uses existing helper lanes, reports a direct-leaf rationale for tiny/mechanical/low-risk work, or blocks.
- **V2 available:** a worker spawns a helper, records its canonical path, consumes evidence, verifies it, closes the helper, and includes the rollup in terminal evidence.
- **Mailbox-only wait:** `wait_agent` returns a mailbox/status update and the worker does not treat that as final content.
- **Durable project work:** Director still creates a top-level `codex_app` worker thread, even if the Director parent has V2 tools exposed.
- **Dynamic workflow packet:** V2 helper output remains candidate evidence until the owning packet worker reports terminal evidence and the Director reads/reconciles that worker.
- **Callback-only final:** owning-worker callbacks remain wake signals only until `codex_app.read_thread` readback.

## Open Questions
None blocking. The implementation-order choices are resolved in this plan: put canonical runtime detection in `runtime-adapters.md` first, patch the split `director-*` skill activation surfaces before broad shared-playbook edits, permit `close_blocked:<reason>` only after evidence is consumed and no helper work remains active, and avoid a plugin version bump unless implementation changes public plugin metadata/default prompts.

## References
- https://github.com/openai/codex/commits/main/
- https://github.com/openai/codex/tree/main/codex-rs/core/src/tools/handlers/multi_agents_v2
- https://github.com/openai/codex/releases
- `docs/plans/director-worker-readback-and-helper-enforcement-2026-06-05.md`
- `plugins/codex-director/skills/codex-director/SKILL.md`
- `plugins/codex-director/skills/codex-director/REFERENCE.md`
- `plugins/codex-director/skills/codex-director/references/runtime-adapters.md`
- `plugins/codex-director/skills/codex-director/references/dynamic-workflow-integration.md`
- `/Users/claire/.agents/skills/rp-orchestrate/SKILL.md`
- `/Users/claire/.agents/skills/rp-build/SKILL.md`
- `/Users/claire/.agents/skills/rp-deep-plan/SKILL.md`
- `/Users/claire/.agents/skills/rp-investigate/SKILL.md`
- `/Users/claire/.agents/skills/rp-refactor/SKILL.md`
- `/Users/claire/.agents/skills/rp-optimize/SKILL.md`
- `/Users/claire/.agents/skills/rp-review/SKILL.md`
- `/Users/claire/.agents/skills/rp-oracle-export/SKILL.md`
- `/Users/claire/.agents/skills/rp-reminder/SKILL.md`
