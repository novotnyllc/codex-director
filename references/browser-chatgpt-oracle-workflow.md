# Browser ChatGPT Oracle Workflow

Use when the chief thread or a Codex worker thread needs an external second-opinion result from ChatGPT through the signed-in in-app Browser session.

## Principle

The browser oracle is an implementation of the oracle lane. It should package context, send it to ChatGPT in the in-app Browser, wait for the response, extract the answer, save it as an artifact, and feed the result back into the plan/review/build workflow. It should not become a manual copy/paste chore for the user.

## Safety Gate

Before sending content to ChatGPT through Browser, check whether the payload contains secrets, credentials, raw private data, source-data exports, transcripts, tokens, invite links, or regulated data. If it does, ask the user for explicit permission or create a redacted/summarized prompt first.

Do not print sensitive payloads in chat. Prefer local files and concise status.

## Phase 0: Decide Whether Browser Oracle Is Appropriate

Use Browser ChatGPT oracle when:

- The normal local oracle lane is unavailable, insufficient, or the user specifically wants ChatGPT web.
- A plan/result needs independent critique.
- The prompt benefits from ChatGPT's current web product context or model mix.
- The user is already signed in and wants automatic round-trip results.

Do not use it for:

- tiny mechanical changes
- sensitive payloads without permission
- tasks where local review is enough
- prompts too large to submit reliably without file upload or chunking

## Phase 1: Package The Prompt

Use [Prompt Export workflow](prompt-export-workflow.md) to extract the real task, infer Question/Plan/Review, build context, and export a repo-local prompt file under `prompt-exports/`.

If a full export is unnecessary, build the prompt from the current plan/review/research artifact and selected evidence. Include task, context, constraints, desired output format, and explicit review questions. Save it under `prompt-exports/<timestamp>-browser-oracle-<slug>.md`.

The prompt should ask for concise, actionable output. Examples:

```text
Review this plan adversarially. Return:
1. Must-fix gaps
2. Missing research or evidence
3. Sequencing risks
4. Test/verification gaps
5. Verdict: proceed / revise / block
```

Model/effort guidance: browser oracle is normally a main/high-quality second-opinion lane. Use it only when the expected critique is worth the browser round trip. Do not use it as a cheap first-pass scout.

```text
Review this implementation summary and evidence. Return only findings that could change whether this should ship.
```

## Phase 2: Submit Through Browser

Use the Browser plugin and its in-app browser session.

1. Connect to the selected in-app Browser tab.
2. Use the existing `https://chatgpt.com/` session if it is already open; otherwise navigate there.
3. Start a new chat unless the user explicitly wants the current chat reused.
4. Read the prompt file locally.
5. Paste or type the prompt into ChatGPT.
6. If the prompt is too large for reliable paste, try file upload if available; otherwise split into labeled chunks and ask ChatGPT to wait until the final chunk before answering.
7. Submit.

Browser automation should stay in the background by default. Do not reload or disrupt a user-visible in-progress chat unless necessary.

Automation should follow the Browser plugin's own control instructions. Prefer DOM/Playwright-style interaction over visual guessing when reliable. After each click/type/submit, collect the cheapest state check needed to confirm progress.

## Phase 3: Wait And Capture

After submitting:

1. Wait for ChatGPT to finish generating.
2. Capture the final assistant response from the page.
3. Save it to `prompt-exports/<timestamp>-browser-oracle-result-<slug>.md`.
4. Include the source prompt path, ChatGPT URL if available, timestamp, and any automation caveats.

If extraction is brittle, capture the visible response text and a screenshot reference if useful. Do not rely only on a screenshot when text extraction is possible.

If the response is long, save the full text to the result artifact and summarize only the verdict and must-fix items in the CoS status.

## Phase 4: Feed Back Into The Workflow

Use the Browser oracle result as evidence, not as authority.

For plan review:

- Fold must-fix findings into the plan.
- Resolve or explicitly reject suggestions.
- Record the verdict and remaining risks.

For build/review:

- Fix must-fix issues before completion.
- If the oracle conflicts with local evidence, prefer local source-backed evidence and record the conflict.

For research:

- Treat current external claims as dated.
- Verify high-stakes or unstable facts with primary sources where possible.

## Phase 5: Report Concisely

Return:

- prompt export path
- result artifact path
- verdict
- must-fix findings count
- whether the plan/work was updated
- any blockers or caveats

Do not paste the full oracle response unless the user asks.

## Failure Modes

- Not signed in: ask the user to sign in or fall back to local oracle/review.
- ChatGPT refuses or truncates: reduce context, upload file if available, or ask a narrower question.
- Browser automation cannot extract result: save what can be extracted, note the blocker, and keep the prompt export.
- Sensitive payload detected: pause for permission or redact.

## Evidence

The final evidence bundle should include:

- exported prompt path
- browser oracle result path
- verdict
- follow-up edits or decisions made from the result
- unresolved caveats
