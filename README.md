# Codex Director

A Codex plugin containing a project-scoped director skill. It defines a pinned coordinating Codex thread that routes work, creates and monitors worker threads, invokes task-level dynamic workflows when warranted, and uses research, oracle, review, git/worktree, and evidence gates to keep complex work coherent.

## Install

Install from GitHub:

```bash
codex plugin marketplace add novotnyllc/codex-director
codex plugin add codex-director --marketplace codex-director
```

## Structure

- `.agents/plugins/marketplace.json` declares this repository as a Codex plugin marketplace.
- `plugins/codex-director/.codex-plugin/plugin.json` is the plugin manifest.
- `plugins/codex-director/skills/codex-director/SKILL.md` is the compact entrypoint Codex reads when selecting the skill.
- `plugins/codex-director/skills/codex-director/REFERENCE.md` contains the full operating brief, worker templates, evidence rules, and status formats.
- `plugins/codex-director/skills/codex-director/references/` contains workflow playbooks for build, review, research, dynamic workflow integration, Browser ChatGPT oracle, and related execution modes.
- `plugins/codex-director/skills/codex-director/agents/` contains optional model/profile guidance that travels with the skill.

## Operating Model

```text
Director Codex thread
  -> Codex worker threads
      -> selected self-contained workflow / dynamic workflow packet / optional tool implementation
          -> research, oracle, review, and verification gates
```

The skill is intentionally project-scoped: the project can be a single repo, a multi-repo workspace, or a projectless working directory.
