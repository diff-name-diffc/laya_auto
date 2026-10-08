"""Run the Google research tasks in a real browser, end to end.

    # with the inference server running the browser fine-tune:
    python -m e2e.run --base-url http://127.0.0.1:8811
    python -m e2e.run --base-url http://127.0.0.1:8811 --task fact-capital --headed

Verification is independent of the agent: after each run the final page is
checked against the task's expectations (see ``tasks.py``). A model that says
DONE too early fails.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from .agent import Agent, RunResult
from .tasks import TASKS, Task, get, text_provider_for


class HttpModel:
    """Laya client over the running /v1/systemone server."""

    def __init__(self, base_url: str, api_key: str | None = None, timeout: int = 120):
        import urllib.request

        self._req = urllib.request
        self.url = base_url.rstrip("/") + "/v1/systemone"
        self.key = api_key
        self.timeout = timeout

    def predict(self, state, questions):
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        data = json.dumps({"state": state, "questions": questions}, ensure_ascii=False).encode("utf-8")
        req = self._req.Request(self.url, data=data, headers=headers)
        with self._req.urlopen(req, timeout=self.timeout) as resp:
            return json.load(resp)["answers"]


def run_task(page, model, task: Task, *, max_steps: int, verbose: bool, shots: str | None) -> RunResult:
    def on_step(step):
        if verbose:
            print(f"    [{step.n:>2}] {step.operation:<9} conf={step.operation_confidence:.2f} "
                  f"target={step.target_label or '-':<40.40} -> {step.outcome}", flush=True)

    agent = Agent(model, text_model=text_provider_for(task), max_steps=max_steps, on_step=on_step)
    result = agent.run(page, task.goal)

    # independent verification of the final page
    from .observer import observe

    try:
        final = observe(page)
    except Exception as exc:  # noqa: BLE001
        final = {"url": page.url, "title": "", "text": ""}
        result.error = (result.error or "") + f" final observe: {exc}"

    verdict = task.verify(final)
    result.verified = verdict["passed"]
    result.verification = {**verdict, "final_url": final.get("url"), "final_title": (final.get("title") or "")[:80]}
    # success requires BOTH the agent reaching DONE and the page actually showing it
    result.success = bool(verdict["passed"]) and result.status == "done"

    if shots:
        try:
            Path(shots).mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(Path(shots) / f"{task.task_id}.png"), full_page=False)
        except Exception:  # noqa: BLE001
            pass
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="End-to-end Google research evaluation in a real browser")
    ap.add_argument("--base-url", default="http://127.0.0.1:8811")
    ap.add_argument("--api-key", default=os.environ.get("INFER_API_KEY"))
    ap.add_argument("--task", action="append", help="run only this task id (repeatable)")
    ap.add_argument("--max-steps", type=int, default=25)
    ap.add_argument("--headed", action="store_true", help="show the browser window")
    ap.add_argument("--channel", default="chrome", help="browser channel (chrome | chromium)")
    ap.add_argument("--shots", help="directory to save a screenshot per task")
    ap.add_argument("--out", help="write the JSON report here")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--engine", default="google", choices=["google", "bing", "duckduckgo"],
                    help="search engine for the start page")
    ap.add_argument("--start-url", default=None,
                    help="override the start URL (default: the engine's home page)")
    ap.add_argument("--start-at-results", action="store_true",
                    help="start on the engine's results page for each task's first query, "
                         "isolating result-selection from the search-box step")
    args = ap.parse_args()

    tasks: List[Task] = [get(t) for t in args.task] if args.task else TASKS
    model = HttpModel(args.base_url, args.api_key)

    home = args.start_url or {
        "google": "https://www.google.com/",
        "bing": "https://www.bing.com/",
        "duckduckgo": "https://duckduckgo.com/",
    }[args.engine]

    from playwright.sync_api import sync_playwright

    report: Dict[str, Any] = {"base_url": args.base_url, "start_url": home, "engine": args.engine, "tasks": []}
    with sync_playwright() as p:
        # Google serves a bot challenge to a plainly-automated Chrome. Dropping
        # the AutomationControlled blink feature is the minimum that gets real
        # results; headless additionally needs --headless=new, which Playwright
        # sets for channel="chrome". Headed is the most reliable.
        browser = p.chromium.launch(
            channel=args.channel,
            headless=not args.headed,
            args=["--disable-blink-features=AutomationControlled"],
        )
        for task in tasks:
            print(f"\n=== {task.task_id} ===", flush=True)
            print(f"  goal: {task.goal}", flush=True)
            ctx = browser.new_context(
                viewport={"width": 1120, "height": 780},
                locale="en-US",
                timezone_id="America/New_York",
            )
            # hide the navigator.webdriver flag for the challenge check
            ctx.add_init_script(
                "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
            )
            page = ctx.new_page()
            page.set_default_timeout(20000)
            start = home
            if args.start_at_results:
                from .tasks import search_urls

                start = search_urls(args.engine, task.queries[0])
            try:
                page.goto(start, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(800)
                result = run_task(page, model, task, max_steps=args.max_steps,
                                  verbose=not args.quiet, shots=args.shots)
            except Exception as exc:  # noqa: BLE001
                result = RunResult(goal=task.goal, error=f"{type(exc).__name__}: {exc}")
            finally:
                ctx.close()

            rec = {"task_id": task.task_id, **result.summary()}
            report["tasks"].append(rec)
            print(f"  -> status={result.status} verified={result.verified} "
                  f"success={result.success} steps={len(result.steps)} "
                  f"{(result.error or '')[:80]}", flush=True)
        browser.close()

    n = len(report["tasks"])
    ok = sum(1 for t in report["tasks"] if t["success"])
    verified = sum(1 for t in report["tasks"] if t["verified"])
    report["summary"] = {
        "tasks": n,
        "success": ok,
        "success_rate": round(ok / n, 3) if n else 0.0,
        "independently_verified": verified,
    }
    print("\n" + json.dumps(report["summary"], indent=1), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=1, ensure_ascii=False))
        print(f"wrote {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
