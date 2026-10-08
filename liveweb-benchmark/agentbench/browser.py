"""CloakBrowser integration: free pinned build, humanized, per-task identity.

Free-tier facts (checked against the CloakBrowser repo, 2026-09):

* the "v146 free" tier has **no darwin assets** -- the free macOS build is
  Chromium ``145.0.7632.109.2`` (26 patches); Linux/Windows free is
  ``146.0.7680.177.5``. We pin per-platform so the binary never drifts to a
  Pro-only version;
* keyless use (no ``cloakbrowser login``) keeps the pin, needs no GitHub key,
  and has no server-side session cap;
* ``launch()`` returns a genuine Playwright ``Browser``; with ``humanize=True``
  the click/fill/type paths are humanized (fill = click + select-all + typed
  characters, with configurable typo-and-correct behaviour);
* fingerprint seed is the Chrome arg ``--fingerprint=N`` -- we derive a stable
  seed per task id so runs are comparable across repetitions;
* CloakBrowser's README advises avoiding ``page.wait_for_timeout`` (a detectable
  CDP round trip) -- we shadow it on each page with a plain ``time.sleep``.

Known limitation: ``mouse.wheel`` (the executor's scroll) is not humanized by
CloakBrowser; scrolls stay raw Playwright.
"""

from __future__ import annotations

import glob
import os
import subprocess
import sys
import time
import zlib
from typing import Any, Dict, Optional, Tuple

# The free (keyless) pinned builds, per platform -- see module docstring.
FREE_PIN = {
    "darwin": "145.0.7632.109.2",
    "linux": "146.0.7680.177.5",
    "win32": "146.0.7680.177.5",
}

VIEWPORT = {"width": 1120, "height": 780}
LOCALE = "en-US"
TIMEZONE = "America/New_York"


def pinned_version() -> str:
    key = "darwin" if sys.platform.startswith("darwin") else sys.platform
    return FREE_PIN.get(key, FREE_PIN["linux"])


def fingerprint_for(task_id: str) -> int:
    """A stable fingerprint seed per task id (10000..99999)."""
    return 10000 + (zlib.crc32(task_id.encode("utf-8")) % 90000)


def _darwin_gatekeeper_fix() -> None:
    """Best-effort: clear the quarantine flag CloakBrowser's README says blocks
    the first launch of its ad-hoc signed binary on macOS."""
    if not sys.platform.startswith("darwin"):
        return
    for app in glob.glob(os.path.expanduser("~/.cloakbrowser/chromium-*/Chromium.app")):
        try:
            subprocess.run(["xattr", "-cr", app], check=False, capture_output=True, timeout=30)
        except Exception:  # noqa: BLE001 -- advisory only
            pass


def open_browser(
    *,
    headless: bool = False,
    humanize: bool = True,
    human_preset: str = "careful",
    human_config: Optional[Dict[str, Any]] = None,
    fingerprint: Optional[int] = None,
    proxy: Optional[str] = None,
    geoip: bool = False,
) -> Any:
    """Launch the pinned free CloakBrowser. Returns a Playwright Browser.

    Anti-challenge posture (beyond the binary-level stealth):

    * ``human_preset="careful"`` + ``idle_between_actions`` -- slower, more
      deliberate human behaviour between consecutive actions;
    * ``geoip=True`` -- resolves the *actual* exit IP (through the system
      TUN/proxy) and aligns the fingerprint's timezone/locale to it. A
      hardcoded America/New_York against a mismatched exit IP is a classic
      risk-score signal;
    * a stable fingerprint seed lets one identity accumulate session history
      across steps/runs instead of appearing as a fresh stranger every task.
    """
    try:
        from cloakbrowser import launch
    except ImportError as exc:
        raise RuntimeError(
            "cloakbrowser is not installed; run: pip install 'cloakbrowser[geoip]>=0.5'"
        ) from exc

    _darwin_gatekeeper_fix()

    args: list = []
    if fingerprint is not None:
        args.append(f"--fingerprint={int(fingerprint)}")
    kwargs: Dict[str, Any] = {
        "browser_version": pinned_version(),
        "headless": headless,
        "humanize": humanize,
        "human_preset": human_preset,
    }
    if humanize and human_config is None:
        human_config = {"idle_between_actions": True}
    if human_config:
        kwargs["human_config"] = human_config
    if geoip:
        # geoip resolves tz/locale from the exit IP itself; passing explicit
        # locale/timezone alongside would fight it
        kwargs["geoip"] = True
    else:
        kwargs["locale"] = LOCALE
        kwargs["timezone"] = TIMEZONE
    if args:
        kwargs["args"] = args
    if proxy:
        kwargs["proxy"] = proxy
    # The ~200 MB pinned binary downloads once, then caches under ~/.cloakbrowser.
    return launch(**kwargs)


def new_page(browser: Any, geoip: bool = False) -> Tuple[Any, Any]:
    """Create a context + page with the benchmark's viewport.

    ``page.wait_for_timeout`` is shadowed with a client-side sleep: CloakBrowser
    flags the Playwright CDP round trip behind it as a detection signal.
    With ``geoip`` the fingerprint args own locale/timezone; a context-level
    override would reintroduce a mismatch, so none is set.
    Returns ``(context, page)`` -- the caller owns closing both.
    """
    ctx_kwargs: Dict[str, Any] = {"viewport": VIEWPORT}
    if not geoip:
        ctx_kwargs.update(locale=LOCALE, timezone_id=TIMEZONE)
    ctx = browser.new_context(**ctx_kwargs)
    page = ctx.new_page()
    page.set_default_timeout(20000)
    page.wait_for_timeout = lambda ms: time.sleep(ms / 1000.0)
    return ctx, page


def goto(page: Any, url: str, settle: float = 0.8) -> None:
    """Navigate to the task's start URL and let the page settle briefly."""
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(settle)
