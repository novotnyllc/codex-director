# Codex Director

A Codex plugin containing a project-scoped director skill. It defines a pinned coordinating Codex thread that routes work, creates and monitors worker threads, invokes task-level dynamic workflows when warranted, and uses research, oracle, review, git/worktree, and evidence gates to keep complex work coherent.

## Install

Install from GitHub:

```bash
codex plugin marketplace add novotnyllc/codex-director
codex plugin add codex-director --marketplace codex-director
```

## Use

After installing, open Codex in the project you want the Director to own. The project can be a single repo, a multi-repo workspace, or a plain working folder.

Start a new Codex thread and send a setup prompt like:

```text
Start $codex-director for this project.
Use this thread as the Director thread. Read the project instructions, identify the project scope, set up the Director operating brief, and tell me what you need from me before coordinating work.
```

`$codex-director` is a Codex skill mention, not a terminal command. Use it explicitly when setting up the Director or when you want to force the skill to activate. After the Director thread is established, keep using that same thread for project-level requests:

```text
Coordinate the Discord invite work and use dynamic workflow if the task needs packets.
```

```text
Review worker progress, reconcile completed work, and tell me what is blocked.
```

```text
Plan the next implementation slice, run research and adversarial review first, then dispatch worker threads where useful.
```

For a multi-repo workspace, name the scope directly:

```text
Start $codex-director for this workspace. Treat admin/, website/, and ops/ as separate child repos under one project scope.
```

If Codex can manage threads in the current runtime, the Director should title and pin the thread. If not, manually name the thread `Director: <project>` and keep using it as the coordination home.

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
