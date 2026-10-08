"""Independent verifier (spec §6): the model's DONE is never the success signal.

After each run the final page observation is checked against the task's
expectations. A model that declares DONE on the search box fails; a bot
challenge is a failed run for *every* task, checked before anything else.
"""

from __future__ import annotations

from typing import Any, Dict

from .tasks import Task
from .validators import is_bot_challenge


def verify(task: Task, page: Dict[str, Any]) -> Dict[str, Any]:
    """Check the final page observation. Returns {passed, reason, checks}."""
    text = (page.get("text") or "").lower()
    title = (page.get("title") or "").lower()
    url = (page.get("url") or "").lower()
    haystack = f"{url}\n{title}\n{text}"

    checks: Dict[str, Any] = {"url": url[:120]}

    # 1. A bot challenge is a failed run, not a satisfied goal -- check first.
    blocked = is_bot_challenge(url, text)
    checks["bot_challenge"] = blocked
    if blocked:
        return {"passed": False, "reason": "bot_challenge", "checks": checks}

    # 2. Every any-of group must have >= 1 hit.
    missing: list = []
    for i, group in enumerate(task.require_any):
        hit = [g for g in group if g.lower() in haystack]
        checks[f"group{i}"] = hit
        if not hit:
            missing.append(group)
    if missing:
        return {"passed": False, "reason": f"missing evidence: {missing}", "checks": checks}

    # 3. None of the forbidden strings may appear.
    forbidden = [f for f in task.forbid if f.lower() in haystack]
    checks["forbidden_found"] = forbidden
    if forbidden:
        return {"passed": False, "reason": f"forbidden content: {forbidden}", "checks": checks}

    # 4. URL expectations.
    if task.expect_url_contains and task.expect_url_contains.lower() not in url:
        return {"passed": False,
                "reason": f"url lacks {task.expect_url_contains!r}",
                "checks": checks}
    for bad in task.expect_url_not_contains:
        if bad.lower() in url:
            return {"passed": False,
                    "reason": f"url still contains {bad!r}",
                    "checks": checks}

    return {"passed": True, "reason": "ok", "checks": checks}
