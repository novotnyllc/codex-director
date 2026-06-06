# Codex Director

A Codex plugin containing a project-scoped director skill. It defines a pinned coordinating Codex thread that routes work, creates and monitors worker threads, invokes task-level dynamic workflows when warranted, and uses research, oracle, review, git/worktree, and evidence gates to keep complex work coherent.

## Install

Install from GitHub:

```bash
codex plugin marketplace add novotnyllc/marketplace
codex plugin add codex-director --marketplace novotnyllc
```

## Use

After installing, open Codex in the project you want the Director to own. The project can be a single repo, a multi-repo workspace, or a plain working folder.

Start a new Codex thread and send a setup prompt like:

```text
Start $codex-director for this project.
Use this thread as the Director thread. Read the project instructions, identify the project scope, set up the Director operating brief, and tell me what you need from me before coordinating work.
```

`$codex-director` is a Codex skill mention, not a terminal command. Use it explicitly when setting up the Director or when you want to force the skill to activate.

After the Director thread is established, give it outcomes, not workflow mechanics. You should not need to say "use dynamic workflow", "orchestrate", "use workers", or "run subagents". The Director should decide that based on scope, risk, parallelism, evidence needs, and token economy. Every worker or packet it routes must have a selected workflow/playbook and top-level control loop recorded before dispatch, whether or not you asked for the structure. If it cannot name the workflow yet, it is still routing and should not launch the worker.

```text
Coordinate the Discord invite work.
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

The Director titles and pins its coordination thread as the stable `<Project Display Name> Director` handle, then creates separate Codex worker threads for project work. Task-specific focus belongs in the ledger and worker titles, not by retitling the parent Director. Local material-focus title rules apply to ordinary task threads and child workers, not to the parent Director. On setup, heartbeat/callback/resume, worker title changes, and final checkpoints, the Director restores the parent title if the app auto-title layer has drifted it toward the latest task. The user's request to set up or use a Director for the project is the explicit separate-thread authorization for bounded worker threads inside that project scope; outside that scope, the active `codex_app` thread contract still governs. Director-created workers are accepted only after the Director reads the child thread and reconciles the worker's evidence. Non-trivial Director-created workers use helper/subagent lanes; direct leaf is worker-internal only for tiny, mechanical, low-risk work. The Director thread stays available for instructions, check-ins, steering, evidence integration, and final status.

### Director boundary

The Director thread coordinates only. It may answer from its existing ledger or conversation state, draft worker briefs, monitor and steer worker threads, reconcile evidence, and produce final status. It must delegate repo/docs/code inspection, tests, smoke checks, production/service checks, file edits, deploys, external project/service writes, migrations, schema/data fixes, rollback/repair, and reviews to Codex worker threads or dynamic workflow packets. If worker thread tools are unavailable for required project work, it reports a runtime blocker instead of doing the work inline.

Status, checkup, and lookup requests follow the same rule: ledger-only status can be answered inline; repo/prod-backed status must be delegated.

Examples:

```text
Coordinate this production incident.
```

Expected behavior: dispatch a read-only verifier worker, stop for any required safety/production authority, dispatch remediation through a bounded worker, route independent oracle/review, dispatch final verification, archive/cleanup after evidence capture, and return concise final evidence.

```text
Here are four outcomes I need this week: <list>.
```

Expected behavior: route each distinct topic to a bounded worker thread or dynamic workflow packet, record handles and expected evidence, stop for more instructions, and avoid live polling narration.

```text
What is blocked right now?
```

Expected behavior: answer from the Director ledger when possible; dispatch or continue workers for any repo/docs/code/prod-backed status.

The Director is optimized for rapid-fire intake: each distinct ask should be routed to a bounded worker thread or workflow packet, recorded with its handle and expected evidence, then released so the Director can immediately accept the next instruction.

## Structure

- `plugins/codex-director/.codex-plugin/plugin.json` is the plugin manifest.
- `plugins/codex-director/hooks/` contains an intentionally empty hook config; Director does not bundle active lifecycle hooks or a hook runner.
- `plugins/codex-director/skills/codex-director/SKILL.md` is the compact entrypoint Codex reads when selecting the skill.
- `plugins/codex-director/skills/codex-director/REFERENCE.md` contains the full operating brief, worker templates, evidence rules, and status formats.
- `plugins/codex-director/skills/codex-director/references/` contains workflow playbooks for build, review, research, dynamic workflow integration, Browser ChatGPT oracle, and related execution modes.
- `plugins/codex-director/skills/codex-director/agents/` contains optional model/profile guidance that travels with the skill.

## Operating Model

```text
Director Codex thread
  -> Codex worker threads
      -> named selected workflow/playbook and top-level control loop
          -> selected self-contained workflow / dynamic workflow packet / optional tool implementation
          -> research, oracle, review, and verification gates
```

The skill is intentionally project-scoped: the project can be a single repo, a multi-repo workspace, or a projectless working directory.
