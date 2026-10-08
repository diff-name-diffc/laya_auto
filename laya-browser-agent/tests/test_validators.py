"""Tests for the reference validators (AGENT_INTEGRATION_PROMPT.md §5, §6).

These run without a model or a browser. They are the harness's own proof that
each validation layer rejects what it claims to reject.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from e2e.reference_validators import (  # noqa: E402
    InvalidAnswer,
    InvalidOperation,
    RequestTooLarge,
    ValidationError,
    detect_no_progress,
    detect_repeat,
    is_bot_challenge,
    marker,
    normalize_operation,
    resolve_target,
    validate_choice_answer,
    validate_noul_answer,
    validate_question,
    validate_request,
)

Q = {"type": "choice", "criteria": {"a": "x", "b": "y"}, "instructions": "pick"}
GOOD = {"type": "choice", "choice": "a", "probabilities": {"a": 0.9, "b": 0.1}, "confidence": 0.9}


# --- request validation ------------------------------------------------------

def test_valid_request_passes():
    validate_request({"body": "hi"}, {"q": Q})


def test_v3_invariant_elements_not_in_state():
    with pytest.raises(ValidationError, match="must not contain 'elements'"):
        validate_request({"elements": [1, 2], "body": "x"}, {"q": Q})


def test_too_many_questions_is_request_too_large():
    qs = {f"q{i}": Q for i in range(100)}
    with pytest.raises(RequestTooLarge):
        validate_request({"body": "x"}, qs)


def test_oversized_state_is_request_too_large():
    with pytest.raises(RequestTooLarge):
        validate_request({"body": "x" * 60_000}, {"q": Q})


def test_bad_question_type_rejected():
    with pytest.raises(ValidationError, match="unknown question type"):
        validate_question({"type": "bogus", "instructions": "x"})


def test_choice_needs_criteria_map():
    with pytest.raises(ValidationError, match="non-empty criteria map"):
        validate_question({"type": "choice", "criteria": [], "instructions": "x"})


def test_score_needs_two_levels():
    with pytest.raises(ValidationError, match=">= 2 levels"):
        validate_question({"type": "score", "criteria": ["only"], "instructions": "x"})


# --- answer validation -------------------------------------------------------

def test_good_answer_accepted():
    validate_choice_answer(GOOD, ["a", "b"])


def test_probability_keys_must_match():
    bad = {"choice": "a", "probabilities": {"a": 0.9, "c": 0.1}, "confidence": 0.9}
    with pytest.raises(InvalidAnswer, match="do not match"):
        validate_choice_answer(bad, ["a", "b"])


def test_probabilities_must_sum_to_one():
    bad = {"choice": "a", "probabilities": {"a": 0.5, "b": 0.1}, "confidence": 0.9}
    with pytest.raises(InvalidAnswer, match="sum to 1"):
        validate_choice_answer(bad, ["a", "b"])


def test_choice_must_be_offered():
    bad = {"choice": "z", "probabilities": {"a": 0.9, "b": 0.1}, "confidence": 0.9}
    with pytest.raises(InvalidAnswer, match="not one of the offered"):
        validate_choice_answer(bad, ["a", "b"])


def test_choice_must_be_argmax():
    bad = {"choice": "a", "probabilities": {"a": 0.2, "b": 0.8}, "confidence": 0.9}
    with pytest.raises(InvalidAnswer, match="argmax"):
        validate_choice_answer(bad, ["a", "b"])


def test_nan_probability_rejected():
    bad = {"choice": "a", "probabilities": {"a": float("nan"), "b": 0.1}, "confidence": 0.9}
    with pytest.raises(InvalidAnswer):
        validate_choice_answer(bad, ["a", "b"])


def test_out_of_range_probability_rejected():
    bad = {"choice": "a", "probabilities": {"a": 1.5, "b": -0.5}, "confidence": 0.9}
    with pytest.raises(InvalidAnswer):
        validate_choice_answer(bad, ["a", "b"])


def test_noul_range():
    assert validate_noul_answer({"noul": 0.42}) == 0.42
    for bad in ({"noul": 1.5}, {"noul": -0.1}, {"noul": "x"}, {}):
        with pytest.raises(InvalidAnswer):
            validate_noul_answer(bad)


# --- operation normalisation -------------------------------------------------

def test_normalize_known_operations():
    assert normalize_operation("CLICK", {"CLICK": {}}, {}) == "CLICK"
    assert normalize_operation("DONE", {}, {}) == "DONE"
    assert normalize_operation("BLOCKED", {}, {}) == "BLOCKED"


def test_normalize_page_level_control_case_insensitive():
    assert normalize_operation("wait", {}, {"wait": {}}) == "WAIT"
    assert normalize_operation("WAIT", {}, {"wait": {}}) == "WAIT"


def test_normalize_rejects_unknown():
    with pytest.raises(InvalidOperation):
        normalize_operation("TELEPORT", {}, {})


def test_normalize_rejects_non_string():
    with pytest.raises(InvalidOperation):
        normalize_operation(None, {}, {})


# --- target resolution -------------------------------------------------------

def test_resolve_target_returns_action_for_matching_head():
    targets = {"CLICK": {"1": {"id": "click:1", "kind": "click", "label": "Search"}}}
    answer = {"click_target": {"type": "choice", "choice": "1",
                               "probabilities": {"1": 1.0}, "confidence": 1.0}}
    key, action = resolve_target("CLICK", answer, targets)
    assert key == "1" and action["id"] == "click:1"


def test_resolve_target_ignores_non_matching_head():
    """Only the head for the chosen operation is consumed."""
    targets = {"CLICK": {"1": {"id": "click:1"}}}
    answer = {
        "click_target": {"type": "choice", "choice": "1", "probabilities": {"1": 1.0}, "confidence": 1.0},
        "type_text_target": {"type": "choice", "choice": "9", "probabilities": {"9": 1.0}, "confidence": 1.0},
    }
    key, action = resolve_target("DONE", answer, targets)
    assert key is None and action is None


def test_resolve_target_returns_none_on_invalid_answer():
    targets = {"CLICK": {"1": {}, "2": {}}}
    answer = {"click_target": {"choice": "1", "probabilities": {"1": 0.5, "2": 0.1}}}  # sum != 1
    key, action = resolve_target("CLICK", answer, targets)
    assert key is None and action is None


def test_resolve_target_missing_head():
    assert resolve_target("TYPE_TEXT", {}, {"TYPE_TEXT": {}}) == (None, None)


# --- semantic marker ---------------------------------------------------------

def _obs(url="u", title="t", text="body", actions=None):
    return {"url": url, "title": title, "text": text, "actions": actions or []}


def test_marker_stable_for_same_semantics():
    a = [{"id": "click:1", "kind": "click", "label": "Search", "value": "", "current_value": ""}]
    assert marker(_obs(actions=a)) == marker(_obs(actions=a))


def test_marker_changes_when_a_label_changes():
    a1 = [{"id": "click:1", "kind": "click", "label": "Search", "value": "", "current_value": ""}]
    a2 = [{"id": "click:1", "kind": "click", "label": "Copilot", "value": "", "current_value": ""}]
    assert marker(_obs(actions=a1)) != marker(_obs(actions=a2))


def test_marker_ignores_geometry_correctly():
    """Geometry is not part of the marker, so a pure scroll/animation does not
    invalidate a decision. This is the property that avoids the 25% slowdown the
    official runtime measured when it counted DOM mutations."""
    a1 = [{"id": "click:1", "kind": "click", "label": "Search", "value": "", "current_value": "",
           "rect": {"x": 1, "y": 2}}]
    a2 = [{"id": "click:1", "kind": "click", "label": "Search", "value": "", "current_value": "",
           "rect": {"x": 99, "y": 88}}]
    assert marker(_obs(actions=a1)) == marker(_obs(actions=a2))


def test_marker_changes_when_field_value_changes():
    a1 = [{"id": "fill:1", "kind": "fill", "label": "Search", "value": "", "current_value": ""}]
    a2 = [{"id": "fill:1", "kind": "fill", "label": "Search", "value": "x", "current_value": "x"}]
    assert marker(_obs(actions=a1)) != marker(_obs(actions=a2))


# --- no-progress / repeat ----------------------------------------------------

def _steps(*pairs):
    return [{"page_changed": c, "kind": k, "operation": o, "target": t}
            for c, k, o, t in pairs]


def test_no_progress_detected():
    traj = _steps((False, "click", "CLICK", "1")) * 4
    assert detect_no_progress(traj) is True


def test_wait_steps_do_not_count_as_progress():
    traj = _steps((False, "wait", "WAIT", None)) * 4
    assert detect_no_progress(traj) is False


def test_progress_resets_the_guard():
    traj = _steps((False, "click", "CLICK", "1"), (True, "click", "CLICK", "2"),
                  (False, "click", "CLICK", "3"), (False, "click", "CLICK", "4"))
    assert detect_no_progress(traj) is False


def test_repeat_detected():
    traj = _steps((False, "click", "CLICK", "7")) * 3
    assert detect_repeat(traj) is True


def test_repeat_not_triggered_on_variation():
    traj = _steps((False, "click", "CLICK", "7"), (False, "click", "CLICK", "8"),
                  (False, "click", "CLICK", "7"))
    assert detect_repeat(traj) is False


# --- bot challenge -----------------------------------------------------------

def test_bot_challenge_detected():
    assert is_bot_challenge("https://www.google.com/sorry/index?continue=x", "text")
    assert is_bot_challenge("https://x.com/", "Our systems have detected unusual traffic")
    assert is_bot_challenge("https://x.com/", "complete the following challenge")
    assert is_bot_challenge("https://x.com/", "verify you are not a robot")


def test_normal_page_is_not_a_challenge():
    assert not is_bot_challenge("https://en.wikipedia.org/wiki/Python", "Python is a language")
