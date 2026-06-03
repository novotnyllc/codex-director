# Director Hooks

Codex Director bundles scoped advisory hooks through `hooks/hooks.json`.

These hooks remind Director-marked threads about role boundaries and closeout hygiene. They keep runtime nudges close to the hook implementation while the skill docs define the Director workflow itself.

## Files

- `hooks.json`: Codex hook registration.
- `director-hook.py`: scoped hook runner.

## Events

| Event | Purpose |
|---|---|
| `SessionStart` | Restore the role boundary on Director-marked starts and compact resumes |
| `UserPromptSubmit` | Re-check routing before handling a Director-marked instruction |
| `Stop` | Emit a structured closeout warning for Director-marked turns |
| `SubagentStart` | Remind Director-marked nested helpers they are scoped under an owning worker or packet |
| `SubagentStop` | Emit a structured warning to roll helper evidence back to the owning worker or packet |

The bundled hooks intentionally omit `PostCompact`. Plain `PostCompact` stdout is not model-visible, so compaction reminders use the `SessionStart` hook when Codex starts from `compact` and the transcript is Director-marked.

## Scoping

The runner emits output only when the submitted prompt or recent transcript contains a Director marker such as `$codex-director`, `codex-director`, `Codex Director`, or `Director thread`.

- `SessionStart`, `UserPromptSubmit`, and `SubagentStart` emit structured `additionalContext`.
- `Stop` and `SubagentStop` emit structured `systemMessage` only; they do not block or force continuation.
- Unmarked threads receive no hook output.

Do not use Director hooks to block ordinary worker tools or routine turn completion. Rely on worker briefs, activation reports, monitoring, review gates, and ledger state for enforcement.

## Trust

Codex lists configured hooks through `/hooks`. New or changed non-managed hooks require review and trust before they run. Plugin-bundled hooks load alongside other hook sources and use the same trust-review flow.

A runtime policy that disables hooks is a reduced reminder surface, not a blocker by itself. The Director contract does not change: project work still belongs in Codex worker threads.
