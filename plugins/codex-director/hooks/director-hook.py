#!/usr/bin/env python3
"""Scoped advisory hooks for the Codex Director plugin."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


DIRECTOR_MARKERS = (
    "$codex-director",
    "codex-director",
    "codex director",
    "director thread",
)

TAIL_BYTES = 262_144

CONTEXT_MESSAGES = {
    "SessionStart": (
        "[codex-director] Director thread reminder: coordinate, dispatch, monitor, "
        "steer, reconcile evidence, and keep project work in Codex worker threads."
    ),
    "UserPromptSubmit": (
        "[codex-director] If this is the Director thread, route before doing work. "
        "If this needs repo/docs/code/prod inspection, create or continue a worker; "
        "do not inspect, test, edit, deploy, query production, or narrate polling "
        "inline. Use dynamic workflow for production or external project/service writes."
    ),
    "SubagentStart": (
        "[codex-director] Nested helpers are worker-internal. Keep scope under "
        "the owning worker or packet and roll concise evidence back up."
    ),
}

SYSTEM_MESSAGES = {
    "Stop": (
        "[codex-director] Closeout reminder: capture worker evidence; record "
        "missing activation/review/oracle blockers; account for active, stale, "
        "and cancelled workers; note cleanup needs and archive decisions; keep "
        "routine progress narration out of chat."
    ),
    "SubagentStop": (
        "[codex-director] Nested helper closeout: record concise evidence in "
        "the owning worker or packet; do not treat helper transcripts as the "
        "Director ledger."
    ),
}


def main() -> int:
    event = sys.argv[1] if len(sys.argv) > 1 else None
    payload = read_payload()
    event = event or payload.get("hook_event_name")
    if not isinstance(event, str):
        return 0

    if not is_director_context(payload):
        return 0

    if event in CONTEXT_MESSAGES:
        emit(
            {
                "hookSpecificOutput": {
                    "hookEventName": event,
                    "additionalContext": CONTEXT_MESSAGES[event],
                }
            }
        )
        return 0

    if event in SYSTEM_MESSAGES:
        emit({"systemMessage": SYSTEM_MESSAGES[event]})
        return 0

    return 0


def read_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def is_director_context(payload: dict[str, Any]) -> bool:
    direct_text = "\n".join(
        str(payload.get(key, ""))
        for key in (
            "prompt",
            "last_assistant_message",
            "source",
            "agent_type",
        )
    )
    if has_director_marker(direct_text):
        return True

    for key in ("transcript_path", "agent_transcript_path"):
        candidate = payload.get(key)
        if isinstance(candidate, str) and candidate:
            if has_director_marker(read_tail(candidate)):
                return True

    return env_truthy("CODEX_DIRECTOR_HOOKS_ALWAYS")


def has_director_marker(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in DIRECTOR_MARKERS)


def read_tail(path: str) -> str:
    try:
        target = Path(path).expanduser()
        size = target.stat().st_size
        with target.open("rb") as handle:
            if size > TAIL_BYTES:
                handle.seek(size - TAIL_BYTES)
            return handle.read().decode("utf-8", errors="ignore")
    except OSError:
        return ""


def env_truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def emit(payload: dict[str, Any]) -> None:
    json.dump(payload, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())
