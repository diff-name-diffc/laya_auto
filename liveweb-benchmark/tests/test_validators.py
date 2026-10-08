"""Unit tests for the pure validation layer (spec §5) -- no browser, no model."""

import pytest

from agentbench.validators import (
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


def _answer(keys, choice, base=0.9):
    """A well-formed choice answer over `keys` with `choice` as the argmax."""
    others = [k for k in keys if k != choice]
    probs = {k: (1.0 - base) / max(1, len(others)) for k in others}
    probs[choice] = base
    return {"type": "choice", "choice": choice, "probabilities": probs, "confidence": base}


class TestValidateQuestion:
    def test_choice_requires_nonempty_map(self):
        with pytest.raises(ValidationError):
            validate_question({"type": "choice", "criteria": {}, "instructions": "x"})

    def test_unknown_type_rejected(self):
        with pytest.raises(ValidationError):
            validate_question({"type": "essay", "criteria": {"a": "b"}, "instructions": "x"})

    def test_valid(self):
        validate_question({"type": "choice", "criteria": {"a": "b"}, "instructions": "x"})
        validate_question({"type": "score", "criteria": ["lo", "hi"], "instructions": "x"})


class TestValidateRequest:
    def test_elements_in_state_rejected(self):
        with pytest.raises(ValidationError, match="elements"):
            validate_request({"page": {}, "elements": [1, 2]}, {})

    def test_too_many_questions(self):
        questions = {f"q{i}": {"type": "noul", "instructions": "x"} for i in range(65)}
        with pytest.raises(RequestTooLarge):
            validate_request({}, questions)

    def test_state_too_large(self):
        with pytest.raises(RequestTooLarge):
            validate_request({"text": "x" * 60000}, {})


class TestValidateChoiceAnswer:
    KEYS = ["CLICK", "WAIT", "DONE"]

    def test_valid(self):
        ans = _answer(self.KEYS, "CLICK")
        assert validate_choice_answer(ans, self.KEYS) is ans

    def test_missing_probabilities(self):
        with pytest.raises(InvalidAnswer):
            validate_choice_answer({"choice": "CLICK"}, self.KEYS)

    def test_wrong_key_set(self):
        ans = _answer(self.KEYS, "CLICK")
        with pytest.raises(InvalidAnswer):
            validate_choice_answer(ans, ["CLICK", "WAIT", "BLOCKED"])

    def test_choice_not_in_keys(self):
        ans = _answer(self.KEYS, "CLICK")
        ans["choice"] = "NUKE"
        with pytest.raises(InvalidAnswer):
            validate_choice_answer(ans, self.KEYS)

    def test_not_argmax(self):
        probs = {"CLICK": 0.3, "WAIT": 0.6, "DONE": 0.1}  # sums to 1, CLICK is not argmax
        ans = {"type": "choice", "choice": "CLICK", "probabilities": probs, "confidence": 0.3}
        with pytest.raises(InvalidAnswer, match="argmax"):
            validate_choice_answer(ans, self.KEYS)

    def test_probabilities_do_not_sum_to_one(self):
        ans = _answer(self.KEYS, "CLICK")
        ans["probabilities"]["CLICK"] = 0.5
        with pytest.raises(InvalidAnswer, match="sum"):
            validate_choice_answer(ans, self.KEYS)

    def test_noul(self):
        assert validate_noul_answer({"noul": 0.4}) == 0.4
        with pytest.raises(InvalidAnswer):
            validate_noul_answer({"noul": 1.5})


class TestNormalizeOperation:
    TARGETS = {"CLICK": {}, "TYPE_TEXT": {}}
    CONTROLS = {"WAIT": {}, "SCROLL_DOWN": {}, "PRESS_ENTER": {}}

    def test_pass_through_and_membership(self):
        assert normalize_operation("DONE", self.TARGETS, self.CONTROLS) == "DONE"
        assert normalize_operation("BLOCKED", self.TARGETS, self.CONTROLS) == "BLOCKED"
        assert normalize_operation("CLICK", self.TARGETS, self.CONTROLS) == "CLICK"
        assert normalize_operation("wait", self.TARGETS, self.CONTROLS) == "WAIT"

    def test_unknown_rejected(self):
        with pytest.raises(InvalidOperation):
            normalize_operation("FLY", self.TARGETS, self.CONTROLS)
        with pytest.raises(InvalidOperation):
            normalize_operation(None, self.TARGETS, self.CONTROLS)


class TestResolveTarget:
    def test_consumes_only_matching_head(self):
        targets = {"CLICK": {"1": {"id": "click:1"}, "2": {"id": "click:2"}}}
        answers = {
            "click_target": _answer(["1", "2"], "2"),
            "type_text_target": _answer(["9"], "9"),  # bogus head, must be ignored
        }
        key, action = resolve_target("CLICK", answers, targets)
        assert (key, action) == ("2", {"id": "click:2"})

    def test_invalid_answer_yields_none(self):
        targets = {"CLICK": {"1": {"id": "click:1"}}}
        answers = {"click_target": _answer(["7", "8"], "7")}  # keys not offered
        assert resolve_target("CLICK", answers, targets) == (None, None)

    def test_terminal_has_no_target(self):
        assert resolve_target("DONE", {}, {}) == (None, None)


class TestMarkers:
    def test_identical_pages_same_marker(self):
        obs = {"url": "u", "title": "t", "text": "x",
               "actions": [{"id": "click:1", "kind": "click", "label": "A",
                            "value": "", "current_value": ""}]}
        assert marker(obs) == marker(dict(obs))

    def test_geometry_only_change_keeps_marker(self):
        base = {"url": "u", "title": "t", "text": "x",
                "actions": [{"id": "click:1", "kind": "click", "label": "A",
                             "value": "", "current_value": ""}]}
        moved = dict(base)
        # adding a geometry field (what animations do) must not change the marker
        moved["actions"] = [dict(base["actions"][0], rect=[9, 9, 9, 9])]
        assert marker(base) == marker(moved)

    def test_text_change_changes_marker(self):
        a = {"url": "u", "title": "t", "text": "x", "actions": []}
        b = {"url": "u", "title": "t", "text": "y", "actions": []}
        assert marker(a) != marker(b)


class TestGuards:
    def test_no_progress(self):
        traj = [{"page_changed": False, "kind": "click"} for _ in range(4)]
        assert detect_no_progress(traj)
        traj[-1]["page_changed"] = True
        assert not detect_no_progress(traj)
        # waits do not count as no-progress evidence
        waits = [{"page_changed": False, "kind": "wait"} for _ in range(4)]
        assert not detect_no_progress(waits)

    def test_repeat(self):
        traj = [{"operation": "CLICK", "target": "1"} for _ in range(3)]
        assert detect_repeat(traj)
        traj[1]["target"] = "2"
        assert not detect_repeat(traj)


class TestBotChallenge:
    def test_signatures(self):
        assert is_bot_challenge("https://www.google.com/sorry/index", "")
        assert is_bot_challenge("https://x/", "Our systems have detected unusual traffic")
        assert is_bot_challenge("https://x/", "please complete the following challenge")
        assert is_bot_challenge("https://x/", "确认您是真人")
        assert not is_bot_challenge("https://www.google.com/search?q=openai", "openai news results")
