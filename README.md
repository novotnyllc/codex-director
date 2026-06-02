# Codex Project Chief of Staff

A Codex plugin containing a project-scoped chief-of-staff skill. It defines a pinned coordinating Codex thread that routes work, creates and monitors worker threads, invokes task-level dynamic workflows when warranted, and uses research, oracle, review, git/worktree, and evidence gates to keep complex work coherent.

## Install

Install from GitHub:

```bash
codex plugin marketplace add novotnyllc/codex-project-chief-of-staff-skill --ref main
codex plugin add codex-project-chief-of-staff --marketplace codex-project-chief-of-staff
```

For local development from a checkout:

```bash
codex plugin marketplace add /Users/claire/dev/codex-project-chief-of-staff-skill
codex plugin add codex-project-chief-of-staff --marketplace codex-project-chief-of-staff
```

## Structure

- `.agents/plugins/marketplace.json` declares this repository as a Codex plugin marketplace.
- `plugins/codex-project-chief-of-staff/.codex-plugin/plugin.json` is the plugin manifest.
- `plugins/codex-project-chief-of-staff/skills/codex-project-chief-of-staff/SKILL.md` is the compact entrypoint Codex reads when selecting the skill.
- `plugins/codex-project-chief-of-staff/skills/codex-project-chief-of-staff/REFERENCE.md` contains the full operating brief, worker templates, evidence rules, and status formats.
- `plugins/codex-project-chief-of-staff/skills/codex-project-chief-of-staff/references/` contains workflow playbooks for build, review, research, dynamic workflow integration, Browser ChatGPT oracle, and related execution modes.
- `plugins/codex-project-chief-of-staff/skills/codex-project-chief-of-staff/agents/` contains optional model/profile guidance that travels with the skill.

## Operating Model

```text
Chief-of-staff Codex thread
  -> Codex worker threads
      -> selected self-contained workflow / dynamic workflow packet / optional tool implementation
          -> research, oracle, review, and verification gates
```

The skill is intentionally project-scoped: the project can be a single repo, a multi-repo workspace, or a projectless working directory.
