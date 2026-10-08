"""The end-to-end agent loop: observe -> Laya decides -> execute -> repeat.

Deliberately close to jev-ultrafast's loop (``agent.py``) so the evaluation
measures a real architecture:

* a goal in natural language drives every step;
* Laya answers an ``operation`` question plus one speculative ``*_target`` head
  per operation in a single request;
* only the target head matching the chosen operation is consumed;
* typed values come from an optional text model, never from hard-coding;
* the run stops on DONE/BLOCKED, a step budget, or repeated no-progress.

Every step is recorded with the decision, the model's confidence and the
executed action, so success can be checked independently afterwards.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from benchmark.browser_request import build_request

from . import executor, observer
from .reference_validators import (
    InvalidAnswer,
    InvalidOperation,
    ValidationError,
    detect_no_progress,
    detect_repeat,
    normalize_operation,
    resolve_target,
)

MAX_STEPS = 25
# Consecutive invalid decisions (a target key or operation the model was not
# offered) before the run is abandoned. Distinct from no-progress: here the page
# never even moved because nothing executable was chosen.
MAX_INVALID_STREAK = 3


@dataclass
class Step:
    n: int
    operation: str
    operation_confidence: float
    target: Optional[str]
    target_label: Optional[str]
    kind: Optional[str]
    text: Optional[str]
    url: str
    title: str
    latency_ms: float
    outcome: str  # executed | stale | failed | done | blocked
    page_changed: Optional[bool] = None


@dataclass
class RunResult:
    goal: str
    success: bool = False
    status: str = "incomplete"
    steps: List[Step] = field(default_factory=list)
    verified: Optional[bool] = None
    verification: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    total_ms: float = 0.0

    def summary(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "success": self.success,
            "status": self.status,
            "verified": self.verified,
            "steps": len(self.steps),
            "total_ms": round(self.total_ms),
            "error": self.error,
            "verification": self.verification,
        }


class Agent:
    def __init__(
        self,
        model,
        *,
        text_model: Optional[Callable[[Dict[str, Any]], str]] = None,
        max_steps: int = MAX_STEPS,
        max_operation_requests: int = 60,
        on_step: Optional[Callable[[Step], None]] = None,
        keep_screenshots: bool = False,
        screenshot_dir: Optional[str] = None,
    ):
        self.model = model                # .predict(state, questions) -> answers
        self.text_model = text_model      # (context) -> text, or None
        self.max_steps = max_steps
        self.max_operation_requests = max_operation_requests
        self.on_step = on_step
        self.keep_screenshots = keep_screenshots
        self.screenshot_dir = screenshot_dir

    def run(self, page, goal: str) -> RunResult:
        result = RunResult(goal=goal)
        history: List[Dict[str, Any]] = []
        started = time.perf_counter()
        requests = 0
        recent: List[Dict[str, Any]] = []
        invalid_streak = 0

        try:
            obs = observer.observe(page)
        except Exception as exc:  # noqa: BLE001
            result.error = f"initial observe failed: {exc}"
            return result

        for step_no in range(1, self.max_steps + 1):
            prev_marker = obs.get("marker")
            # --- decide ---------------------------------------------------
            page_obj = {
                "url": obs["url"],
                "title": obs["title"],
                "text": obs["text"],
                "actions": obs["actions"],
            }
            state, questions, targets, controls = build_request(page_obj, goal, history)

            if requests >= self.max_operation_requests:
                result.status = "budget"
                break
            t0 = time.perf_counter()
            try:
                answers = self.model.predict(state, questions)
            except Exception as exc:  # noqa: BLE001
                result.error = f"model error: {str(exc)[:200]}"
                break
            latency = (time.perf_counter() - t0) * 1000
            requests += 1

            op_ans = answers.get("operation", {})
            try:
                operation = normalize_operation(op_ans.get("choice"), targets, controls)
                op_conf = float(op_ans.get("probabilities", {}).get(op_ans.get("choice"), 0.0))
            except InvalidOperation as exc:
                # The model answered outside the offered vocabulary: a harness or
                # model-contract problem, not something to execute blindly. Count
                # it toward the invalid guard so a persistently-broken model stops
                # instead of burning the whole step budget.
                step = Step(step_no, str(op_ans.get("choice")), 0.0, None, None, None, None,
                            obs["url"], obs["title"], latency, f"invalid-operation: {exc}")
                result.steps.append(step)
                self._emit(step)
                invalid_streak += 1
                if invalid_streak >= MAX_INVALID_STREAK:
                    result.status = "invalid-decisions"
                    result.error = f"{invalid_streak} consecutive invalid decisions; stopping"
                    break
                obs = observer.observe(page)
                continue

            # --- resolve target (only the head matching the operation) -----
            action = None
            target_key = None
            if operation in controls:
                action = controls[operation]        # page-level: wait/scroll/enter
            elif operation not in ("DONE", "BLOCKED"):
                target_key, action = resolve_target(operation, answers, targets)
                if action is None:
                    step = Step(step_no, operation, op_conf, target_key, None, None, None,
                                obs["url"], obs["title"], latency, "invalid-target")
                    result.steps.append(step)
                    self._emit(step)
                    invalid_streak += 1
                    if invalid_streak >= MAX_INVALID_STREAK:
                        result.status = "invalid-decisions"
                        result.error = f"{invalid_streak} consecutive invalid decisions; stopping"
                        break
                    obs = observer.observe(page)
                    continue

            step = Step(step_no, operation, op_conf, target_key,
                        action["label"] if action else None,
                        action["kind"] if action else None, None,
                        obs["url"], obs["title"], latency, "pending")

            # --- terminal -------------------------------------------------
            if operation == "DONE":
                step.outcome = "done"
                result.steps.append(step)
                self._emit(step)
                result.status = "done"
                break
            if operation == "BLOCKED":
                step.outcome = "blocked"
                result.steps.append(step)
                self._emit(step)
                result.status = "blocked"
                break

            # --- typed value ----------------------------------------------
            text = None
            if action and action["kind"] == "fill":
                if self.text_model is None:
                    step.outcome = "no-text-model"
                    result.steps.append(step)
                    self._emit(step)
                    result.status = "blocked"
                    break
                try:
                    text = self.text_model({
                        "goal": goal,
                        "field": {"label": action["label"], "role": action.get("role"),
                                  "value": action.get("current_value", "")},
                        "page": {"title": obs["title"], "text": obs["text"][:1500]},
                        "recent_actions": [h.get("action") for h in history[-6:]],
                    })
                except Exception as exc:  # noqa: BLE001
                    step.outcome = f"text-error: {str(exc)[:60]}"
                    result.steps.append(step)
                    self._emit(step)
                    break
                step.text = text

            # --- execute --------------------------------------------------
            try:
                executor.act(page, action, obs, text=text)
                step.outcome = "executed"
                invalid_streak = 0      # only a step that actually ran clears the streak
            except executor.StalePage as exc:
                step.outcome = f"stale: {str(exc)[:60]}"
            except executor.ActionFailed as exc:
                step.outcome = f"failed: {str(exc)[:60]}"

            result.steps.append(step)
            self._emit(step)
            history.append({
                "action": action["label"] if action else operation,
                "kind": action["kind"] if action else operation.lower(),
                "text": text,
                "page_changed": None,      # filled in after the re-observation below
            })

            # --- re-observe -----------------------------------------------
            try:
                obs = observer.observe(page)
            except Exception as exc:  # noqa: BLE001
                result.error = f"observe failed after step: {exc}"
                break

            # record whether the page actually moved (this drives the guards)
            changed = obs.get("marker") != prev_marker
            step.page_changed = changed
            if history:
                history[-1]["page_changed"] = changed

            # --- no-progress / repeat guards ------------------------------
            # A click that changes nothing, a challenge page, a disabled control:
            # all leave the marker fixed. Stop rather than burn the budget
            # repeating one action -- the earlier baseline loop did exactly that.
            recent.append({"page_changed": changed, "kind": action["kind"] if action else operation.lower(),
                           "operation": operation, "target": target_key})
            if detect_no_progress(recent):
                result.status = "no-progress"
                result.error = "page unchanged across 4 steps; stopping"
                break
            if detect_repeat(recent):
                result.status = "repeat-loop"
                result.error = "same operation+target repeated 3x; stopping"
                break
        else:
            result.status = "max-steps"

        result.total_ms = (time.perf_counter() - started) * 1000
        return result

    def _emit(self, step: Step) -> None:
        if self.on_step:
            try:
                self.on_step(step)
            except Exception:  # noqa: BLE001
                pass
