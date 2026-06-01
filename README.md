# Codex Project Chief of Staff Skill

Project-scoped chief-of-staff workflow for Codex. It defines a pinned coordinating Codex thread that routes work, creates and monitors worker threads, invokes task-level dynamic workflows when warranted, and uses research, oracle, review, git/worktree, and evidence gates to keep complex work coherent.

## Install

Use this repository as the skill directory:

```bash
ln -s "$PWD" ~/.agents/skills/codex-project-chief-of-staff
```

If a skill directory already exists at that path, replace it intentionally after checking for local changes.

## Structure

- `SKILL.md` is the compact entrypoint Codex reads when selecting the skill.
- `REFERENCE.md` contains the full operating brief, worker templates, evidence rules, and status formats.
- `references/` contains workflow playbooks for build, review, research, dynamic workflow integration, Browser ChatGPT oracle, and related execution modes.

## Operating Model

```text
Chief-of-staff Codex thread
  -> Codex worker threads
      -> selected self-contained workflow / dynamic workflow packet / optional tool implementation
          -> research, oracle, review, and verification gates
```

The skill is intentionally project-scoped: the project can be a single repo, a multi-repo workspace, or a projectless working directory.
