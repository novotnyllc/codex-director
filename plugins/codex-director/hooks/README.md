# Director Hook Reference

Codex Director does not register plugin-bundled lifecycle hooks. `hooks/hooks.json` is intentionally empty so installs do not attach Director behavior to every Codex thread.

No hook runner is shipped or retained. Hook support is absent unless Codex exposes real thread-attached metadata or another explicit per-thread binding surface and a future implementation is added.

## Files

- `hooks.json`: empty Codex hook configuration. No events or commands are registered.

## Registration

No hook events are registered. The plugin does not install `SessionStart`, `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`, or `PostCompact` commands.

Do not use marker strings, prompt scanning, or transcript scanning to infer Director scope. Director identity and routing come from explicit thread setup, project scope, worker launch contracts, and ledger state.

## Future Hook Requirements

Hook support can be reconsidered only when the runtime exposes a reliable way to bind hooks to a specific Director thread or explicit per-thread metadata.

Any future hook design must be opt-in or thread-attached, avoid global behavior for ordinary Codex threads, and avoid marker, string, or transcript detection as the primary scope mechanism.

Until then, rely on worker briefs, activation reports, monitoring, review gates, ledger state, and workflow artifacts for Director-scoped enforcement and reminders, including child-thread readback, evidence reconciliation, and helper/direct-leaf policy.

## Trust

Codex lists configured hooks through `/hooks`. Because `hooks/hooks.json` is empty, Codex Director should not appear as a configured hook provider after install.

A runtime policy that disables hooks is not a reduced Director surface. The Director contract is independent of hooks: project work still belongs in Codex worker threads.
