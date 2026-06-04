# Deep Plan Workflow

Use when the deliverable is a durable implementation or architecture plan, not code.

## Principle

Plan only. The output is a polished, executable plan that future implementation workers can trust. Research scouts gather evidence; the planner owns synthesis, structure, and final wording. Do not implement, scaffold, or half-build.

## Phase 0: Scope And Involvement

1. Verify project/repo/path scope and local instructions.
2. Decide where the plan artifact belongs according to project conventions.
3. Confirm model, thinking level plus rationale, commit authority, required skills/workflows, and evidence format from the launch contract.
4. Discover applicable Codex skills; record skills considered, loaded, skipped, and unavailable in activation.
5. Ask the user for input only when an ambiguity would change architecture, order, scope, or risk.
6. If the user asks to be involved at a checkpoint, honor that promise. Do not silently continue past a chosen checkpoint.

Involvement modes:

- Hands-off: do the research and return the polished plan.
- Up-front: run a small ambiguity scan, then ask focused questions before broad research.
- Mid-flow: draft the plan, then ask only questions that would change order, scope, or risk before critique.

If the user explicitly chose a checkpoint and then does not answer, stop rather than silently proceeding with guessed answers.

## Phase 1: Grounded Ambiguity Scan

Before asking detailed questions, do a small evidence scan so questions are concrete.

Good ambiguity scout prompts:

```text
What existing patterns or conventions in <area> could apply to <task>? Report 2-3 concrete options with file:line refs. Do not propose a solution.
```

```text
This could land in <module A> or <module B>. Find evidence for each ownership path and the tradeoff. No implementation.
```

Ask the user only questions that the scan made sharper.

## Phase 2: Research And Seam Mapping

Run research lanes before drafting:

- In-workspace seams: how subsystems connect, key types, extension points.
- External facts: APIs/libraries/current behavior that the plan depends on.
- Prior art: existing plans, docs, commits, PRs, similar implementations.
- Constraints: deployment, data, auth, privacy, migration, operational rules.

Each scout gets one narrow question and returns sources, conflicts, confidence, and implications.

Curate findings into the plan's background. Do not paste raw scout transcripts.

Scout result format:

```text
Question:
Evidence:
Confidence:
Conflicts:
Plan implication:
References:
```

## Phase 3: Plan Scaffold

Create or prepare the plan file with:

- Goal.
- Background with curated evidence.
- Open questions.
- References.

Do not write the detailed approach before context planning unless it is already dictated by the user or project.

Default path when the project has no convention:

```text
docs/plans/<topic>-<YYYY-MM-DD>.md
```

If the repo forbids durable docs or the task is projectless, use a local artifact such as `prompt-exports/<timestamp>-plan-<slug>.md` and say it is local/non-durable.

## Phase 4: Context Plan Pass

Use the lightest adequate planning path:

- Use a context engine when it can cheaply synthesize the plan file/background, likely files, risks, and verification strategy.
- Ask an oracle/review thread to critique the evidence and propose an approach when independent judgment would reduce risk.
- Draft directly from research when the scope is narrow.
- Export the response when it will be handed to implementers or reviewers.

The draft must include:

- Recommended approach.
- Alternatives rejected and why.
- Ordered work items.
- Dependencies.
- Done criteria.
- Verification strategy.
- Review stop points.
- Risks and rollback notes.

If the context engine returns an export, treat it as the draft source, not a disposable hint. Read it, copy the useful approach/work items into the plan, then keep the export until critique is complete.

## Phase 5: Work Item Shaping

Each work item should have:

- Goal.
- Done when.
- Key files/modules.
- Dependencies.
- Size.
- Review gate.
- Evidence required.
- Commit boundary.

Most plans should have 2-3 work items. More than 5 usually means the abstraction level is too low.

## Phase 6: Plan Critique

Run a bounded design/adversarial critique before finalizing.

Ask the critic to check:

- Under-specified seams.
- Over-specified tactics implementers should own.
- Missing dependencies.
- Sequencing mistakes.
- Risks and test strategy.
- Open questions that would change implementation order.

The critic should not rewrite the plan. Fold actionable findings into the plan yourself.

Give the critic both the plan and any context-builder/oracle export that shaped it. Ask for top gaps, over-specified tactics, missing dependencies, sequencing risks, and questions that would change implementation order.

## Phase 7: Polish And Handoff

Final plan should be tight and executable:

- Clear goal and scope.
- Background with source-backed evidence.
- Concrete approach.
- Work items an implementation worker can execute.
- No transcript dumps.
- Open questions only when they matter.
- Suggested next workflow: build, orchestrate, review, investigate, refactor, or optimize.

## Evidence

Return plan path, summary, reviewed status, open questions, and suggested next workflow.

## Anti-Patterns

- Implementing while in plan mode.
- Asking generic questions before doing any grounding.
- Dumping raw scout transcripts into Background.
- Deleting the draft/export before critique has used it.
- Over-specifying tactical choices that implementation workers should own.
- Leaving plan work items without done criteria, dependencies, or verification.
