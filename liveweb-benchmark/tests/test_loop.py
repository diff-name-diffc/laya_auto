"""Loop-level tests: a scripted fake model + fake observation/execution.

These pin the guard semantics the spec calls out as measured bug sources:
invalid-decision streak resets only after a *successful execution*, invalid
paths check the guard before continuing, challenge pages terminate at once,
low confidence is recorded without blocking, and 413 trims and resends.
No browser, no network.
"""

from agentbench.loop import Agent
from agentbench.executor import StalePage
from agentbench.validators import RequestTooLarge


# --- fakes --------------------------------------------------------------------


def make_obs(marker="m0", challenge=False, text="page text"):
    actions = [
        {"id": "click:1", "kind": "click", "label": "Search button", "role": "button",
         "node": 1, "value": "", "current_value": "", "in_viewport": True},
        {"id": "fill:2", "kind": "fill", "label": "Search query", "role": "searchbox",
         "node": 2, "value": "", "current_value": "", "in_viewport": True},
        {"id": "click:3", "kind": "click", "label": "Link A", "role": "link",
         "node": 3, "value": "", "current_value": "", "in_viewport": False},
        {"node": 0, "id": "wait", "kind": "wait", "label": "Wait", "role": "wait"},
        {"node": 0, "id": "press_enter", "kind": "enter", "label": "Enter", "role": "enter"},
    ]
    return {"url": "https://x/", "title": "t", "text": text, "actions": actions,
            "scroll": {"y": 0, "height": 800}, "count": len(actions),
            "signals": {"suspicious": False}, "truncated": False,
            "challenge": {"hit": challenge, "kind": "dom" if challenge else None},
            "marker": marker}


class FakeObserve:
    """Returns scripted observations; when exhausted, repeats the last one."""

    def __init__(self, observations):
        self.queue = list(observations)
        self.calls = 0

    def __call__(self, page):
        self.calls += 1
        if len(self.queue) > 1:
            return self.queue.pop(0)
        return self.queue[0]


class FakeAct:
    def __init__(self):
        self.calls = []

    def __call__(self, page, action, page_state, text=None):
        self.calls.append((action["id"], text))


class StaleAct:
    """Every action is refused: the page changed under every decision."""

    def __init__(self):
        self.calls = []

    def __call__(self, page, action, page_state, text=None):
        self.calls.append(action["id"])
        raise StalePage("page changed since the decision")


class FakeModel:
    """Builds self-consistent answers from the actual questions.

    Script items: "OP" | ("OP", target_key_or_None, confidence).
    `raise_on_calls` maps call-index -> exception to raise (for 413 testing).
    """

    def __init__(self, script, raise_on_calls=None):
        self.script = list(script)
        self.raise_on_calls = raise_on_calls or {}
        self.calls = 0
        self.criteria_sizes = []

    def predict(self, state, questions):
        self.calls += 1
        if self.calls in self.raise_on_calls:
            raise self.raise_on_calls[self.calls]
        item = self.script.pop(0) if self.script else "DONE"
        if isinstance(item, tuple):
            op, target, conf = item
        else:
            op, target, conf = item, None, 0.95
        answers = {}
        opq = questions["operation"]
        keys = list(opq["criteria"])
        self.criteria_sizes.append(len(keys))
        answers["operation"] = self._choice(keys, op, conf)
        for qid, q in questions.items():
            if qid == "operation":
                continue
            tkeys = list(q["criteria"])
            if not tkeys:
                continue
            # honour the scripted target verbatim -- a bogus key must surface as
            # an invalid answer, not be silently corrected by the fake
            chosen = target if target is not None else tkeys[0]
            answers[qid] = self._choice(tkeys, chosen, 0.9)
        return answers

    @staticmethod
    def _choice(keys, choice, conf):
        if len(keys) == 1:
            probs = {keys[0]: 1.0}
            return {"type": "choice", "choice": keys[0], "probabilities": probs,
                    "confidence": 1.0}
        others = [k for k in keys if k != choice]
        # keep the chosen key the argmax while honouring the requested confidence
        conf = min(max(conf, 1.0 / len(keys) + 0.02), 0.98)
        rest = (1.0 - conf) / len(others)
        probs = {k: rest for k in others}
        probs[choice] = conf
        return {"type": "choice", "choice": choice, "probabilities": probs,
                "confidence": conf}


def run_agent(model, observations, text_model=None, act=None, **kw):
    obs_fn = observations if isinstance(observations, FakeObserve) else FakeObserve(observations)
    act = act or FakeAct()
    agent = Agent(model, text_model=text_model, observe_fn=obs_fn, act_fn=act, **kw)
    result = agent.run(page=None, goal="test goal")
    return result, act


# --- terminals ----------------------------------------------------------------


def test_done_on_first_step():
    result, act = run_agent(FakeModel(["DONE"]), [make_obs()])
    assert result.status == "done"
    assert result.steps[0].outcome == "done"
    assert act.calls == []


def test_blocked():
    result, _ = run_agent(FakeModel(["BLOCKED"]), [make_obs()])
    assert result.status == "blocked"


# --- invalid-decision guards ---------------------------------------------------


def test_three_invalid_targets_stop_the_run():
    model = FakeModel([("CLICK", "999", 0.9)] * 3)
    result, _ = run_agent(model, [make_obs()])
    assert result.status == "invalid-decisions"
    assert all(s.outcome == "invalid-target" for s in result.steps)


def test_invalid_operation_stops_the_run():
    result, _ = run_agent(FakeModel(["FLY"] * 3), [make_obs()])
    assert result.status == "invalid-decisions"
    assert "invalid-operation" in result.steps[0].outcome


def test_streak_resets_only_after_real_execution():
    # invalid, invalid, executed CLICK, then three more invalid -> stop at 6 steps
    model = FakeModel([
        ("CLICK", "999", 0.9), ("CLICK", "999", 0.9), ("CLICK", "1", 0.9),
        ("CLICK", "999", 0.9), ("CLICK", "999", 0.9), ("CLICK", "999", 0.9),
    ])
    # markers change after the executed step so no other guard fires first
    observations = FakeObserve([make_obs(f"m{i}") for i in range(7)])
    result, _ = run_agent(model, observations)
    assert result.status == "invalid-decisions"
    assert len(result.steps) == 6


# --- no-progress / repeat ------------------------------------------------------


def test_no_progress_after_four_unchanged_steps():
    # alternate targets so the repeat guard does not fire before no-progress
    alternating = [("CLICK", t, 0.9) for t in ("1", "3", "1", "3")]
    result, act = run_agent(FakeModel(alternating), [make_obs()])
    assert result.status == "no-progress"
    assert len(act.calls) == 4


def test_repeat_loop_with_changing_pages():
    observations = FakeObserve([make_obs(f"m{i}") for i in range(5)])
    result, _ = run_agent(FakeModel([("CLICK", "1", 0.9)] * 3), observations)
    assert result.status == "repeat-loop"


def test_unstable_page_after_consecutive_stales():
    # pages keep changing (so no-progress never fires), targets alternate (so
    # repeat never fires) -- only the stale-streak guard stops the burn
    alternating = [("CLICK", t, 0.9) for t in ("1", "3") * 6]
    act = StaleAct()
    result, _ = run_agent(
        FakeModel(alternating),
        FakeObserve([make_obs(f"m{i}") for i in range(20)]),
        act=act)
    assert result.status == "unstable-page"
    assert len(act.calls) == 4  # MAX_STALE_STREAK
    assert all(s.outcome.startswith("stale") for s in result.steps)


def test_stale_streak_resets_after_a_real_execution():
    # three stales (targets alternate so repeat never fires), one executed
    # click, then a DONE -- the streak reset let the run continue to success
    model = FakeModel([("CLICK", "1", 0.9), ("CLICK", "3", 0.9), ("CLICK", "1", 0.9),
                       ("CLICK", "3", 0.9), "DONE"])
    flaky = _FlakyAct(stale_first=3)
    result, act = run_agent(
        model, FakeObserve([make_obs(f"m{i}") for i in range(20)]), act=flaky)
    assert result.status == "done"
    assert len(act.executed) == 1


class _FlakyAct:
    """Stales the first N calls, then executes normally."""

    def __init__(self, stale_first):
        self.remaining = stale_first
        self.executed = []

    def __call__(self, page, action, page_state, text=None):
        if self.remaining > 0:
            self.remaining -= 1
            raise StalePage("page changed")
        self.executed.append(action["id"])


def test_budgets():
    # alternate targets so no repeat guard fires; pages change so no no-progress
    alternating = [("CLICK", t, 0.9) for t in ("1", "3", "1", "3", "1", "3")]
    result, _ = run_agent(
        FakeModel(alternating),
        FakeObserve([make_obs(f"m{i}") for i in range(20)]),
        max_steps=3)
    assert result.status == "max-steps"
    assert len(result.steps) == 3


# --- text helper ----------------------------------------------------------------


def test_fill_without_text_model_blocks():
    result, _ = run_agent(FakeModel(["TYPE_TEXT"]), [make_obs()])
    assert result.status == "blocked"
    assert result.steps[0].outcome == "no-text-model"


def test_fill_passes_text_from_provider():
    result, act = run_agent(
        FakeModel([("TYPE_TEXT", "2", 0.9), "DONE"]),
        FakeObserve([make_obs("m0"), make_obs("m1"), make_obs("m1")]),
        text_model=lambda ctx: "openai news")
    assert act.calls == [("fill:2", "openai news")]
    assert result.status == "done"
    assert result.steps[0].text == "openai news"


# --- challenge pages -------------------------------------------------------------


def test_initial_challenge_never_calls_the_model():
    model = FakeModel(["DONE"])
    result, _ = run_agent(model, [make_obs(challenge=True)],
                          challenge_wait_s=0, challenge_retries=1)
    assert result.status == "bot-challenge"
    assert model.calls == 0
    assert result.bot_challenge


def test_challenge_mid_run_terminates():
    observations = FakeObserve([make_obs("m0"), make_obs("m1", challenge=True)])
    result, _ = run_agent(FakeModel(["CLICK"] * 10), observations,
                          challenge_wait_s=0, challenge_retries=1)
    assert result.status == "bot-challenge"
    assert len(result.steps) == 1  # stopped right after the page turned into a wall


def test_js_challenge_self_clears_and_run_continues():
    # the wall appears after step 1, then clears during the wait-retry window
    observations = FakeObserve([make_obs("m0"), make_obs("m1", challenge=True),
                                make_obs("m2")])
    result, act = run_agent(FakeModel(["CLICK", "DONE"]), observations,
                            challenge_wait_s=0, challenge_retries=2)
    assert result.status == "done"
    assert len(act.calls) == 1  # the run resumed and finished normally


# --- confidence gating ------------------------------------------------------------


def test_low_confidence_marked_and_node_dirtied():
    model = FakeModel([("CLICK", "1", 0.2), "DONE"])
    result, _ = run_agent(model, FakeObserve([make_obs("m0"), make_obs("m1"), make_obs("m1")]))
    assert result.low_confidence_steps == 1
    assert result.steps[0].low_confidence is True
    assert result.dirty_nodes == [1]
    # a low-confidence decision still executes: the side path never blocks (§2.4)
    assert result.steps[0].outcome == "executed"


# --- DONE gate (VLM side path, stage 1) ----------------------------------------


def test_done_gate_rejection_forces_redecision():
    calls = {"n": 0}

    def gate(page, goal, obs):          # rejects once, then is satisfied
        calls["n"] += 1
        return {"satisfied": calls["n"] > 1, "missing": ["search results"]}

    model = FakeModel(["DONE", "DONE"])
    result, act = run_agent(model, [make_obs()], done_gate=gate)
    assert result.status == "done"           # second DONE accepted
    assert len(result.steps) == 2
    assert result.steps[0].outcome.startswith("done-rejected")
    assert act.calls == []


def test_done_gate_caps_rejections():
    def always_reject(page, goal, obs):
        return {"satisfied": False, "missing": ["evidence"]}

    result, _ = run_agent(FakeModel(["DONE"] * 4), [make_obs()], done_gate=always_reject)
    assert result.status == "done"           # accepted after MAX_DONE_REJECTIONS
    rejections = [s for s in result.steps if s.outcome.startswith("done-rejected")]
    assert len(rejections) == 2


def test_done_gate_error_fails_open():
    def boom(page, goal, obs):
        raise RuntimeError("vlm endpoint down")

    result, _ = run_agent(FakeModel(["DONE"]), [make_obs()], done_gate=boom)
    assert result.status == "done"
    assert result.steps[0].outcome == "done"


def test_rejected_done_feeds_missing_evidence_into_history():
    seen_history = []

    class CapturingModel(FakeModel):
        def predict(self, state, questions):
            seen_history.append(state.get("recent_actions", []))
            return super().predict(state, questions)

    gate = lambda page, goal, obs: {"satisfied": False, "missing": ["openai results"]}  # noqa: E731
    run_agent(CapturingModel(["DONE", "DONE"]), [make_obs()], done_gate=gate)
    # the second decision must see the corrective note from the first rejection
    assert any("still missing: openai results" in str(h) for h in seen_history)


# --- 413 trim-and-resend -----------------------------------------------------------


def test_request_too_large_trims_and_resends():
    model = FakeModel(["DONE"], raise_on_calls={1: RequestTooLarge("HTTP 413")})
    agent_obs = FakeObserve([make_obs()])
    agent = Agent(model, observe_fn=agent_obs, act_fn=FakeAct(), max_actions=250)
    result = agent.run(page=None, goal="g")
    assert result.status == "done"
    assert model.calls == 2
    assert agent.max_actions == 125  # the trimmed table is kept for the run


def test_trimmed_resend_resolves_against_the_answered_table():
    """The contract the 413 path must hold: answers are resolved against the
    same questions/targets that produced them, never across two tables."""
    model = FakeModel([("CLICK", None, 0.9), "DONE"],
                      raise_on_calls={1: RequestTooLarge("HTTP 413")})
    agent_obs = FakeObserve([make_obs("m0"), make_obs("m1"), make_obs("m1")])
    act = FakeAct()
    agent = Agent(model, observe_fn=agent_obs, act_fn=act, max_actions=250)
    result = agent.run(page=None, goal="g")

    assert result.status == "done"
    # behavioural check: the executed action is the one the *second* (trimmed)
    # build's criteria pointed at -- the model answered from that table
    from agentbench.request_builder import build_request
    _, _, targets_trimmed, _ = build_request(
        {"url": "https://x/", "title": "t", "text": "page text",
         "actions": make_obs()["actions"]}, "g", (), 125)
    assert act.calls[0][0] == targets_trimmed["CLICK"]["1"]["id"]
    # call 1 raised 413 (no script consumed), call 2 answered CLICK, call 3 DONE
    assert model.calls == 3


def test_persistent_too_large_stops_the_run():
    model = FakeModel(["DONE"], raise_on_calls={1: RequestTooLarge("a"), 2: RequestTooLarge("b")})
    result, _ = run_agent(model, [make_obs()])
    assert result.status == "incomplete"
    assert "caps" in (result.error or "")


# --- empty-submit refusal -------------------------------------------------------


def test_empty_enter_refused_and_coached():
    # press_enter with an empty field -> refused with a coaching note; the model
    # then types (executes) and finishes
    model = FakeModel(["PRESS_ENTER", ("TYPE_TEXT", "2", 0.9), "DONE"])
    obs_seq = [make_obs("m0"), make_obs("m1"), make_obs("m2"), make_obs("m2")]
    result, act = run_agent(model, FakeObserve(obs_seq), text_model=lambda ctx: "openai news")
    assert result.steps[0].outcome == "refused-empty-enter"
    assert act.calls == [("fill:2", "openai news")]
    assert result.status == "done"


def test_enter_with_filled_field_executes():
    obs = make_obs()
    for a in obs["actions"]:
        if a["kind"] == "fill":
            a["current_value"] = "openai news"
    result, act = run_agent(FakeModel(["PRESS_ENTER", "DONE"]),
                            FakeObserve([obs, make_obs("m1"), make_obs("m1")]))
    assert result.steps[0].outcome == "executed"
    assert act.calls == [("press_enter", None)]


# --- VLM rescue (System-2 takeover) ----------------------------------------------


def test_rescue_after_rejected_done_executes_and_recovers():
    gate_calls = {"n": 0}

    def gate(page, goal, obs):
        gate_calls["n"] += 1
        return {"satisfied": gate_calls["n"] > 1, "missing": ["search results"]}

    def rescue(page, goal, obs, problem):
        return {"id": "fill:2", "text": "ai research papers"}

    model = FakeModel(["DONE", "DONE"])
    result, act = run_agent(model, FakeObserve([make_obs("m0"), make_obs("m1"), make_obs("m1")]),
                            done_gate=gate, rescue=rescue)
    assert result.status == "done"
    assert result.steps[0].outcome.startswith("done-rejected")
    assert result.steps[1].operation == "VLM_RESCUE"
    assert act.calls == [("fill:2", "ai research papers")]
    assert result.summary()["vlm_rescues"] == 1


def test_rescue_on_repeat_loop_instead_of_terminating():
    def rescue(page, goal, obs, problem):
        assert "repeats without progress" in problem
        return {"id": "click:3"}

    model = FakeModel([("CLICK", "1", 0.9)] * 3 + ["DONE"])
    result, act = run_agent(model, FakeObserve([make_obs(f"m{i}") for i in range(6)]),
                            rescue=rescue)
    assert result.status == "done"
    assert any(s.operation == "VLM_RESCUE" for s in result.steps)
    assert act.calls[-1] == ("click:3", None)


def test_rescue_rejects_unobserved_element():
    def bogus(page, goal, obs, problem):
        return {"id": "click:999"}   # not in the observed table

    result, _ = run_agent(FakeModel([("CLICK", "1", 0.9)] * 3),
                          FakeObserve([make_obs(f"m{i}") for i in range(6)]),
                          rescue=bogus)
    assert result.status == "repeat-loop"   # fell back to normal termination


def test_rescue_budget_exhaustion_falls_back():
    def rescue(page, goal, obs, problem):
        return {"id": "click:3"}

    model = FakeModel([("CLICK", "1", 0.9)] * 6)
    result, _ = run_agent(model, FakeObserve([make_obs(f"m{i}") for i in range(10)]),
                          rescue=rescue, max_rescues=0)
    assert result.status == "repeat-loop"


def test_empty_enter_storm_escalates_to_rescue():
    def rescue(page, goal, obs, problem):
        assert "no text typed" in problem
        return {"id": "fill:2", "text": "llm"}

    model = FakeModel(["PRESS_ENTER", "PRESS_ENTER", "PRESS_ENTER", "DONE"])
    result, act = run_agent(model, FakeObserve([make_obs("m0"), make_obs("m1"), make_obs("m1")]),
                            rescue=rescue)
    assert result.status == "done"
    assert act.calls == [("fill:2", "llm")]
    assert sum(1 for s in result.steps if s.outcome == "refused-empty-enter") == 2  # 3rd escalates


def test_rescue_tolerant_id_resolution():
    actions = [{"id": "click:25", "kind": "click", "label": "paperclipai / paperclip",
                "role": "link", "node": 25},
               {"id": "fill:8", "kind": "fill", "label": "Search",
                "role": "searchbox", "node": 8, "current_value": ""}]

    def run(choice):
        return Agent._resolve_rescue_target(choice, actions)

    assert run({"id": "click:25"})["id"] == "click:25"          # exact
    assert run({"id": "25"})["id"] == "click:25"                # bare node number
    assert run({"id": "8", "text": "q"})["id"] == "fill:8"      # bare fill number
    assert run({"id": "bogus", "label": "paperclipai"})["id"] == "click:25"  # by label
    assert run({"id": "nope"}) is None                          # unresolvable
    assert run({"label": "Search"})["id"] == "fill:8"           # label only


# --- distillation cases (every rescue becomes training data) ---------------------


def test_rescue_emits_training_case():
    seen = []

    def rescue(page, goal, obs, problem):
        return {"id": "click:25"}

    def obs_with_repo(marker):
        o = make_obs(marker)
        o["actions"] = [
            {"id": "click:25", "kind": "click", "label": "paperclipai / paperclip",
             "role": "link", "node": 25},
            *[a for a in o["actions"] if a["kind"] == "fill"],
        ]
        return o

    model = FakeModel([("CLICK", "1", 0.9)] * 3 + ["DONE"])
    result, _ = run_agent(model,
                          FakeObserve([obs_with_repo(f"m{i}") for i in range(6)]),
                          rescue=rescue, on_case=seen.append)
    cases = [c for c in seen if c["source"] == "liveweb:rescue"]
    assert cases and cases[0]["gold_op"] == "CLICK" and cases[0]["gold_id"] == "click:25"
    assert cases[0]["page"]["actions"] and "VLM rescue" in cases[0]["rationale"]


def test_model_steps_emitted_only_via_sink_filter():
    from agentbench.traindata import CaseSink, gold_of

    sink = CaseSink("t")
    assert gold_of({"kind": "fill", "id": "fill:2"}) == ("TYPE_TEXT", "fill:2")
    assert gold_of({"kind": "scroll", "id": "scroll_down", "delta": 560}) == ("SCROLL_DOWN", "scroll_down")
    assert gold_of({"kind": "enter", "id": "press_enter"}) == ("PRESS_ENTER", "press_enter")
    sink.add({"source": "liveweb:model-step", "x": 1, "gold_op": "TYPE_TEXT",
              "gold_id": "fill:2", "page": {"url": "u1"}})
    sink.add({"source": "liveweb:rescue", "x": 2})
    assert [c["x"] for c in sink.finalize(verified=False)] == [2]   # rescue only
    assert [c["x"] for c in sink.finalize(verified=True)] == [2, 1]  # rescue + capped step


# --- failure-primary distillation policy -----------------------------------------


def test_done_case_and_capped_steps_policy():
    from agentbench.traindata import CaseSink

    sink = CaseSink("t", step_cap=2)
    sink.add({"source": "liveweb:model-step", "gold_op": "TYPE_TEXT", "gold_id": "fill:2",
              "page": {"url": "u1"}})
    sink.add({"source": "liveweb:model-step", "gold_op": "TYPE_TEXT", "gold_id": "fill:2",
              "page": {"url": "u1"}})          # duplicate url+gold -> dropped
    sink.add({"source": "liveweb:model-step", "gold_op": "CLICK", "gold_id": "click:5",
              "page": {"url": "u2"}})
    sink.add({"source": "liveweb:model-step", "gold_op": "SCROLL_DOWN", "gold_id": "scroll_down",
              "page": {"url": "u3"}})
    sink.add({"source": "liveweb:rescue", "gold_op": "CLICK", "gold_id": "click:9",
              "page": {"url": "u4"}})
    sink.add({"source": "liveweb:done", "gold_op": "DONE", "gold_id": None,
              "page": {"url": "u5"}})
    failed = sink.finalize(verified=False)
    assert [c["source"] for c in failed] == ["liveweb:rescue"]
    ok = sink.finalize(verified=True)
    kinds = [c["source"] for c in ok]
    assert kinds.count("liveweb:rescue") == 1
    assert kinds.count("liveweb:done") == 1
    steps = [c for c in ok if c["source"] == "liveweb:model-step"]
    assert len(steps) <= 2                                   # capped
    assert steps[0]["gold_op"] in ("SCROLL_DOWN", "CLICK")   # rare ops first
