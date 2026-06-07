# Browser ChatGPT Pro Oracle Workflow

Use when the Director needs an external second-opinion result from ChatGPT Pro through the signed-in in-app Browser session, or when a worker has been explicitly launched as a delegated Browser ChatGPT Pro oracle runner. Ordinary implementation/review workers that need this lane should return an Oracle Request Packet to the Director rather than opening or messaging ChatGPT themselves. The workflow must detect whether a Pro-capable ChatGPT model/tier is available before submitting; not every signed-in account has access.

## Principle

The Browser ChatGPT Pro oracle is an implementation of the oracle lane. It should assemble the prompt payload from the current task, selected evidence, and existing plan/review/research artifacts, then use `@Browser` with the `browser:control-in-app-browser` skill to complete the ChatGPT round trip only after the Director has selected this lane for a real oracle request. It may open `https://chatgpt.com/`, start a new chat, inspect the model picker/account UI for Pro-capable availability, select ChatGPT Pro or the requested Pro-tier model when available, send the prompt, wait for the response to finish even when it takes a while, extract the answer, save the result as an artifact, and feed the result back into the plan/review/build workflow. It should not become a manual copy/paste chore for the user, and it should not open or navigate an in-app Browser merely to check whether Pro might be available.

Do not require a separate prompt file just because Browser ChatGPT Pro is the selected oracle lane. Write a prompt artifact only when it adds real value: durable audit trail, large payload/upload, resumability after Browser failure, cross-thread handoff, or explicit user request. When this workflow is selected for a delegated oracle-runner worker, that runner must complete the Browser round trip unless blocked by sign-in, Pro availability, safety, or browser automation failure. Other workers should request this lane through the Director. Do not run a non-Pro ChatGPT model and report it as a Pro oracle; when Pro is unavailable, prefer the built-in Codex oracle/review lane with main/`xhigh`.

If the Browser oracle runner is a Director-created worker, its result artifact and callback are not accepted until the Director reads the runner's child thread with `codex_app.read_thread`, captures the terminal report, reconciles oracle evidence and helper/direct-leaf policy, and records cleanup/archive state. Native V2 helpers may support local fallback review, prompt preparation, or reconciliation inside the runner, but they must not bypass Browser/Pro suitability, privacy approval, or Director-mediated oracle routing.

## Safety Gate

Before sending content to ChatGPT through Browser, check whether the payload contains secrets, credentials, raw private data, source-data exports, transcripts, tokens, invite links, or regulated data. If it does, ask the user for explicit permission or create a redacted/summarized prompt first.

Do not print sensitive payloads in chat. Prefer local files and concise status.

## Phase 0: Decide Whether Browser ChatGPT Pro Oracle Is Appropriate

Confirm the launch contract first: model/thinking plus rationale for the runner, requested ChatGPT model or tier, required skills/workflows, sensitivity boundary, commit authority, helper/direct-leaf policy, native helper runtime surface, and evidence format. Discover applicable Codex skills and record skills considered, loaded, skipped, and not loaded in activation.

Use Browser ChatGPT Pro oracle when a Pro web-model second opinion is materially better than the local oracle/review lane, even if the user did not explicitly say Pro:

- The normal local oracle lane is unavailable, insufficient, or likely to share the same blind spot as the worker/reviewer.
- A high-ambiguity plan/result needs independent critique and the extra Browser round trip is justified.
- The prompt benefits from ChatGPT's current web product context, product/UX/content judgment, or model diversity.
- Broad architecture tradeoffs, conflicting local reviews, or final critique before high-cost work would benefit from an external Pro-model challenge.
- The user is already signed in and the sentinel or current Browser state suggests Pro may be available.
- The user explicitly asks to use ChatGPT Pro, ChatGPT in Browser, or the signed-in `chatgpt.com` session.

When a local oracle or review lane is sufficient, use the local lane. Browser is higher overhead and may send data outside the local environment. Prefer local oracle/review for sensitive payloads, routine source-backed code review, ordinary diffs, and fast review loops.

Do not preflight Pro access by opening or navigating an in-app Browser just to inspect the account. Decide whether the Browser Pro lane is warranted from the task, user request, sensitivity boundary, and available local lanes. Pro availability inspection happens only as part of executing the selected Browser Pro oracle lane, or in an already-open ChatGPT tab when that inspection is safe and non-disruptive.

### Capability Sentinel

Use a local capability sentinel as a cache, not as a probe. Reading the sentinel is non-invasive; creating or refreshing it must happen only after a real Browser Pro oracle run or after inspecting an already-open ChatGPT tab that is safe to touch.

Preferred write locations, in order:

1. User state: `$XDG_STATE_HOME/codex-director/chatgpt-pro-capability.json`, or `~/.local/state/codex-director/chatgpt-pro-capability.json` when `XDG_STATE_HOME` is unset.
2. Repo-local untracked state: `.codex-director/local-state/chatgpt-pro-capability.json`, with `.codex-director/` added to `.git/info/exclude` when allowed. Do not edit tracked `.gitignore` just to store this cache.
3. Director ledger/thread notes only, when filesystem writes are unavailable or sandboxed.

The sentinel is advisory and may be stale. A missing, unreadable, expired, or sandbox-inaccessible sentinel means `unknown`; it must not trigger Browser navigation. Negative or ambiguous sentinel values should bias toward the built-in Codex oracle/review lane unless the user explicitly asks for Browser Pro.

When the sentinel is expired and Browser Pro would materially affect routing, a non-invasive refresh is allowed only if one of these is already available:

- An already-open ChatGPT tab in the in-app Browser that can be inspected without navigation, reload, chat submission, account-settings browsing, or disruption to an in-progress user chat.
- Browser/tab metadata exposed by active Browser tooling that can identify a safe existing ChatGPT surface without opening a new page.
- A just-completed selected Browser Pro oracle run, where the model picker was already inspected as part of the run.

If none of those surfaces exists, leave the sentinel stale or record `pro_available: "unknown"` with `refresh_status: "deferred_no_safe_surface"`. Do not ask the user to log in or open Browser merely to refresh the sentinel. Ask for login only after a real Browser Pro oracle run has been selected and sign-in is required to complete that run.

Suggested fields:

```json
{
  "schema": 1,
  "checked_at": "2026-06-04T00:00:00Z",
  "expires_at": "2026-06-11T00:00:00Z",
  "next_noninvasive_refresh_after": "2026-06-11T00:00:00Z",
  "last_noninvasive_refresh_attempt_at": "2026-06-11T00:00:00Z",
  "source": "selected_browser_pro_oracle_run|already_open_chatgpt_tab|safe_browser_metadata|deferred_no_safe_surface",
  "refresh_status": "fresh|stale|deferred_no_safe_surface|sandbox_inaccessible",
  "login_state": "signed_in|login_required|unknown",
  "pro_available": "yes|no|ambiguous|unknown",
  "selected_label": "ChatGPT Pro",
  "browser_context_hint": "default|unknown",
  "notes": "no prompts, responses, credentials, raw account identifiers, or private payloads"
}
```

Keep TTLs short enough that stale account state does not become authority. Treat `yes` as a convenience hint, not proof; confirm Pro availability during the actual selected Browser Pro run before sending. Treat `no`, `ambiguous`, `login_required`, `stale`, and `deferred_no_safe_surface` as routing hints only.

Do not use it for:

- tiny mechanical changes
- sensitive payloads without permission
- tasks where local review is enough
- prompts too large to submit reliably without file upload or chunking

## Phase 1: Assemble The Prompt Payload

Build the prompt directly from the current plan/review/research artifact, selected evidence, and exact question the oracle should answer. Include task, context, constraints, desired output format, sensitivity notes, and explicit review questions.

Use optional [prompt artifact notes](optional-prompt-artifact-notes.md) only when a durable scratch/handoff artifact is explicitly useful for audit, upload/chunking, cross-thread handoff, resumability, or user request. The normal ChatGPT Pro oracle path keeps the prompt payload in memory and submits it directly through Browser.

The prompt should ask for concise, actionable output. Examples:

```text
Review this plan adversarially. Return:
1. Must-fix gaps
2. Missing research or evidence
3. Sequencing risks
4. Test/verification gaps
5. Verdict: proceed / revise / block
```

Model/effort guidance: ChatGPT Pro oracle is normally a high-quality second-opinion lane. Use it when the expected critique is worth the Browser round trip, whether or not the user named Pro. Do not use it as a cheap first-pass scout.

When native V2 helpers are exposed, keep them local and bounded: `explore` for prompt-source or fallback evidence checks, `pair` for reconciliation if Browser and local oracle disagree, `engineer` only for mechanical prompt artifact preparation, and `design` for critique-shape/polish. Record helper role/model/thinking/fork rationale when exposed, verify helper output locally, and close helpers or record `close_blocked:<reason>`.

```text
Review this implementation summary and evidence. Return only findings that could change whether this should ship.
```

## Phase 2: Submit Through Browser

Use the `@Browser` plugin and load/follow the `browser:control-in-app-browser` skill for the in-app browser session after the Director has selected this lane for an actual oracle request. Do not satisfy this workflow by only writing a prompt artifact, by using generic web browsing, or by asking the user to paste the prompt manually. Do not open or navigate Browser solely to test whether ChatGPT Pro is available.

1. Connect to the selected in-app Browser tab, preferring an already-open ChatGPT tab when one exists and is safe to inspect.
2. Navigate to `https://chatgpt.com/` only because this Browser Pro oracle run has been selected, not just for availability preflight.
3. If ChatGPT is not signed in, pause and ask the user to log in in the in-app Browser. Do not ask for credentials in chat. Resume the same run after the user confirms login, or use the built-in main/`xhigh` fallback only if the user declines/cannot log in and fallback is allowed.
4. Start a new chat. Do not reuse the current chat unless the user explicitly asks to.
5. Inspect the model picker/account UI enough to determine Pro availability. Keep inspection minimal and non-disruptive: do not change unrelated account settings, browse account pages, or disturb an in-progress user chat. Record `pro_available: yes/no/ambiguous`, the visible labels inspected, and the selected label.
6. Select ChatGPT Pro or the requested Pro-tier model when available. If Pro availability is `no` or `ambiguous`, do not use a non-Pro web model by default; record the availability result and fall back to the built-in Codex oracle/review lane with main/`xhigh`, unless the user explicitly asked for Pro-only/no fallback or explicitly allowed a non-Pro web fallback.
7. Paste or type the assembled prompt payload into ChatGPT.
8. If the prompt is too large for reliable paste, create a temporary prompt artifact only as upload/chunking support and try file upload if available; otherwise split into labeled chunks and ask ChatGPT to wait until the final chunk before answering.
9. Submit.

If any required Browser step is unavailable:

- Browser plugin unavailable: use the built-in Codex oracle/review lane with main/`xhigh` unless the user explicitly required Browser/Pro-only/no fallback; otherwise record the substitution.
- Not signed in: ask the user to log in through the in-app Browser and resume after confirmation. Do not ask for credentials in chat. If the user declines/cannot log in and fallback is allowed, use the built-in Codex oracle/review lane with main/`xhigh` and record the substitution.
- Pro availability cannot be inspected after login: use the built-in Codex oracle/review lane with main/`xhigh` unless the user explicitly required Pro-only/no fallback.
- Pro availability `no` or `ambiguous`: use the built-in Codex oracle/review lane with main/`xhigh` unless the user explicitly required Pro-only/no fallback; do not silently substitute a non-Pro web model.
- Named Pro model/tier unavailable or ambiguous when explicitly required: use built-in main/`xhigh` unless the user explicitly required that exact model/tier only.
- Prompt too sensitive: redact/summarize or ask explicit permission.
- UI automation unreliable: stop with the exact state reached and the prompt source, creating a temporary prompt artifact only if needed for retry or handoff.

Browser automation should stay in the background by default. Do not reload or disrupt a user-visible in-progress chat unless necessary.

Automation should follow the Browser plugin's own control instructions. Prefer DOM/Playwright-style interaction over visual guessing when reliable. After each click/type/submit, collect the cheapest state check needed to confirm progress.

## Phase 3: Wait And Capture

After submitting:

1. Wait for ChatGPT to finish generating. Pro responses can take a while; poll patiently until the stop/regenerate controls and page state indicate completion. Use a generous wait budget and report progress only if the wait becomes unusually long.
2. Capture the final assistant response from the page.
3. Save it to the active workflow's `results/` directory only when this is already an accepted/reconciled packet result; otherwise save to a scratch or candidate-result artifact until Director readback and reconciliation promote it. Use another local scratch artifact path when a standalone result file is useful.
4. Include the prompt source (`direct` or artifact path), selected ChatGPT model label, ChatGPT URL if available, timestamp, elapsed wait time, helper/direct-leaf status if delegated, cleanup/archive expectation, and any automation caveats.

Capture metadata:

```text
Prompt source/artifact:
Result artifact:
Runner thread id if delegated:
Readback status if Director-created runner:
Helper/direct-leaf status:
Model/label selected:
Submission time:
Completion time:
Pro availability:
Built-in xhigh fallback used:
```

If extraction is brittle, capture the visible response text and a screenshot reference if useful. Do not rely only on a screenshot when text extraction is possible.

If the response is long, save the full text to the result artifact and summarize only the verdict and must-fix items in the Director status.

## Phase 4: Feed Back Into The Workflow

Use the Browser ChatGPT Pro oracle result as evidence, not as authority. If the oracle result came from a delegated Director-created runner, treat the result as candidate evidence until child-thread readback and reconciliation are complete.

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

- prompt source or artifact path if one was created
- result artifact path
- Pro availability result and selected ChatGPT model label, or built-in main/`xhigh` fallback note
- verdict
- must-fix findings count
- whether the plan/work was updated
- delegated runner readback status, helper/direct-leaf acceptance, and cleanup/archive state when applicable
- native helper surface and V2 helper profiles/evidence/owner verification/cleanup when used
- any blockers or caveats

Do not paste the full oracle response unless the user asks.

## Failure Modes

- Not signed in: ask the user to log in through the in-app Browser, then resume after confirmation. Do not ask for credentials in chat. If the user declines/cannot log in and fallback is allowed, use the built-in Codex oracle/review lane with main/`xhigh` and record the substitution.
- ChatGPT Pro unavailable or ambiguous: use the built-in Codex oracle/review lane with main/`xhigh` and record the substitution, unless the user explicitly required Pro-only/no fallback.
- ChatGPT refuses or truncates: reduce context, upload file if available, or ask a narrower question.
- Browser automation cannot extract result: save what can be extracted, note the blocker, and create or keep a temporary prompt artifact only if needed for retry or handoff.
- Sensitive payload detected: pause for permission or redact.
- Page structure changes make capture unreliable.
- Reporting a delegated oracle-runner callback or result artifact as accepted before `codex_app.read_thread` readback and evidence reconciliation.
- Treating V2 helper output as an oracle result or Browser/Pro availability proof.

## Evidence

The final evidence bundle should include:

- prompt source or artifact path if one was created
- Browser ChatGPT Pro oracle result path
- Pro availability result and selected ChatGPT model label
- verdict
- follow-up edits or decisions made from the result
- unresolved caveats
- delegated runner thread id, child-thread readback status, helper/direct-leaf status, and cleanup/archive state when applicable
- native helper surface and V2 helper profiles/evidence/owner verification/cleanup when used
