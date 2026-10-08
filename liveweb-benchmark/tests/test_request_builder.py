"""Request-format invariants: the v3 wire format the fine-tune was trained on."""

from agentbench.request_builder import (
    LABEL_CHARS,
    PAGE_TEXT_CHARS,
    action_space,
    build_request,
    cap_actions,
)


def _action(n, kind="click", label=None, in_viewport=True):
    return {"id": f"{kind}:{n}", "kind": kind, "label": label or f"Element {n}",
            "role": "button", "node": n, "value": "", "current_value": "",
            "in_viewport": in_viewport}


def _page(n_elements=3, text="page text"):
    actions = [_action(i) for i in range(1, n_elements + 1)]
    actions += [{"node": 0, "id": "wait", "kind": "wait", "label": "Wait", "role": "wait"},
                {"node": 0, "id": "press_enter", "kind": "enter", "label": "Enter", "role": "enter"}]
    return {"url": "https://x/", "title": "T", "text": text, "actions": actions}


class TestV3Format:
    def test_elements_never_in_state(self):
        state, questions, _, _ = build_request(_page(), "goal")
        assert "elements" not in state
        assert set(state) == {"page", "recent_actions"}
        # candidates live only in criteria
        assert "click_target" in questions
        assert "1" in questions["click_target"]["criteria"]

    def test_page_text_capped(self):
        state, *_ = build_request(_page(text="x" * 9999), "goal")
        assert len(state["page"]["text"]) == PAGE_TEXT_CHARS

    def test_label_capped(self):
        page = _page()
        page["actions"][0]["label"] = "L" * 200
        _, questions, _, _ = build_request(page, "goal")
        crit = questions["click_target"]["criteria"]["1"]
        # _compact renders the element as "label (role)" with the label cut to 50
        assert len(crit) <= LABEL_CHARS + len(" (button)")

    def test_operation_vocabulary(self):
        _, questions, _, _ = build_request(_page(), "goal")
        criteria = questions["operation"]["criteria"]
        for key in ("CLICK", "DONE", "BLOCKED", "WAIT", "PRESS_ENTER"):
            assert key in criteria, criteria

    def test_target_head_carries_goal_and_operation(self):
        goal = "find the answer"
        _, questions, _, _ = build_request(_page(), goal)
        for qid, q in questions.items():
            if qid == "operation":
                continue
            assert q["instructions"]["goal"] == goal
            assert q["instructions"]["operation"] == qid.removesuffix("_target").upper()

    def test_history_capped_at_ten(self):
        history = [{"action": f"a{i}", "kind": "click", "text": None, "page_changed": True}
                   for i in range(30)]
        state, *_ = build_request(_page(), "goal", history)
        assert len(state["recent_actions"]) == 10
        assert state["recent_actions"][-1]["action"] == "a29"


class TestSelectOptions:
    def test_select_targets_get_option_indices(self):
        actions = [
            {"id": "select:1:0", "kind": "select", "label": "City → Paris",
             "role": "combobox", "node": 1, "value": "paris", "current_value": "—"},
            {"id": "select:1:1", "kind": "select", "label": "City → Tokyo",
             "role": "combobox", "node": 1, "value": "tokyo", "current_value": "—"},
        ]
        _, _, targets, _ = build_request(
            {"url": "u", "title": "t", "text": "x", "actions": actions}, "goal")
        assert set(targets["SELECT"]) == {"1:1", "1:2"}


class TestActionCap:
    def test_cap_keeps_controls_and_prefers_viewport(self):
        controls = [{"node": 0, "id": "wait", "kind": "wait", "label": "Wait", "role": "wait"},
                    {"node": 0, "id": "press_enter", "kind": "enter", "label": "Enter", "role": "enter"}]
        actions = [_action(i, in_viewport=False) for i in range(1, 201)]
        actions += [_action(1000 + i, in_viewport=True) for i in range(100)]
        actions += controls
        capped = cap_actions(actions, max_actions=250)
        element_kinds = [a for a in capped if a["kind"] in ("click", "fill", "select")]
        assert len(element_kinds) == 250
        # every in-viewport element survives; only the last off-screen ones drop
        nodes = {a["node"] for a in element_kinds}
        assert 1001 in nodes and 1099 in nodes
        assert 1 in nodes and 200 not in nodes  # out-view keep the first 150 of 200
        assert all(c in capped for c in controls)  # page-level controls always survive

    def test_build_request_respects_max_actions(self):
        page = _page(n_elements=300)
        state, questions, targets, controls = build_request(page, "goal", max_actions=50)
        assert len(targets["CLICK"]) == 50
        assert "WAIT" in controls  # controls survive the cap

    def test_cap_prefix_invariant(self):
        """Index consistency across caps: for the same action list, key k must
        identify the same element at any cap >= k.

        The observation level caps at 250 and the 413 trim path re-caps at a
        smaller size; both rely on cap_actions(N) yielding a prefix of
        cap_actions(M) (N < M) and on action_space indexing sequentially. If
        capping ever becomes relevance-ranked or otherwise non-prefix, indices
        silently diverge and a model's chosen key would execute a *different*
        element while passing every validation layer."""
        actions = [_action(i, in_viewport=(i % 2 == 0)) for i in range(1, 401)]
        controls = [{"node": 0, "id": "wait", "kind": "wait", "label": "Wait", "role": "wait"},
                    {"node": 0, "id": "press_enter", "kind": "enter", "label": "Enter", "role": "enter"}]
        page = {"url": "u", "title": "t", "text": "x", "actions": actions + controls}
        _, _, targets_full, _ = build_request(page, "goal", max_actions=300)
        _, _, targets_small, _ = build_request(page, "goal", max_actions=150)
        assert set(targets_small["CLICK"]) < set(targets_full["CLICK"])  # both capped
        for key, action in targets_small["CLICK"].items():
            assert targets_full["CLICK"][key]["id"] == action["id"], key


class TestObserveFinalize:
    def test_dropped_counts_capped_elements(self):
        from agentbench.observe import _finalize
        actions = [{"id": f"click:{i}", "kind": "click", "label": f"E{i}", "role": "button",
                    "node": i, "value": "", "current_value": ""} for i in range(1, 301)]
        actions.append({"node": 0, "id": "wait", "kind": "wait", "label": "Wait", "role": "wait"})
        raw = {"url": "u", "title": "t", "text": "x", "actions": actions,
               "scroll": {"y": 0, "height": 800}, "count": len(actions),
               "semantics": [], "stats": {"n_elements": 300, "text_len": 1},
               "challenge": {"hit": False}}
        obs = _finalize(raw, max_actions=250)
        assert obs["dropped"] == 50 and obs["truncated"] is True
        assert obs["count"] == 251  # 250 elements + the wait control

    def test_signals_default_to_zero(self):
        from agentbench.observe import _finalize
        raw = {"url": "u", "title": "t", "text": "x", "actions": [], "scroll": {},
               "count": 0, "semantics": [], "stats": {}, "challenge": {"hit": False}}
        obs = _finalize(raw, 250)
        assert obs["signals"]["n_occluded"] == 0 and obs["dropped"] == 0
