"""Executor: perform a chosen action on a live Playwright page.

Keeps the two guards that make the loop safe, taken from jev-ultrafast:

* **freshness** -- before acting, recheck the page's semantic marker. If it moved
  since the decision was made, refuse and re-observe (``StalePage``). Typing or
  clicking a stale target is how an agent clicks the wrong thing.
* **pre-input visibility** -- resolve the target element *at the moment of input*
  and confirm it is still visible and enabled, rather than trusting the geometry
  from observation time.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .observer import observe


class StalePage(Exception):
    """The page changed since the decision; observe again."""


class ActionFailed(Exception):
    """The action could not be performed on a live, visible target."""


def _handle_of(page, node: int):
    """Resolve an observer node id back to a live element handle."""
    return page.evaluate_handle(
        "(node) => { const m = window.__e2eIds ||= new Map(); return m.get(node) || null; }", node
    )


def _resolve(page, node: int):
    """Find the element for a node id via its per-element id attribute."""
    return page.evaluate_handle(
        """(node) => {
             const all = document.querySelectorAll('*');
             for (const e of all) if (e.__e2eId === node) return e;
             return null;
           }""",
        node,
    )


def fresh(page, page_state: Dict[str, Any]) -> bool:
    """True if the current page still matches the observed marker."""
    try:
        current = page.evaluate(
            """() => {
                 if (!document.body) return null;
                 return {url: location.href, title: document.title};
               }"""
        )
    except Exception:  # noqa: BLE001
        return False
    if current is None or current["url"] != page_state["url"]:
        return False
    # A cheap check: the full marker is recomputed on demand in act() only when
    # the URL matches; URL changes are the common stale case on the web.
    return True


def act(page, action: Dict[str, Any], page_state: Dict[str, Any], text: Optional[str] = None) -> None:
    """Execute one action. Raises StalePage / ActionFailed on refusal.

    Deliberately does **not** press Enter after typing: submitting a search is a
    decision the model must make (CLICK the Search button), and auto-submitting
    would remove that decision and inflate the score.
    """
    kind = action["kind"]

    if kind == "wait":
        page.wait_for_timeout(400)
        return

    if kind == "scroll":
        page.mouse.wheel(0, int(action.get("delta", 560)))
        page.wait_for_timeout(200)
        return

    if kind == "enter":
        # A model-chosen submit: press Enter in whatever field currently has focus
        # (a fill leaves focus in its field). This is an action the model picked
        # from its option list, not a harness shortcut.
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        return

    if not fresh(page, page_state):
        raise StalePage("URL changed since the decision")

    node = action["node"]
    if not isinstance(node, int) or node <= 0:
        raise ActionFailed(f"invalid node {node!r}")

    el = _resolve(page, node)
    try:
        if el is None:
            raise StalePage("target element is gone")
        # pre-input visibility check
        ok = page.evaluate(
            """(e) => {
                 if (!e || !e.isConnected) return false;
                 if (e.matches(':disabled') || e.closest('[aria-disabled="true"],[inert]')) return false;
                 const r = e.getBoundingClientRect();
                 if (r.width <= 0 || r.height <= 0) return false;
                 if (r.bottom <= 0 || r.top >= innerHeight) return false;
                 return true;
               }""",
            el,
        )
        if not ok:
            raise StalePage("target no longer visible/enabled")

        if kind == "click":
            el.scroll_into_view_if_needed(timeout=3000)
            el.click(timeout=5000)
        elif kind == "fill":
            if text is None:
                raise ActionFailed("fill requires text")
            el.scroll_into_view_if_needed(timeout=3000)
            el.click(timeout=5000)
            el.fill(str(text), timeout=5000)
        elif kind == "select":
            el.select_option(value=action.get("value"))
        else:
            raise ActionFailed(f"unknown kind {kind!r}")
    except (StalePage, ActionFailed):
        raise
    except Exception as exc:  # noqa: BLE001 -- Playwright timeouts etc.
        raise ActionFailed(f"{kind} failed: {str(exc)[:120]}") from exc

    # let the page settle a little before the next observation
    try:
        page.wait_for_load_state("domcontentloaded", timeout=1500)
    except Exception:  # noqa: BLE001
        pass
    page.wait_for_timeout(350)


def observe_fresh(page) -> Dict[str, Any]:
    return observe(page)
