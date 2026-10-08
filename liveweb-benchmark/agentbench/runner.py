"""CLI orchestration: browser lifecycle, the agent loop, verification, reports.

    # smoke-test the browser + observer against the live web (no model):
    python -m agentbench.runner --dry-run google-ai-openai

    # full run against the remote inference service
    python -m agentbench.runner --base-url http://10.144.144.2:8000

Anti-challenge defaults (all reversible via flags):

* **headed** (``--headless`` to opt back out) -- Google's /search risk-flags
  headless far more often even with a stealth binary;
* **warm session** (``--fresh-session`` to opt out) -- ONE browser, context and
  page for the whole run, so the site sees a continuous session with history
  instead of a fresh stranger per task; the fingerprint seed is fixed across
  runs (``--fingerprint N`` to pin another, ``--fingerprint-random`` to randomize);
* **geoip** (``--no-geoip`` to opt out) -- locale/timezone resolved from the
  actual exit IP instead of hardcoded America/New_York;
* **careful humanization** (``--human-preset default`` to opt out) with idle
  pauses between actions;
* challenge pages get a short wait-and-reobserve window (``--challenge-wait``)
  before the run is declared blocked -- JS-checkpoint walls often self-clear.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import browser as browser_mod
from . import report as report_mod
from . import traindata as traindata_mod
from .decision_client import DecisionClient
from .loop import Agent, RunResult
from .observe import observe
from .tasks import TASKS, Task, by_source, get
from .text_model import text_provider_for
from .verify import verify

DEFAULT_BASE_URL = "http://10.144.144.2:8000"
SESSION_SEED_KEY = "liveweb-session"   # stable identity for the warm session


def taskgen_mix_names():
    """Archetype-mix preset names, for --gen-mix choices."""
    from . import taskgen
    return taskgen.MIX_PRESETS.keys()


def _observe_flags(args) -> Dict[str, Any]:
    return {"filter_occluded": not args.no_filter_occluded,
            "filter_chrome": args.filter_chrome}


def run_task(page, model, task: Task, *, max_steps: int, verbose: bool,
             challenge_wait_s: float = 6.0, done_gate=None, rescue=None,
             observe_flags: Optional[Dict[str, Any]] = None) -> tuple:
    """Run one task. Returns (RunResult, verdict, distillation cases)."""
    text_model = text_provider_for(task.queries) if task.queries else None
    observe_fn = partial(observe, **(observe_flags or {}))
    sink = traindata_mod.CaseSink(task.task_id)

    def on_step(step):
        if verbose:
            print(f"    [{step.step:>2}] {step.operation:<11} conf={step.operation_confidence:.2f} "
                  f"target={str(step.target_label or '-')[:40]:<40} -> {step.outcome}", flush=True)

    agent = Agent(model, text_model=text_model, max_steps=max_steps, on_step=on_step,
                  challenge_wait_s=challenge_wait_s, done_gate=done_gate,
                  rescue=rescue, observe_fn=observe_fn,
                  on_case=sink.add, task_id=task.task_id)
    result = agent.run(page, task.goal)

    # independent verification of the final page (spec §6)
    try:
        final = observe(page)
    except Exception as exc:  # noqa: BLE001
        final = {"url": getattr(page, "url", ""), "title": "", "text": ""}
        result.error = (result.error or "") + f" final observe: {exc}"

    verdict = verify(task, final)
    result.verified = bool(verdict["passed"])
    result.verification = {**verdict, "final_url": final.get("url"),
                            "final_title": (final.get("title") or "")[:80]}
    # success requires BOTH the agent reaching DONE and the page proving it
    result.success = bool(verdict["passed"]) and result.status == "done"
    return result, verdict, sink.finalize(result.verified)


def _launch_opts(args) -> Dict[str, Any]:
    return {
        "headless": args.headless,
        "humanize": not args.no_humanize,
        "human_preset": args.human_preset,
        "geoip": not args.no_geoip,
        "proxy": args.proxy,
    }


def dry_run(task: Task, args) -> int:
    """Open the start URL with the real browser and print the L0/L1 observation."""
    fingerprint = (args.fingerprint or browser_mod.fingerprint_for(SESSION_SEED_KEY)
                   if not args.fingerprint_random else None)
    opts = _launch_opts(args)
    print(f"[dry-run] task={task.task_id} start={task.start_url} "
          f"pin={browser_mod.pinned_version()} fingerprint={fingerprint} "
          f"headless={opts['headless']} geoip={opts['geoip']} "
          f"preset={opts['human_preset']}", flush=True)
    b = browser_mod.open_browser(fingerprint=fingerprint, **opts)
    try:
        ctx, page = browser_mod.new_page(b, geoip=opts["geoip"])
        browser_mod.goto(page, task.start_url)
        obs = observe(page, **_observe_flags(args))
        print(f"  url:    {obs['url']}")
        print(f"  title:  {obs['title']}")
        print(f"  challenge: {obs['challenge']}  signals: {obs['signals']}")
        print(f"  actions: {obs['count']}  (dropped={obs['dropped']})")
        print(f"  marker: {obs['marker']}")
        kinds: Dict[str, int] = {}
        for a in obs["actions"]:
            kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
        print(f"  kinds:  {kinds}")
        print("  first actions:")
        for a in obs["actions"][:25]:
            print(f"    {a['id']:<22} {a['kind']:<7} {a['label'][:60]}")
        print(f"  text head: {obs['text'][:300]!r}")
        if args.shots:
            Path(args.shots).mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(Path(args.shots) / f"dry-{task.task_id}.png"))
            print(f"  screenshot -> {args.shots}/dry-{task.task_id}.png")
        ctx.close()
    finally:
        b.close()
    return 0


def _shoot(page, args, task: Task) -> None:
    if args.shots:
        try:
            Path(args.shots).mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(Path(args.shots) / f"{task.task_id}.png"))
        except Exception:  # noqa: BLE001
            pass


def _record(records: List[Dict[str, Any]], task: Task, result: RunResult,
            verdict: Dict[str, Any], fingerprint) -> None:
    records.append({"task": task, "result": result, "verdict": verdict,
                    "verified": bool(verdict.get("passed")),
                    "success": bool(verdict.get("passed")) and result.status == "done",
                    "fingerprint": fingerprint})


def _run_on_page(page, client, task, args, done_gate=None, rescue=None) -> tuple:
    browser_mod.goto(page, task.start_url)
    result, verdict, cases = run_task(page, client, task, max_steps=args.max_steps,
                                      verbose=not args.quiet,
                                      challenge_wait_s=args.challenge_wait,
                                      done_gate=done_gate, rescue=rescue,
                                      observe_flags=_observe_flags(args))
    _shoot(page, args, task)
    return result, verdict, cases


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Live-web e2e benchmark for the Laya browser model")
    ap.add_argument("--base-url", default=os.environ.get("LIVEWEB_BASE_URL", DEFAULT_BASE_URL))
    ap.add_argument("--api-key", default=os.environ.get("INFER_API_KEY"))
    ap.add_argument("--task", action="append", help="run only this task id (repeatable)")
    ap.add_argument("--source", choices=["google", "github"], help="run only this source's tasks")
    ap.add_argument("--list-tasks", action="store_true")
    ap.add_argument("--dry-run", metavar="TASK_ID", help="browser+observer smoke test, no model")
    ap.add_argument("--max-steps", type=int, default=25)
    ap.add_argument("--headless", action="store_true",
                    help="run headless (default is headed -- much fewer bot walls)")
    ap.add_argument("--no-humanize", action="store_true", help="disable humanized input")
    ap.add_argument("--human-preset", default="careful", choices=["careful", "default"])
    ap.add_argument("--no-geoip", action="store_true",
                    help="keep hardcoded locale/timezone instead of exit-IP-aligned")
    ap.add_argument("--fresh-session", action="store_true",
                    help="fresh browser + context per task (old behavior) instead of one "
                         "warm session for the whole run")
    ap.add_argument("--fingerprint", type=int, default=None,
                    help="pin an explicit fingerprint seed for the warm session")
    ap.add_argument("--fingerprint-random", action="store_true",
                    help="random per-run identity (the default: a fixed seed burns "
                         "the identity on Google after a few runs)")
    ap.add_argument("--challenge-cooldown", type=float, default=45.0,
                    help="extra seconds to cool down after a bot-challenge task")
    ap.add_argument("--proxy", default=None, help="optional proxy for the browser (http/socks5)")
    ap.add_argument("--no-filter-occluded", action="store_true",
                    help="keep overlay-covered elements in the candidate table")
    ap.add_argument("--filter-chrome", action="store_true",
                    help="drop landmark navigation chrome (nav/header/footer/aside links) "
                         "from the candidate table -- A/B-gated: changes the distribution")
    ap.add_argument("--challenge-wait", type=float, default=6.0,
                    help="seconds to wait per retry when a challenge page appears (0 = none)")
    ap.add_argument("--vlm-base-url", default=None,
                    help="enable the DONE-gate VLM: OpenAI-compatible vision endpoint")
    ap.add_argument("--vlm-model", default=None, help="vision model id for the DONE gate")
    ap.add_argument("--vlm-api-key", default=os.environ.get("VLM_API_KEY"))
    ap.add_argument("--vlm-timeout", type=float, default=20.0)
    ap.add_argument("--generated", type=int, default=0,
                    help="run N freshly generated search-research tasks (persistent "
                         "registry guarantees no task ever repeats across runs)")
    ap.add_argument("--gen-seed", type=int, default=None,
                    help="reproducible sampling seed for the generator")
    ap.add_argument("--gen-mix", default=None, choices=list(taskgen_mix_names()),
                    help="archetype-mix preset for the generator (farm waves: 'trending')")
    ap.add_argument("--delay", type=float, default=8.0, help="seconds between tasks")
    ap.add_argument("--shots", help="directory to save a final screenshot per task")
    ap.add_argument("--out", default="results", help="output directory for reports")
    ap.add_argument("--timeout", type=int, default=120, help="per-request timeout (s)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.list_tasks:
        for t in TASKS:
            print(f"{t.task_id:<28} {t.source:<7} {t.goal[:70]}")
        return 0

    if args.dry_run:
        return dry_run(get(args.dry_run), args)

    tasks: List[Task] = [get(t) for t in args.task] if args.task else (
        by_source(args.source) if args.source else TASKS)
    if args.generated > 0:
        from . import taskgen
        gen = taskgen.generate(args.generated, seed=args.gen_seed, mix=args.gen_mix)
        if not gen:
            raise SystemExit("task generator could not produce fresh tasks "
                             "(registry exhausted?)")
        print(f"[liveweb] generated {len(gen)} fresh tasks "
              f"(mix={args.gen_mix or 'default'}, "
              f"registry {taskgen.remaining_space()['used_tasks']} used)", flush=True)
        for t in gen:
            print(f"  {t.task_id}  {t.goal[:80]}", flush=True)
        # explicit --task/--source selections still run; otherwise replace the
        # builtin suite entirely with the generated batch
        tasks = tasks + gen if (args.task or args.source) else gen

    client = DecisionClient(args.base_url, api_key=args.api_key, timeout=args.timeout)
    print(f"[liveweb] backend: {args.base_url}", flush=True)
    health = client.health()
    if not args.quiet:
        print(f"[liveweb] health: {json.dumps(health, ensure_ascii=False)}", flush=True)

    done_gate, rescue_fn = None, None
    if args.vlm_base_url and args.vlm_model:
        from .vlm import VisionJudge, make_done_gate, make_rescue
        judge = VisionJudge(args.vlm_base_url, args.vlm_model,
                            api_key=args.vlm_api_key, timeout=args.vlm_timeout)
        done_gate = make_done_gate(judge)
        rescue_fn = make_rescue(judge)
        print(f"[liveweb] DONE-gate + rescue VLM: {args.vlm_model} @ {args.vlm_base_url}",
              flush=True)
    elif args.vlm_base_url or args.vlm_model:
        print("[liveweb] VLM disabled: needs both --vlm-base-url and --vlm-model",
              flush=True)

    opts = _launch_opts(args)
    warm = not args.fresh_session
    # default: a FRESH identity per run (stable within the run). A fixed
    # cross-run seed measurably burns the identity on Google after a few
    # consecutive runs -- the risk score sticks to fingerprint+IP.
    session_fp = (args.fingerprint if args.fingerprint is not None
                  else random.randint(10000, 99999))
    mode = "warm-session" if warm else "fresh-per-task"
    print(f"[liveweb] browser: pin={browser_mod.pinned_version()} mode={mode} "
          f"fingerprint={session_fp if warm else 'per-task'} "
          f"headless={opts['headless']} geoip={opts['geoip']} "
          f"humanize={opts['humanize']}/{opts['human_preset']}", flush=True)

    out_dir = Path(args.out) / (time.strftime("%Y%m%d-%H%M%S") + f"-{os.getpid() % 10000:04d}")
    out_dir.mkdir(parents=True, exist_ok=True)
    traindata_path = out_dir / "traindata.jsonl"
    total_cases = 0
    meta = {
        "base_url": args.base_url,
        "browser_version": browser_mod.pinned_version(),
        "session": mode,
        "fingerprint": session_fp if warm else "per-task",
        "humanize": opts["humanize"],
        "human_preset": opts["human_preset"],
        "geoip": opts["geoip"],
        "headless": opts["headless"],
        "challenge_wait_s": args.challenge_wait,
        "observe_filters": _observe_flags(args),
        "done_gate": {"model": args.vlm_model, "base_url": args.vlm_base_url}
        if done_gate is not None else None,
        "max_steps": args.max_steps,
        "delay": args.delay,
        "backend": health,
    }

    records: List[Dict[str, Any]] = []
    shared: Optional[tuple] = None   # (browser, ctx, page) for the warm session
    try:
        if warm:
            b = browser_mod.open_browser(fingerprint=session_fp, **opts)
            ctx, page = browser_mod.new_page(b, geoip=opts["geoip"])
            shared = (b, ctx, page)

        for i, task in enumerate(tasks):
            print(f"\n=== [{i+1}/{len(tasks)}] {task.task_id} ===", flush=True)
            print(f"  goal: {task.goal}", flush=True)
            fp = session_fp if warm else (
                None if args.fingerprint_random else browser_mod.fingerprint_for(task.task_id))
            print(f"  fingerprint: {fp}", flush=True)

            result: RunResult
            verdict: Dict[str, Any]
            cases: List[Dict[str, Any]] = []
            try:
                if warm:
                    result, verdict, cases = _run_on_page(page, client, task, args,
                                                         done_gate, rescue_fn)
                else:
                    b = browser_mod.open_browser(fingerprint=fp, **opts)
                    try:
                        ctx, page = browser_mod.new_page(b, geoip=opts["geoip"])
                        result, verdict, cases = _run_on_page(page, client, task, args,
                                                             done_gate, rescue_fn)
                        ctx.close()
                    finally:
                        b.close()
            except Exception as exc:  # noqa: BLE001 -- browser/launch failures
                result = RunResult(goal=task.goal, error=f"{type(exc).__name__}: {exc}")
                verdict = {"passed": False, "reason": "harness error", "checks": {}}

            total_cases += traindata_mod.append_jsonl(traindata_path, cases)

            _record(records, task, result, verdict, fp)
            print(f"  -> status={result.status} verified={verdict.get('passed')} "
                  f"success={records[-1]['success']} steps={len(result.steps)} "
                  f"{(result.error or '')[:80]}", flush=True)

            if i < len(tasks) - 1 and args.delay > 0:
                time.sleep(args.delay)
            # a challenged identity needs a cooldown before the next task hits
            # the same site, or the wall follows for every subsequent task
            if i < len(tasks) - 1 and result.bot_challenge and args.challenge_cooldown > 0:
                print(f"  [cooldown {args.challenge_cooldown:.0f}s after bot-challenge]",
                      flush=True)
                time.sleep(args.challenge_cooldown)
    finally:
        if shared is not None:
            b, ctx, _ = shared
            for closer in (ctx.close, b.close):
                try:
                    closer()
                except Exception:  # noqa: BLE001
                    pass

    out = report_mod.write_report(out_dir, meta, records)
    summary = report_mod.summarize(records)
    summary["traindata_cases"] = total_cases
    print("\n" + json.dumps(summary, indent=1, ensure_ascii=False), flush=True)
    print(f"report -> {out}/report.md (json alongside)", flush=True)
    if total_cases:
        print(f"distillation data -> {traindata_path} ({total_cases} cases: "
              "rescue=always, model-step=verified runs only)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
