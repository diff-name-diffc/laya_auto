"""Executor guard tests with a stub page -- no browser needed.

The element paths (click/fill/select) go through `fresh()`, which needs a live
JS context; those are exercised by the dry-run and live runs. What is testable
headlessly is the URL plumbing both freshness checks share, and the `enter`
control's URL guard.
"""

from types import SimpleNamespace

import pytest

from agentbench.executor import StalePage, act, url_fresh


class FakePage:
    """Just enough page for the URL probes and the enter path."""

    def __init__(self, url=None, raise_eval=False):
        self.url = url
        self.raise_eval = raise_eval
        self.presses = []
        self.keyboard = SimpleNamespace(press=lambda k: self.presses.append(k))

    def evaluate(self, script, *args):
        if self.raise_eval:
            raise RuntimeError("execution context was destroyed")
        return None if self.url is None else {"url": self.url, "title": "t"}


class TestUrlFresh:
    def test_match(self):
        assert url_fresh(FakePage(url="https://x/"), {"url": "https://x/"})

    def test_mismatch(self):
        assert not url_fresh(FakePage(url="https://x/b"), {"url": "https://x/a"})

    def test_mid_navigation_is_stale(self):
        # document.body absent (evaluate returns None) -> fail closed
        assert not url_fresh(FakePage(url=None), {"url": "https://x/"})

    def test_context_destroyed_is_stale(self):
        assert not url_fresh(FakePage(raise_eval=True), {"url": "https://x/"})


class TestEnterGuard:
    DECISION_STATE = {"url": "https://www.google.com/", "marker": "m"}

    def test_enter_fires_when_url_unchanged(self):
        page = FakePage(url="https://www.google.com/")
        act(page, {"kind": "enter"}, self.DECISION_STATE)
        assert page.presses == ["Enter"]

    def test_enter_refused_after_navigation(self):
        # the focused-field assumption must not leak across a navigation
        page = FakePage(url="https://www.google.com/search?q=x")
        with pytest.raises(StalePage, match="URL changed"):
            act(page, {"kind": "enter"}, self.DECISION_STATE)
        assert page.presses == []

    def test_enter_refused_mid_navigation(self):
        page = FakePage(url=None)
        with pytest.raises(StalePage):
            act(page, {"kind": "enter"}, self.DECISION_STATE)
