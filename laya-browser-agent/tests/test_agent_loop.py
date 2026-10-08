"""Loop-level tests: a scripted model drives the real agent against a real page.

These prove the integration works end to end -- the validators are wired into the
loop, not merely documented -- without needing the Laya model. Strategy:

* a scripted model returns a chosen operation/target;
* a real Playwright page (a `data:` URL, no network) is the environment;
* assertions are on the run's status and the recorded outcomes.

Every case here corresponds to a guarantee in AGENT_INTEGRATION_PROMPT.md §5, §8.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

pytest.importorskip("playwright", reason="playwright is not installed")

from e2e.agent import Agent, MAX_INVALID_STREAK  # noqa: E402

HTML = ("<html><body>"
        "<input id=q aria-label='Search'>"
        "<button id=go type=button>Search</button>"
        "<a href='#other'>Other</a>"
        "</body></html>")


@pytest.fixture()
def page():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        pg = browser.new_page()
        pg.goto("data:text/html," + HTML)
        pg.wait_for_timeout(250)
        yield pg
        browser.close()


def scripted(op: str, target: str, bad_distribution: bool = False):
    """A model that always answers the same way.

    ``bad_distribution`` makes the probabilities sum to 1.5, which the answer
    validator must reject -- the signature of a model that answered a different
    question than the one asked.
    """
    class M:
        def predict(self, state, questions):
            out = {}
            for qid, q in questions.items():
                keys = list(q["criteria"].keys())
                if qid == "operation":
                    pick = op if op in keys else keys[0]
                elif qid.endswith("_target"):
                    pick = target
                else:
                    pick = keys[0]
                if bad_distribution:
                    probs = {k: 1.5 / len(keys) for k in keys}   # sums to 1.5
                else:
                    probs = {k: (1.0 if k == pick else 0.0) for k in keys}
                out[qid] = {"type": "choice", "choice": pick, "probabilities": probs,
                            "confidence": 1.0}
            return out
    return M()


def test_done_terminates_immediately(page):
    r = Agent(scripted("DONE", "1"), max_steps=5).run(page, "x")
    assert r.status == "done"
    assert len(r.steps) == 1
    assert r.steps[0].outcome == "done"


def test_blocked_terminates(page):
    r = Agent(scripted("BLOCKED", "1"), max_steps=5).run(page, "x")
    assert r.status == "blocked"


def test_page_level_control_resolves_from_controls(page):
    """WAIT is a control, not a target head; it must resolve and execute."""
    r = Agent(scripted("WAIT", "1"), max_steps=2).run(page, "x")
    assert r.status in ("max-steps", "no-progress", "repeat-loop")
    assert all(s.outcome == "executed" for s in r.steps)


def test_invalid_target_key_is_rejected_and_run_stops(page):
    """A target key not among the offered criteria must never execute."""
    r = Agent(scripted("CLICK", "NOT-A-KEY"), max_steps=10).run(page, "x")
    assert any(s.outcome == "invalid-target" for s in r.steps)
    assert r.status == "invalid-decisions"
    assert len(r.steps) == MAX_INVALID_STREAK
    assert not any(s.outcome == "executed" for s in r.steps)


def test_unknown_operation_is_rejected_and_run_stops(page):
    class BadOp:
        def predict(self, state, questions):
            return {"operation": {"type": "choice", "choice": "TELEPORT",
                                  "probabilities": {k: 1.0 for k in questions["operation"]["criteria"]},
                                  "confidence": 1.0}}

    r = Agent(BadOp(), max_steps=10).run(page, "x")
    assert any("invalid-operation" in s.outcome for s in r.steps)
    assert r.status == "invalid-decisions"


def test_malformed_answer_is_rejected(page):
    """Probabilities that do not sum to 1 must be refused, never executed."""
    r = Agent(scripted("CLICK", "2", bad_distribution=True), max_steps=10).run(page, "x")
    assert not any(s.outcome == "executed" for s in r.steps)
    assert r.status == "invalid-decisions"


def test_repeated_noop_click_trips_a_guard(page):
    """Clicking a no-op button forever must stop, not exhaust the budget."""
    r = Agent(scripted("CLICK", "2"), max_steps=25).run(page, "x")
    assert r.status in ("repeat-loop", "no-progress")
    assert len(r.steps) < 25


def test_page_changed_is_recorded_from_real_observation(page):
    """The trajectory must carry the real page-change signal, not a constant."""
    r = Agent(scripted("CLICK", "2"), max_steps=6).run(page, "x")
    assert all(s.page_changed is not None for s in r.steps[:1]) or r.steps == []
    # a no-op click changes nothing
    assert all(s.page_changed is False for s in r.steps if s.outcome == "executed")
