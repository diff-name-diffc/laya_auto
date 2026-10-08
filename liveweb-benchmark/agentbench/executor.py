"""Executor: perform a chosen action on a live page (spec §5.3–§5.5).

Two guards make the loop safe:

* **freshness** -- before acting on an element, the page's semantic marker is
  recomputed and compared with the observation the decision was made on. The
  URL short-circuits the common case (navigation); when it matches, the FULL
  marker is recomputed -- the reference implementation skipped this and trusted
  URL equality alone, which lets a same-URL SPA swap execute stale decisions.
* **pre-input visibility** -- the target element is re-resolved *at the moment
  of input* and confirmed still connected, enabled and visible.

Waits use ``time.sleep`` rather than ``page.wait_for_timeout`` (CloakBrowser
flags the latter's CDP round trip as a detection signal). Scrolling uses raw
``mouse.wheel`` -- CloakBrowser does not humanize that method (known limitation,
README).
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from .observe import observe


class StalePage(Exception):
    """The page changed since the decision; observe again."""


class ActionFailed(Exception):
    """The action could not be performed on a live, visible target."""


def _resolve(page, node: int):
    """Find the element for a node id via its per-element identity property."""
    return page.evaluate_handle(
        """(node) => {
             const all = document.querySelectorAll('*');
             for (const e of all) if (e.__abId === node) return e;
             return null;
           }""",
        node,
    )


def _current_url(page) -> Optional[str]:
    """``location.href``, or None mid-navigation / without a body."""
    try:
        current = page.evaluate(
            """() => {
                 if (!document.body) return null;
                 return {url: location.href, title: document.title};
               }"""
        )
    except Exception:  # noqa: BLE001 -- navigation/context churn
        return None
    return None if current is None else current.get("url")


def url_fresh(page, page_state: Dict[str, Any]) -> bool:
    """Cheap freshness check for page-level controls: URL equality only."""
    return _current_url(page) == page_state.get("url")


def fresh(page, page_state: Dict[str, Any]) -> bool:
    """True if the page still matches the observed state (URL + full marker).

    §5.3: URL changes are the common stale case and short-circuit; otherwise the
    semantic marker is recomputed via a full observation and compared. The
    re-observation reuses the decision-time filter flags -- different filters
    produce different candidate sets and therefore different markers.
    """
    if _current_url(page) != page_state.get("url"):
        return False
    flags = dict(page_state.get("_filter") or {})
    try:
        now = observe(page, retries=2, settle_ms=150, **flags)
    except Exception:  # noqa: BLE001
        return False
    return now.get("marker") == page_state.get("marker")


def act(page, action: Dict[str, Any], page_state: Dict[str, Any], text: Optional[str] = None) -> None:
    """Execute one action. Raises StalePage / ActionFailed on refusal.

    Deliberately does **not** press Enter after typing: submitting a search is a
    decision the model must make (CLICK the Search button or PRESS_ENTER from
    its option list), and auto-submitting would remove that decision from the
    measurement.
    """
    kind = action["kind"]

    if kind == "wait":
        time.sleep(0.4)
        return

    if kind == "scroll":
        page.mouse.wheel(0, int(action.get("delta", 560)))
        time.sleep(0.2)
        return

    if kind == "enter":
        # A model-chosen submit: press Enter in whatever field currently has
        # focus (a fill leaves focus in its field). The URL guard keeps the
        # "focused field" assumption from leaking across a navigation; focus
        # itself is not represented in the marker, so same-URL focus drift
        # remains a known residual risk.
        if not url_fresh(page, page_state):
            raise StalePage("URL changed since the decision")
        page.keyboard.press("Enter")
        time.sleep(0.4)
        return

    if not fresh(page, page_state):
        raise StalePage("page changed since the decision (url or marker mismatch)")

    node = action["node"]
    if not isinstance(node, int) or node <= 0:
        raise ActionFailed(f"invalid node {node!r}")

    el = _resolve(page, node)
    try:
        if el is None:
            raise StalePage("target element is gone")
        # pre-input check, resolved at the moment of input. Returns a refusal
        # reason or 'ok'; the occlusion probe (elementFromPoint at the centre)
        # fails in ~10ms with an actionable reason instead of burning the 5s
        # Playwright actionability timeout on a covered element.
        reason = page.evaluate(
            """(e) => {
                 if (!e || !e.isConnected) return 'gone';
                 if (e.matches(':disabled') || e.closest('[aria-disabled="true"],[inert]')) return 'disabled';
                 const r = e.getBoundingClientRect();
                 if (r.width <= 0 || r.height <= 0) return 'invisible';
                 if (r.bottom <= 0 || r.top >= innerHeight) return 'offscreen';
                 const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
                 const hit = document.elementFromPoint(cx, cy);
                 if (!hit) return 'occluded';
                 if (hit !== e && !e.contains(hit) && !hit.contains(e)) return 'occluded';
                 return 'ok';
               }""",
            el,
        )
        if reason != "ok":
            # StalePage (not ActionFailed): a covered/displaced target should
            # force a re-observation -- a transient overlay then clears and the
            # element re-enters the candidate table on the next decision.
            raise StalePage(f"target {reason}")

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
    time.sleep(0.35)
