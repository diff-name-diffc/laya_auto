"""Reference validators for the browser Agent integration.

These are the executable form of the rules in ``AGENT_INTEGRATION_PROMPT.md``
(§5). Copy them into the implementation, or import them — they carry no Laya or
Playwright dependency, so they are cheap to unit-test.
"""

from __future__ import annotations

import json
import math
from typing import Any, Dict, Iterable, List, Optional, Tuple


class ValidationError(ValueError):
    """A request, answer or decision failed validation."""


class RequestTooLarge(ValidationError):
    """The request exceeds the server's caps; trim and resend, do not retry."""


class InvalidAnswer(ValidationError):
    """The model's answer is malformed; it must not be used."""


class InvalidOperation(ValidationError):
    """The model chose an operation that is not in the offered vocabulary."""


# --- §5.1 request validation -------------------------------------------------

DEFAULT_MAX_QUESTIONS = 64
DEFAULT_MAX_STATE_CHARS = 50_000
DEFAULT_MAX_BODY_BYTES = 2 * 1024 * 1024
Q_TYPES = ("choice", "score", "noul")


def validate_question(q: Dict[str, Any]) -> None:
    if not isinstance(q, dict):
        raise ValidationError("question must be an object")
    if q.get("type") not in Q_TYPES:
        raise ValidationError(f"unknown question type {q.get('type')!r}; use {Q_TYPES}")
    crit = q.get("criteria")
    if q["type"] == "choice":
        if not isinstance(crit, dict) or not crit:
            raise ValidationError("choice requires a non-empty criteria map")
    elif q["type"] == "score":
        if not isinstance(crit, list) or len(crit) < 2:
            raise ValidationError("score requires a criteria list of >= 2 levels")
    if "instructions" not in q:
        raise ValidationError("question requires instructions")


def validate_request(
    state: Any,
    questions: Dict[str, Any],
    *,
    max_questions: int = DEFAULT_MAX_QUESTIONS,
    max_state_chars: int = DEFAULT_MAX_STATE_CHARS,
) -> None:
    if not isinstance(questions, dict):
        raise ValidationError("questions must be an object")
    if len(questions) > max_questions:
        raise RequestTooLarge(f"too many questions ({len(questions)} > {max_questions})")
    try:
        size = len(state) if isinstance(state, str) else len(
            json.dumps(state, ensure_ascii=False))
    except (TypeError, ValueError):
        raise ValidationError("state is not JSON-serialisable")
    if size > max_state_chars:
        raise RequestTooLarge(f"state too large ({size} > {max_state_chars} chars)")
    for qid, q in questions.items():
        try:
            validate_question(q)
        except ValidationError as exc:
            raise ValidationError(f"question {qid!r}: {exc}") from exc
    # v3 invariant: candidate elements must NOT be in state.
    if isinstance(state, dict) and "elements" in state:
        raise ValidationError(
            "state must not contain 'elements' (v3 puts candidates in "
            "questions.*.criteria); a 1024-token window truncates them there"
        )


# --- §5.2 answer validation --------------------------------------------------

def validate_choice_answer(ans: Dict[str, Any], keys: Iterable[str]) -> Dict[str, Any]:
    """Validate a `choice` answer against the offered keys. Raises InvalidAnswer."""
    keyset = set(keys)
    if not isinstance(ans, dict):
        raise InvalidAnswer("answer is not an object")
    probs = ans.get("probabilities")
    if not isinstance(probs, dict) or not probs:
        raise InvalidAnswer("missing probabilities")
    if set(probs) != keyset:
        raise InvalidAnswer("probability keys do not match the offered criteria")
    nums = [*probs.values(), ans.get("confidence", 0.0)]
    if not all(isinstance(n, (int, float)) and math.isfinite(n) and 0.0 <= n <= 1.0
               for n in nums):
        raise InvalidAnswer("probabilities are not finite numbers in [0,1]")
    if abs(sum(probs.values()) - 1.0) >= 0.02:
        raise InvalidAnswer("probabilities do not sum to 1")
    choice = ans.get("choice")
    if choice not in keyset:
        raise InvalidAnswer("choice is not one of the offered criteria")
    if probs[choice] < max(probs.values()) - 1e-6:
        raise InvalidAnswer("choice is not the argmax of its probabilities")
    return ans


def validate_noul_answer(ans: Dict[str, Any]) -> float:
    v = ans.get("noul") if isinstance(ans, dict) else None
    if not isinstance(v, (int, float)) or not math.isfinite(v) or not 0.0 <= v <= 1.0:
        raise InvalidAnswer("noul must be a finite probability in [0,1]")
    return float(v)


# --- §5.6 operation normalisation -------------------------------------------

def normalize_operation(op: Any, targets: Dict[str, Any], controls: Dict[str, Any]) -> str:
    """Map the model's operation onto the offered vocabulary, or raise."""
    if not isinstance(op, str):
        raise InvalidOperation(f"operation must be a string, got {type(op).__name__}")
    if op in ("DONE", "BLOCKED"):
        return op
    if op in targets:
        return op
    upper = op.upper()
    known_controls = {k.upper() for k in controls}
    if upper in known_controls:
        return upper
    raise InvalidOperation(f"{op!r} is not in the offered vocabulary")


def resolve_target(
    operation: str,
    answer: Dict[str, Any],
    targets: Dict[str, Dict[str, Any]],
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """Return (key, action) for the target head matching the chosen operation.

    Only the head matching the operation is consumed; any other head the model
    answered is ignored (the heads are speculative).
    """
    if operation in ("DONE", "BLOCKED"):
        return None, None
    head = operation.lower() + "_target"
    if head not in answer:
        return None, None            # this operation has no target head
    ans = answer[head]
    keys = targets.get(operation, {})
    try:
        validate_choice_answer(ans, keys)
    except InvalidAnswer:
        return None, None
    key = ans["choice"]
    return key, keys.get(key)


# --- §5.3 semantic marker ----------------------------------------------------

def marker(observation: Dict[str, Any]) -> str:
    """Semantic fingerprint. Same meaning -> same value; geometry excluded."""
    import hashlib

    payload = {
        "url": observation.get("url"),
        "title": observation.get("title"),
        "text": observation.get("text"),
        "semantics": [
            [a.get("id"), a.get("kind"), a.get("label"), a.get("value"), a.get("current_value")]
            for a in observation.get("actions", [])
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


# --- §5.5 no-progress / loop detection --------------------------------------

def detect_no_progress(trajectory: List[Dict[str, Any]], window: int = 4) -> bool:
    """True if the last `window` steps changed nothing and none was a wait."""
    recent = trajectory[-window:]
    if len(recent) < window:
        return False
    if any(step.get("page_changed") for step in recent):
        return False
    return all(step.get("kind") != "wait" for step in recent)


def detect_repeat(trajectory: List[Dict[str, Any]], window: int = 3) -> bool:
    """True if the same (operation, target) repeats `window` times consecutively."""
    recent = trajectory[-window:]
    if len(recent) < window:
        return False
    sigs = {(s.get("operation"), s.get("target")) for s in recent}
    return len(sigs) == 1


# --- §6 independent verification --------------------------------------------

def is_bot_challenge(url: str, text: str) -> bool:
    u, t = (url or "").lower(), (text or "").lower()
    return (
        "sorry/index" in u
        or "unusual traffic" in t
        or "complete the following challenge" in t
        or "not a robot" in t
        or "detected unusual traffic" in t
    )
