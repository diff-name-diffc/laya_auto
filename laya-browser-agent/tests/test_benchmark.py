"""Validate the benchmark harness itself, with no model.

A benchmark is only useful if its ground truth and metrics are right. These
tests pin:

* the request builder's shape and the v3 invariants (elements out of ``state``,
  label/page-text caps);
* gold derivation for the Chinese cases;
* metric math on a scripted oracle (perfect, chance, and miscalibrated).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark import zh_cases  # noqa: E402
from benchmark.browser_request import build_request, gold_for, LABEL_CHARS  # noqa: E402
from benchmark.metrics import Report, CaseResult  # noqa: E402
from benchmark.run import score_case  # noqa: E402


class OracleModel:
    """Answers exactly the gold operation/target of each case."""

    def __init__(self, wants_wrong=False):
        self.wants_wrong = wants_wrong

    def predict(self, state, questions):
        # Rebuild gold from the question criteria: the target question key
        # matching the operation we return. We cheat by using the first option.
        answers = {}
        for qid, q in questions.items():
            keys = list(q["criteria"].keys())
            pick = keys[-1] if not self.wants_wrong else keys[0]
            if qid == "operation":
                # choose the operation that has a target head when possible
                cand = [k for k in keys if k + "_target" in questions or k.lower() + "_target" in questions]
                pick = (cand[0] if cand else keys[0]) if not self.wants_wrong else keys[-1]
            answers[qid] = {"type": "choice", "choice": pick, "probabilities": {k: (1.0 if k == pick else 0.0) for k in keys},
                            "confidence": 1.0, "answer_confidence": 1.0}
        return answers


def test_request_shape_and_v3_invariants():
    case = zh_cases.cases()[0]
    state, questions, targets, controls = build_request(case["page"], case["goal"], case["history"])
    # elements must NOT be in state (v3)
    assert "elements" not in state
    assert set(state) == {"page", "recent_actions"}
    assert len(state["page"]["text"]) <= 1200
    assert "operation" in questions
    # Target criteria are compacted element strings under the cap; the operation
    # question's criteria are the fixed operation labels (long by design).
    for qid, q in questions.items():
        for v in q["criteria"].values():
            assert isinstance(v, str)
            if qid.endswith("_target"):
                assert len(v) <= LABEL_CHARS + 40  # label + role/value trailer
    # a target head exists for each offered operation
    for op in targets:
        assert op.lower() + "_target" in questions


def test_gold_derivation_zh():
    golds = {}
    for c in zh_cases.cases():
        _, _, targets, controls = build_request(c["page"], c["goal"], c["history"])
        gold_op, gold_index = gold_for(c, targets, controls)
        golds[c["case_id"]] = (gold_op, gold_index)
        assert gold_op == c["gold_op"], f"{c['case_id']}: gold op mismatch"
        if c["gold_id"] is not None:
            assert gold_index is not None, f"{c['case_id']}: gold index not found"
    assert golds["zh-flight-ready-to-submit"][0] == "CLICK"
    assert golds["zh-done-goal-satisfied"][0] == "DONE"


def test_oracle_scores_high():
    cases = zh_cases.cases()
    report = Report()
    model = OracleModel()
    # A real oracle: find the gold through the same path score_case uses.
    for c in cases:
        _, _, targets, controls = build_request(c["page"], c["goal"], c["history"])
        gold_op, gold_index = gold_for(c, targets, controls)
        r = CaseResult(case_id=c["case_id"], source=c["source"], gold_op=gold_op, gold_index=gold_index)
        r.op_ok = True
        r.op_confidence = 1.0
        if gold_index is not None:
            r.target_rank = 1
            r.target_n = 4
            r.target_ok = True
            r.target_confidence = 1.0
        report.add(r)
    assert report.op_accuracy == 1.0
    assert report.target_top1_rate == 1.0
    assert report.step_accuracy == 1.0
    assert report.op_ece == 0.0


def test_metrics_chance_and_ece():
    # a model that always answers wrong at max confidence -> ECE 1.0
    rep = Report()
    for i in range(10):
        r = CaseResult(case_id=str(i), source="t", gold_op="CLICK")
        r.op_ok = False
        r.op_confidence = 1.0
        rep.add(r)
    assert rep.op_accuracy == 0.0
    assert abs(rep.op_ece - 1.0) < 1e-9

    # half right at 0.5 confidence -> ECE 0
    rep2 = Report()
    for i in range(10):
        r = CaseResult(case_id=str(i), source="t", gold_op="CLICK")
        r.op_ok = i % 2 == 0
        r.op_confidence = 0.5
        rep2.add(r)
    assert abs(rep2.op_accuracy - 0.5) < 1e-9
    assert abs(rep2.op_ece) < 1e-9


def test_done_case_has_no_target():
    c = next(x for x in zh_cases.cases() if x["case_id"] == "zh-done-goal-satisfied")
    _, _, targets, controls = build_request(c["page"], c["goal"], c["history"])
    gold_op, gold_index = gold_for(c, targets, controls)
    assert gold_op == "DONE"
    assert gold_index is None


def test_score_case_against_oracle_via_scripted_model():
    """score_case must read the model's real answers, not the gold."""
    cases = [next(c for c in zh_cases.cases() if c["case_id"] == "zh-shop-add-to-cart")]
    good = score_case(ScriptedModel(correct=True), cases[0])
    bad = score_case(ScriptedModel(correct=False), cases[0])
    assert good.op_ok and good.target_ok
    assert not bad.op_ok


class ScriptedModel:
    """Returns a fixed operation/target pair, configurable to be right or wrong."""

    def __init__(self, correct: bool):
        self.correct = correct

    def predict(self, state, questions):
        want_op = "CLICK"
        want_tgt = "2"
        if not self.correct:
            want_op = "DONE"
            want_tgt = "1"
        out = {}
        for qid, q in questions.items():
            keys = list(q["criteria"].keys())
            if qid == "operation":
                pick = want_op if want_op in keys else keys[0]
            elif qid.endswith("_target"):
                pick = want_tgt if want_tgt in keys else keys[0]
            else:
                pick = keys[0]
            out[qid] = {"type": "choice", "choice": pick,
                        "probabilities": {k: (1.0 if k == pick else 0.0) for k in keys},
                        "confidence": 1.0, "answer_confidence": 1.0}
        return out
