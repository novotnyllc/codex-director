# Prompt Export Workflow

Use when a worker needs to package project context for an oracle, review model, Browser ChatGPT session, or another external reasoning lane.

## Principle

Extract the real task, select the right evidence, export a self-contained prompt artifact, and hand that artifact to the next reasoning lane. The export should make the receiver useful immediately without requiring the user to copy context manually.

When the intended receiver is Browser ChatGPT oracle, prompt export is only Phase 1. The worker must continue into [Browser ChatGPT oracle workflow](browser-chatgpt-oracle-workflow.md), open `chatgpt.com` with `@Browser`, start a new chat, select the Pro model when available, submit the prompt, wait for completion, and capture the result artifact.

## Phase 0: Extract The Real Task

Strip prompt/export meta-framing.

Examples:

- "Export a prompt to evaluate auth refresh" -> task is "evaluate auth refresh".
- "Write a ChatGPT prompt about token caching" -> task is "investigate token caching".
- "Review the last 3 commits" -> task is already review.

Use the extracted task for intent classification and context building.

## Phase 1: Classify Intent

Choose one:

- Question: specific bounded question with a clear answer.
- Plan: design, approach, implementation plan, architecture, audit, evaluation, or broad "look into X".
- Review: git diff, PR, branch comparison, worker output, or plan/result critique.

When in doubt, default to Plan. It produces a more useful structured prompt for broad or ambiguous work.

## Phase 2: Confirm Scope

For Review:

- Check git state or review artifact.
- Determine scope: uncommitted, staged, last N commits, branch vs target, PR, plan, or worker result.
- Ask only if comparison scope is genuinely ambiguous.

For Question/Plan:

- If broad, architectural, evaluative, redesign-oriented, or multi-file, go straight to context building.
- Use fast path only when scope is small, concrete, and file-local.

## Phase 3: Build Context

Build context with the lightest adequate method:

- Use a context engine when it can cheaply curate files, slices, summaries, and code structure.
- For Review exports, include "code review" in the instructions when reviewing code changes.
- Otherwise use targeted search/read/code-structure/git commands.
- Add only relevant evidence.
- Write a prompt that includes task, context, constraints, desired output, and evidence pointers.

Do not spend many exploratory calls just proving a broad task needs context building.

## Phase 4: Export Artifact

Write a unique repo-local file, normally under `prompt-exports/`.

Suggested names:

- `prompt-exports/<timestamp>-question-<slug>.md`
- `prompt-exports/<timestamp>-plan-<slug>.md`
- `prompt-exports/<timestamp>-review-<slug>.md`

The prompt should contain:

- task
- project/repo scope
- selected context or evidence
- constraints
- requested output format
- review/plan/question focus
- safety notes about secrets or private data if relevant

## Phase 5: Handoff Or Execute

Return or pass forward:

- export path
- prompt type
- context path used
- token/size caveat if known
- intended receiver: Browser ChatGPT oracle, local oracle, review worker, etc.

If using Browser ChatGPT oracle, do not stop here. Pass the export path to [Browser ChatGPT oracle workflow](browser-chatgpt-oracle-workflow.md) and run the Browser round trip unless blocked.

## Anti-Patterns

- Exporting a prompt about prompting rather than the actual task.
- Using generic filenames like `prompt.md`.
- Asking generic workflow questions before checking evidence.
- Using fast path for broad review/plan tasks.
- Sending sensitive data externally without permission or redaction.
- Rewriting a good exported prompt without a concrete defect.
- Treating the export file as the final result when the selected lane is Browser ChatGPT oracle.
