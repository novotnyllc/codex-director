# Prompt Export Workflow

Use when the Director or a delegated worker needs to package project context into a durable local artifact for an oracle, review model, worker handoff, upload, retry, or another external reasoning lane. In a Director-managed worker, this exports evidence only; the worker still returns an Oracle Request Packet and artifact path to the Director unless explicitly delegated receiver-runner authority.

## Principle

Extract the real task, select the right evidence, export a self-contained prompt artifact, and hand that artifact to the next reasoning lane. The export should make the receiver useful immediately without requiring the user to copy context manually.

Browser ChatGPT Pro oracle does not normally need this workflow anymore: [Browser ChatGPT Pro oracle workflow](browser-chatgpt-oracle-workflow.md) should assemble and submit the prompt directly through `@Browser` when Pro is available. Use prompt export for Browser only when a durable payload artifact is useful for audit, upload/chunking, retry after automation failure, cross-thread handoff, or explicit user request.

## Phase 0: Extract The Real Task

Confirm the launch contract first: model, thinking level plus rationale, commit authority, required skills/workflows, receiver lane, sensitivity boundary, and evidence format. Discover applicable Codex skills and record skills considered, loaded, skipped, and not loaded in activation.

Strip prompt/export meta-framing.

Examples:

- "Export a prompt to evaluate auth refresh" -> task is "evaluate auth refresh".
- "Write a ChatGPT prompt about token caching" -> task is "investigate token caching".
- "Review the last 3 commits" -> task is already review.

Use the extracted task for intent classification and context building.

The export should let the receiver do the real task directly. Do not ask another model to "write a better prompt" unless prompt design itself is the actual task.

## Phase 1: Classify Intent

Choose one:

- Question: specific bounded question with a clear answer.
- Plan: design, approach, implementation plan, architecture, audit, evaluation, or broad "look into X".
- Review: git diff, PR, branch comparison, worker output, or plan/result critique.

When in doubt, default to Plan. It produces a more useful structured prompt for broad or ambiguous work.

Rules:

- Review exports for code must include the words "code review", comparison scope, changed files, and expected findings-first output.
- Plan exports must include goal, background, constraints, open questions, and requested work item shape.
- Question exports must include exact question, evidence boundaries, and uncertainty/reporting expectations.
- Browser ChatGPT exports, when created, must include a concise requested response shape and a sensitive-data note.

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

If a context engine is available, use its export/prompt packaging function. If not, write the prompt file manually with links or file references instead of pasting large source dumps. Include source excerpts only when necessary for the receiver to reason correctly.

## Phase 4: Export Artifact

Write a unique repo-local file, normally under `prompt-exports/`.

Suggested names:

- `prompt-exports/<timestamp>-question-<slug>.md`
- `prompt-exports/<timestamp>-plan-<slug>.md`
- `prompt-exports/<timestamp>-review-<slug>.md`
- `prompt-exports/<timestamp>-browser-oracle-<slug>.md`

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
- intended receiver: local oracle, review worker, Browser ChatGPT Pro oracle, etc.

If the export is for Browser ChatGPT Pro oracle, treat it as an optional payload artifact for [Browser ChatGPT Pro oracle workflow](browser-chatgpt-oracle-workflow.md), not as a required phase. Run the Browser round trip when Pro is available; if Pro is unavailable or ambiguous, use the built-in main/`xhigh` oracle/review fallback unless the user explicitly required Pro-only/no fallback.

After the receiver consumes the export and the result is captured, delete stale exports unless they are durable evidence for the task.

## Anti-Patterns

- Exporting a prompt about prompting rather than the actual task.
- Using generic filenames like `prompt.md`.
- Asking generic workflow questions before checking evidence.
- Using fast path for broad review/plan tasks.
- Sending sensitive data externally without permission or redaction.
- Rewriting a good exported prompt without a concrete defect.
- Creating a prompt export solely because Browser ChatGPT Pro oracle was selected.
- Treating the export file as the final result when the selected lane is Browser ChatGPT Pro oracle.
- Forgetting comparison scope in review exports.
