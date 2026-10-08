"""The end-to-end agent loop: observe -> decide -> execute -> repeat (spec §4).

Design notes, all traced to measured failures in the reference evaluation:

* the model answers an ``operation`` question plus one speculative ``*_target``
  head per operation in a single request; only the head matching the chosen
  operation is consumed (a 2x round trip if sequenced);
* **invalid decisions count toward a guard** that only a successfully executed
  step resets -- "operation valid but target invalid" must not reset the streak,
  and the invalid path must check the guard *before* continuing;
* a 413 from the server trims the candidate table and resends once (§3.2);
* a bot challenge observed at any step ends the run immediately as
  ``bot-challenge`` -- the model cannot progress on a captcha page, and burning
  25 steps there only pollutes the measurement;
* confidence below ``tau`` marks the step ``low_confidence`` and the element
  dirty. That is the (unimplemented) VLM side path's trigger interface: it arms
  the *next* step, never blocks this one (§2.4).

``observe_fn`` / ``act_fn`` are injectable so the whole loop is unit-testable
with a scripted fake model and fake observations, no browser, no network.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .executor import ActionFailed, StalePage, act as _default_act
from .observe import observe as _default_observe
from .request_builder import MIN_MAX_ACTIONS, build_request
from .validators import (
    InvalidAnswer,
    InvalidOperation,
    RequestTooLarge,
    detect_no_progress,
    detect_repeat,
    normalize_operation,
    resolve_target,
    validate_choice_answer,
)

MAX_STEPS = 25
# Consecutive invalid decisions (a target key or operation the model was not
# offered) before the run is abandoned. Distinct from no-progress: here the page
# never even moved because nothing executable was chosen.
MAX_INVALID_STREAK = 3
# Consecutive stale refusals (the page changed under every decision) before the
# run gives up: a continuously-animating page would otherwise burn the whole
# step budget on decisions that are correctly discarded. Correctness is never
# at stake -- nothing executes on a stale decision -- only budget.
MAX_STALE_STREAK = 4
# Confidence below this marks the step low-confidence / the element dirty (§5.6).
ESCALATE_TAU = 0.35
# A rejected DONE (VLM gate) is fed back as a corrective note and re-decided;
# after this many rejections the DONE is accepted (the gate advises, the loop
# must not wedge on a disagreeing verifier).
MAX_DONE_REJECTIONS = 2


def _any_filled(obs: Dict[str, Any]) -> bool:
    """True if any editable field currently holds text (Enter can submit it)."""
    for a in obs.get("actions", []):
        if a.get("kind") == "fill":
            if str(a.get("current_value") or a.get("value") or "").strip():
                return True
    return False

ObserveFn = Callable[[Any], Dict[str, Any]]
ActFn = Callable[[Any, Dict[str, Any], Dict[str, Any], Optional[str]], None]


@dataclass
class StepRecord:
    """One step of the trajectory (spec §3.6) -- audit input and loop guard input."""

    step: int
    operation: str
    operation_confidence: float
    target: Optional[str] = None
    target_label: Optional[str] = None
    kind: Optional[str] = None
    text: Optional[str] = None
    outcome: str = "pending"  # executed|stale|failed|invalid-target|invalid-operation|done|blocked
    page_changed: Optional[bool] = None
    latency_ms: float = 0.0
    low_confidence: bool = False
    url: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step, "operation": self.operation,
            "confidence": self.operation_confidence, "target": self.target,
            "target_label": self.target_label, "kind": self.kind, "text": self.text,
            "outcome": self.outcome, "page_changed": self.page_changed,
            "latency_ms": round(self.latency_ms, 1), "low_confidence": self.low_confidence,
            "url": self.url,
        }


@dataclass
class RunResult:
    goal: str
    success: bool = False
    status: str = "incomplete"
    steps: List[StepRecord] = field(default_factory=list)
    verified: Optional[bool] = None
    verification: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    total_ms: float = 0.0
    dirty_nodes: List[int] = field(default_factory=list)
    low_confidence_steps: int = 0
    bot_challenge: bool = False

    def summary(self) -> Dict[str, Any]:
        outcomes: Dict[str, int] = {}
        for s in self.steps:
            key = s.outcome.split(":")[0]
            outcomes[key] = outcomes.get(key, 0) + 1
        changed = [s.page_changed for s in self.steps if s.page_changed is not None]
        return {
            "goal": self.goal,
            "success": self.success,
            "status": self.status,
            "verified": self.verified,
            "steps": len(self.steps),
            "total_ms": round(self.total_ms),
            "error": self.error,
            "outcome_counts": outcomes,
            "page_changed_rate": round(sum(1 for c in changed if c) / len(changed), 3) if changed else None,
            "low_confidence_steps": self.low_confidence_steps,
            "vlm_rescues": sum(1 for s in self.steps if s.operation == "VLM_RESCUE"),
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
        on_step: Optional[Callable[[StepRecord], None]] = None,
        tau: float = ESCALATE_TAU,
        max_actions: int = 250,
        observe_fn: ObserveFn = _default_observe,
        act_fn: ActFn = _default_act,
        challenge_retries: int = 2,
        challenge_wait_s: float = 6.0,
        done_gate=None,
        rescue=None,
        max_rescues: int = 5,
        on_case=None,
        task_id: str = "task",
    ):
        self.model = model                # .predict(state, questions) -> answers
        self.text_model = text_model      # (context) -> text, or None
        self.max_steps = max_steps
        self.max_operation_requests = max_operation_requests
        self.on_step = on_step
        self.tau = tau
        self.max_actions = max_actions
        self.observe = observe_fn
        self.act = act_fn
        self.challenge_retries = challenge_retries
        self.challenge_wait_s = challenge_wait_s
        self.done_gate = done_gate  # (page, goal, obs) -> {satisfied, missing}
        self.rescue = rescue        # (page, goal, obs, problem) -> {"id", "text"?}
        self.max_rescues = max_rescues
        self.on_case = on_case      # distillation sink: (case dict) -> None
        self.task_id = task_id
        self._case_seq = 0

    def _emit_case(self, kind: str, goal: str, obs: Dict[str, Any],
                   history: List[Dict[str, Any]], action: Dict[str, Any],
                   rationale: str) -> None:
        if self.on_case is None:
            return
        from .traindata import make_case
        self._case_seq += 1
        try:
            case = make_case(kind, goal, obs, history, action, rationale,
                             self.task_id, self._case_seq)
            if case:
                self.on_case(case)
        except Exception:  # noqa: BLE001 -- data export never breaks the loop
            pass

    # -- main entry ------------------------------------------------------------

    def run(self, page, goal: str) -> RunResult:
        result = RunResult(goal=goal)
        history: List[Dict[str, Any]] = []
        dirty: set = set()
        started = time.perf_counter()
        requests = 0
        recent: List[Dict[str, Any]] = []
        invalid_streak = 0
        stale_streak = 0
        done_rejections = 0
        refused_empty = 0
        self.rescues_used = 0

        try:
            obs = self.observe(page)
        except Exception as exc:  # noqa: BLE001
            result.error = f"initial observe failed: {exc}"
            result.total_ms = (time.perf_counter() - started) * 1000
            return result

        if obs.get("challenge", {}).get("hit"):
            obs = self._wait_out_challenge(page, obs, result)
            if obs is None:
                result.status = "bot-challenge"
                result.bot_challenge = True
                result.total_ms = (time.perf_counter() - started) * 1000
                return result

        for step_no in range(1, self.max_steps + 1):
            if obs.get("challenge", {}).get("hit"):
                # JS-checkpoint challenges (Cloudflare-style) often clear on
                # their own once the browser passes the checks; wait it out
                # before declaring the run blocked.
                obs = self._wait_out_challenge(page, obs, result)
                if obs is None:
                    result.status = "bot-challenge"
                    result.bot_challenge = True
                    break

            prev_marker = obs.get("marker")

            # --- build + decide (413-aware) ---------------------------------
            page_obj = {
                "url": obs["url"],
                "title": obs["title"],
                "text": obs["text"],
                "actions": obs["actions"],
            }

            if requests >= self.max_operation_requests:
                result.status = "budget"
                break
            t0 = time.perf_counter()
            try:
                answers, questions, targets, controls = self._build_and_predict(
                    page_obj, goal, history)
                requests += 1
            except RequestTooLarge:
                # even the trimmed resend did not fit; give up on this task
                result.error = "request exceeds server caps even after trimming"
                break
            except Exception as exc:  # noqa: BLE001 -- ProtocolError/InferenceError
                result.error = f"model error: {str(exc)[:200]}"
                break
            latency = (time.perf_counter() - t0) * 1000

            # --- validate + normalize the operation ------------------------
            op_ans = answers.get("operation", {})
            op_choice = op_ans.get("choice")
            try:
                validate_choice_answer(op_ans, questions["operation"]["criteria"])
                operation = normalize_operation(op_choice, targets, controls)
                op_conf = float(op_ans["probabilities"][op_ans["choice"]])
            except (InvalidAnswer, InvalidOperation) as exc:
                # The model answered outside the offered vocabulary: a harness
                # or model-contract problem. Count it toward the invalid guard
                # so a persistently-broken model stops instead of burning the
                # whole step budget.
                step = StepRecord(step=step_no, operation=str(op_choice), operation_confidence=0.0,
                                  url=obs["url"], outcome=f"invalid-operation: {exc}",
                                  latency_ms=latency)
                result.steps.append(step)
                self._emit(step)
                invalid_streak += 1
                if invalid_streak >= MAX_INVALID_STREAK:
                    result.status = "invalid-decisions"
                    result.error = f"{invalid_streak} consecutive invalid decisions; stopping"
                    break
                obs = self._reobserve(page, result)
                if obs is None:
                    break
                continue

            # --- resolve target (only the head matching the operation) ----
            action = None
            target_key = None
            if operation in controls:
                action = controls[operation]        # page-level: wait/scroll/enter
            elif operation not in ("DONE", "BLOCKED"):
                target_key, action = resolve_target(operation, answers, targets)
                if action is None:
                    step = StepRecord(step=step_no, operation=operation, operation_confidence=op_conf,
                                      target=target_key, url=obs["url"], outcome="invalid-target",
                                      latency_ms=latency)
                    result.steps.append(step)
                    self._emit(step)
                    invalid_streak += 1
                    if invalid_streak >= MAX_INVALID_STREAK:
                        result.status = "invalid-decisions"
                        result.error = f"{invalid_streak} consecutive invalid decisions; stopping"
                        break
                    obs = self._reobserve(page, result)
                    if obs is None:
                        break
                    continue

            low_conf = op_conf < self.tau
            step = StepRecord(step=step_no, operation=operation, operation_confidence=op_conf,
                              target=target_key,
                              target_label=action["label"] if action else None,
                              kind=action["kind"] if action else None,
                              url=obs["url"], latency_ms=latency, low_confidence=low_conf)
            if low_conf:
                result.low_confidence_steps += 1
                if action and isinstance(action.get("node"), int) and action["node"] > 0:
                    dirty.add(action["node"])

            # --- terminal ---------------------------------------------------
            if operation == "DONE":
                # VLM side path, stage 1: gate the terminal choice against the
                # live page. Premature DONE at high confidence is the measured
                # dominant failure mode; a rejection feeds the missing evidence
                # back into recent_actions and the loop re-decides. Fail-open on
                # any gate error -- a broken VLM never wedges the run.
                if self.done_gate is not None and done_rejections < MAX_DONE_REJECTIONS:
                    try:
                        verdict = self.done_gate(page, goal, obs)
                    except Exception as exc:  # noqa: BLE001
                        verdict = {"satisfied": True, "error": str(exc)[:80]}
                    if not verdict.get("satisfied", True):
                        done_rejections += 1
                        problem = "; ".join(str(m) for m in (verdict.get("missing") or []))[:200]
                        problem = problem or "the goal is not visibly satisfied yet"
                        missing = problem[:150]
                        step.outcome = f"done-rejected: missing {missing}"
                        result.steps.append(step)
                        self._emit(step)
                        history.append({
                            "action": f"DONE rejected - still missing: {missing}",
                            "kind": "done", "text": None, "page_changed": False,
                        })
                        # System-2 takeover: the fast model demonstrably just
                        # re-chooses DONE after a rejection -- let the VLM do
                        # the missing step itself, then resume System-1.
                        if self._try_rescue(page, goal, obs, problem, result, step_no, history):
                            obs = self._reobserve(page, result)
                            if obs is None:
                                break
                        continue
                step.outcome = "done"
                result.steps.append(step)
                self._emit(step)
                # terminal-DONE case: positive stopping signal (kept only if
                # the run later verifies -- the sink filters)
                if self.on_case is not None:
                    from .traindata import make_done_case
                    self._case_seq += 1
                    try:
                        self.on_case(make_done_case(
                            goal, obs, history,
                            self.task_id, self._case_seq,
                            f"model DONE at conf {op_conf:.2f}"
                            + (" after gate acceptance" if self.done_gate else "")))
                    except Exception:  # noqa: BLE001
                        pass
                result.status = "done"
                break
            if operation == "BLOCKED":
                step.outcome = "blocked"
                result.steps.append(step)
                self._emit(step)
                result.status = "blocked"
                break

            # --- typed value --------------------------------------------------
            text = None
            if action and action["kind"] == "fill":
                if self.text_model is None:
                    # no literal provider for this task -- System-2 picks a
                    # non-typing way forward instead of terminating the run
                    if self._try_rescue(page, goal, obs,
                                        "a fill is needed but no text provider "
                                        "is configured; choose a non-typing action "
                                        "that advances the goal",
                                        result, step_no, history):
                        obs = self._reobserve(page, result)
                        if obs is None:
                            break
                        continue
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

            # --- execute ------------------------------------------------------
            if action and action["kind"] == "enter" and not _any_filled(obs):
                # Refuse a semantically dead submit: Enter with no field content
                # can never progress (measured pathology -- the model presses
                # Enter on an empty search box, nothing changes, then it DONEs).
                # Coach through recent_actions; after a storm of refusals hand
                # the step to System-2.
                refused_empty += 1
                if (refused_empty >= 3
                        and self._try_rescue(page, goal, obs,
                                             "Enter is pressed repeatedly with no text "
                                             "typed; the query must be typed first",
                                             result, step_no, history)):
                    refused_empty = 0
                    obs = self._reobserve(page, result)
                    if obs is None:
                        break
                    continue
                step.outcome = "refused-empty-enter"
                result.steps.append(step)
                self._emit(step)
                history.append({
                    "action": "Pressed Enter but no field has text; TYPE_TEXT the query first",
                    "kind": "enter", "text": None, "page_changed": False,
                })
                continue
            try:
                self.act(page, action, obs, text=text)
                step.outcome = "executed"
                invalid_streak = 0  # only a step that actually ran clears the streak
                stale_streak = 0
                refused_empty = 0
                # model-step case: kept only if the run later verifies (the
                # runner filters); the page/history here are decision-time
                self._emit_case("model-step", goal, obs, history, action,
                                f"model {operation} on {action.get('id')} "
                                f"(conf {op_conf:.2f})")
            except StalePage as exc:
                step.outcome = f"stale: {str(exc)[:60]}"
                stale_streak += 1
            except ActionFailed as exc:
                step.outcome = f"failed: {str(exc)[:60]}"

            result.steps.append(step)
            self._emit(step)

            if stale_streak >= MAX_STALE_STREAK:
                result.status = "unstable-page"
                result.error = f"{stale_streak} consecutive stale decisions; stopping"
                break

            history.append({
                "action": action["label"] if action else operation,
                "kind": action["kind"] if action else operation.lower(),
                "text": text,
                "page_changed": None,      # filled in after the re-observation below
            })

            # --- re-observe ----------------------------------------------------
            obs = self._reobserve(page, result)
            if obs is None:
                break

            # record whether the page actually moved (this drives the guards)
            changed = obs.get("marker") != prev_marker
            step.page_changed = changed
            if history:
                history[-1]["page_changed"] = changed

            # --- no-progress / repeat guards -----------------------------------
            # A click that changes nothing, a challenge page, a disabled control:
            # all leave the marker fixed. Termination is the last resort -- the
            # VLM rescue gets one corrective action first.
            recent.append({"page_changed": changed,
                           "kind": action["kind"] if action else operation.lower(),
                           "operation": operation, "target": target_key})
            no_progress = detect_no_progress(recent)
            repeating = detect_repeat(recent)
            if no_progress or repeating:
                problem = ("page unchanged across 4 steps" if no_progress else
                           f"{operation} on the same target repeats without progress")
                if self._try_rescue(page, goal, obs, problem, result, step_no, history):
                    recent.clear()
                    obs = self._reobserve(page, result)
                    if obs is None:
                        break
                    continue
                result.status = "no-progress" if no_progress else "repeat-loop"
                result.error = problem + "; stopping"
                break
        else:
            result.status = "max-steps"

        result.total_ms = (time.perf_counter() - started) * 1000
        result.dirty_nodes = sorted(dirty)
        return result

    # -- helpers ----------------------------------------------------------------

    def _build_and_predict(self, page_obj, goal, history):
        """Build + send; on 413 halve the candidate table and resend once (§3.2).

        Returns ``(answers, questions, targets, controls)`` from the build that
        actually produced the answers, so target resolution never crosses two
        differently-indexed tables. The smaller table is kept for the rest of
        the run so later steps do not pay the failed round trip again.
        """
        state, questions, targets, controls = build_request(
            page_obj, goal, history, self.max_actions)
        try:
            answers = self.model.predict(state, questions)
        except RequestTooLarge:
            trimmed = max(MIN_MAX_ACTIONS, self.max_actions // 2)
            if trimmed >= self.max_actions:
                raise
            self.max_actions = trimmed
            state, questions, targets, controls = build_request(
                page_obj, goal, history, trimmed)
            answers = self.model.predict(state, questions)
        return answers, questions, targets, controls

    def _try_rescue(self, page, goal, obs, problem, result, step_no, history) -> bool:
        """One System-2 takeover step. Returns True if an action was executed.

        The VLM may only name an element from the observed table (spec §2.6
        invariant 1: DOM observation is the sole authority on existence). The
        id is resolved tolerantly -- exact id, bare node number, or label text
        -- because measured rescue failures were mostly id-format mismatches.
        Any other failure (error, missing fill text, exhausted budget) returns
        False and the caller falls back to its normal behaviour, with the
        reason printed so misses are visible in the run log.
        """
        if self.rescue is None or self.rescues_used >= self.max_rescues:
            return False
        try:
            choice = self.rescue(page, goal, obs, problem)
        except Exception as exc:  # noqa: BLE001 -- a broken VLM never wedges the run
            print(f"    [rescue unused: vlm error {str(exc)[:60]}]", flush=True)
            return False
        if not isinstance(choice, dict):
            return False
        action = self._resolve_rescue_target(choice, obs.get("actions", []))
        if action is None:
            print(f"    [rescue unused: id {choice.get('id')!r} not resolvable "
                  f"to an observed element]", flush=True)
            return False
        text = choice.get("text") if action.get("kind") == "fill" else None
        if action.get("kind") == "fill" and not text and self.text_model is not None:
            # the VLM picked a fill but no text -- the task's literal provider
            # knows the query (measured: the VLM strongly prefers clicks over
            # fills and never supplies text on its own)
            try:
                text = self.text_model({
                    "goal": goal,
                    "field": {"label": action.get("label"), "role": action.get("role"),
                              "value": action.get("current_value", "")},
                    "page": {"title": obs.get("title"), "text": (obs.get("text") or "")[:1500]},
                    "recent_actions": [],
                })
            except Exception:  # noqa: BLE001
                text = None
        if action.get("kind") == "fill" and not text:
            print(f"    [rescue unused: fill without text]", flush=True)
            return False
        # teacher label: the VLM's corrective choice on this exact observation
        self._emit_case("rescue", goal, obs, history, action,
                        f"VLM rescue ({problem[:150]})" + (f"; typed {text!r}" if text else ""))
        self.rescues_used += 1
        step = StepRecord(step=step_no, operation="VLM_RESCUE", operation_confidence=1.0,
                          target=action.get("id"), target_label=action.get("label"),
                          kind=action.get("kind"), text=text, url=obs.get("url"))
        try:
            self.act(page, action, obs, text=text)
            step.outcome = "executed"
        except (StalePage, ActionFailed) as exc:  # noqa: BLE001
            step.outcome = str(exc)[:60]
        result.steps.append(step)
        self._emit(step)
        history.append({"action": f"VLM rescue: {action.get('label')}",
                        "kind": action.get("kind"), "text": text, "page_changed": None})
        return True

    @staticmethod
    def _resolve_rescue_target(choice: Dict[str, Any], actions: List[Dict[str, Any]]):
        """Resolve the VLM's chosen target onto an observed action, tolerantly."""
        rid = str(choice.get("id") or "").strip()
        if rid:
            by_id = next((a for a in actions if a.get("id") == rid), None)
            if by_id is not None:
                return by_id
            if rid.isdigit():  # bare node number: "25" -> click:25 / fill:25
                for prefix in ("click:", "fill:", "select:"):
                    cand = next((a for a in actions if a.get("id") == f"{prefix}{rid}"), None)
                    if cand is not None:
                        return cand
        label = str(choice.get("label") or choice.get("element") or "").strip().lower()
        if label:
            cand = next((a for a in actions
                         if label in str(a.get("label") or "").lower()), None)
            if cand is not None:
                return cand
        return None

    def _wait_out_challenge(self, page, obs, result) -> Optional[Dict[str, Any]]:
        """Give an auto-resolving challenge time to clear; re-observe each round.

        Returns the fresh observation once clear, or None if it persists after
        `challenge_retries` rounds (Google's /sorry wall typically persists --
        the retries cost a few seconds and nothing else).
        """
        for _ in range(max(1, self.challenge_retries)):
            if self.challenge_wait_s:
                time.sleep(self.challenge_wait_s)
            obs = self._reobserve(page, result)
            if obs is None:
                return None
            if not obs.get("challenge", {}).get("hit"):
                return obs
        return None

    def _reobserve(self, page, result) -> Optional[Dict[str, Any]]:
        try:
            obs = self.observe(page)
        except Exception as exc:  # noqa: BLE001
            result.error = f"observe failed: {exc}"
            return None
        return obs

    def _emit(self, step: StepRecord) -> None:
        if self.on_step:
            try:
                self.on_step(step)
            except Exception:  # noqa: BLE001
                pass
