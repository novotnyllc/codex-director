# Director Multi-Agent V2 Adoption Plan: Critique

## 1. Top 3 under-specified seams

1. **Runtime-surface detection is named, not operationalized.** The plan adds `multi_agent_v2 surface` / `V2 helper plan` fields and fallback states, but does not say exactly what the worker inspects, how namespaced tools are recognized, or what counts as `ambiguous` vs `unavailable` (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:69-85`). This matters because the existing adapter rule says the active `codex_app` schema is the contract (`plugins/codex-director/skills/codex-director/references/runtime-adapters.md:60`). Clarify this once in `runtime-adapters.md`; do not repeat it across playbooks.

2. **Evidence promotion from V2 helper to Director acceptance is still fuzzy.** The plan correctly says helper output is candidate evidence until owner verification and Director readback (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:40-44`), but the proposed fields do not define the minimum acceptable owner verification step (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:69-72`). Existing acceptance already requires readback and helper/subagent reconciliation (`plugins/codex-director/skills/codex-director/REFERENCE.md:316-344`) plus helper lane evidence (`plugins/codex-director/skills/codex-director/REFERENCE.md:348-349`). Add one precise rule: helper claims must be spot-checked by the owning worker before appearing in terminal evidence.

3. **Helper cleanup and blocked-close semantics need a cutoff rule.** The plan says workers can close helpers or record a close blocker (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:38-39`) and mentions `close_agent` hygiene (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:84`), but not what happens if a helper is still running when the owning worker is ready to final/block. Define whether terminal evidence may be accepted with `close_blocked:<reason>`, and whether open helpers must be cancelled, summarized as stale, or left for no more than one follow-up wait.

## 2. Contradictions or missing dependencies

- `Open Questions: None` is too strong (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:170-171`). The detection, cleanup, and minimum verification questions above can change implementation order.
- Work item 7 touches `plugin.json` and README/public surfaces (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:126-135`). If `plugin.json` version changes, the marketplace version file dependency from `AGENTS.md:3` applies; if this is not a release, say not to bump the version.
- The plan says hook enforcement is out of scope (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:139-148`), but validation searches include broad prompt/docs strings. Keep validation informational; do not turn grep results into hook-like enforcement.

## 3. Risk of over-planning: cut or simplify

- **Work item 5** patches seven workflow playbooks (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:99-114`). Cut this to one pointer from each existing helper/evidence section, or skip playbooks without an existing helper section.
- **Work item 6** duplicates role routing already covered by helper policy and runtime adapter semantics (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:116-123`). Prefer a short cross-reference unless model routing currently conflicts.
- **Work item 7** should be one invariant only (`docs/plans/director-multi-agent-v2-adoption-2026-06-07.md:126-134`). Avoid making V2 user-facing in README unless the current README already describes worker internals.

## 4. Questions whose answers would change implementation order

1. Should runtime-surface detection be implemented first in `runtime-adapters.md`, then referenced elsewhere, or should the compact `SKILL.md` own the canonical policy?
2. Is `close_blocked:<reason>` acceptable terminal evidence, or must workers always resolve/close V2 helpers before final status?
3. Is this a release/version bump, or docs-only adoption guidance with no `plugin.json` version change?
