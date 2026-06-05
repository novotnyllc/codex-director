# Optional Prompt Artifact Notes

This is optional scratch/handoff guidance, not a Codex Director workflow. The Director contract remains Codex-native worker/thread lifecycle, with oracle/review mediated through Director packets and worker evidence.

For ChatGPT Pro oracle work, use [Browser ChatGPT Pro oracle workflow](browser-chatgpt-oracle-workflow.md): assemble the prompt payload from current task evidence and complete the Browser round trip directly when Pro is selected and available. Do not create a prompt export as a required or fallback oracle path.

Use a local prompt artifact only when it is explicitly useful outside the Director contract, for example:

- a payload is too large for reliable Browser paste and file upload/chunking needs a stable source;
- retrying after Browser automation failure requires a resumable payload;
- RepoPrompt, Oracle, or another context tool needs a handoff file path;
- the user explicitly asks for a prompt file;
- an audit trail needs the exact external-submission payload.

Prefer active workflow artifact directories such as `.workflow/<slug>/results/` when a packetized workflow exists. Otherwise use a repo-local ignored scratch path such as `prompt-exports/<timestamp>-<type>-<slug>.md`, and delete stale artifacts after the result is captured unless they are durable task evidence.

## Artifact Contents

Keep artifacts narrow and safe:

- actual task or oracle question;
- project/repo scope;
- selected evidence or file references;
- constraints and sensitivity notes;
- requested output shape;
- excluded sensitive material or redactions.

Do not dump full transcripts, secrets, credentials, raw private data, invite links, tokens, regulated data, or bulky logs into prompt artifacts.

## Anti-Patterns

- Treating a prompt artifact as a Director workflow dependency.
- Creating a prompt artifact solely because Browser ChatGPT Pro oracle was selected.
- Using a prompt artifact instead of completing the Browser ChatGPT Pro round trip.
- Treating a prompt artifact as the oracle result.
- Asking the user to manually copy/paste a prompt when Browser automation is available and safe.
- Writing a prompt about prompting rather than asking the actual task question.
- Keeping stale scratch artifacts after the receiver has consumed them.
