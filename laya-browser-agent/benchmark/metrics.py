"""Metrics for browser-decision correctness.

The first four mirror the official fine-tune eval (``code/finetune/eval.py``) so
numbers are comparable to the published ones:

* **operation accuracy** -- top-1 of the ``operation`` question.
* **target top-1** -- top-1 of the ``<op>_target`` question, *given* the gold
  operation (this isolates target selection from operation choice, exactly as
  upstream reports it).
* **mean normalized rank** -- where the gold target lands, divided by the option
  count; 0 is best, 0.5 is chance for a uniform random guess.
* **per-operation breakdown** -- accuracy split by CLICK / TYPE_TEXT / SELECT /
  DONE.

The last two are additions:

* **end-to-end step accuracy** -- operation *and* target both correct, the
  quantity that actually matters for a running agent.
* **Expected Calibration Error (ECE)** -- whether the reported confidence is
  trustworthy. Laya's whole pitch is calibrated probabilities, so a benchmark
  that ignores calibration would miss its main claim.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _top1(probs: Dict[str, float]) -> Optional[str]:
    if not probs:
        return None
    return max(probs, key=probs.get)


def _ece(pairs: List[tuple], bins: int = 10) -> float:
    """Expected Calibration Error over (confidence, correct) pairs."""
    if not pairs:
        return 0.0
    buckets: List[List[tuple]] = [[] for _ in range(bins)]
    for conf, correct in pairs:
        idx = min(bins - 1, max(0, int(conf * bins)))
        buckets[idx].append((conf, correct))
    total = len(pairs)
    ece = 0.0
    for bucket in buckets:
        if not bucket:
            continue
        avg_conf = sum(c for c, _ in bucket) / len(bucket)
        acc = sum(1 for _, ok in bucket if ok) / len(bucket)
        ece += (len(bucket) / total) * abs(avg_conf - acc)
    return ece


@dataclass
class CaseResult:
    case_id: str
    source: str
    gold_op: Optional[str]
    op_ok: bool = False
    gold_index: Optional[str] = None
    target_rank: Optional[int] = None
    target_n: Optional[int] = None
    target_ok: Optional[bool] = None
    step_ok: bool = False
    op_confidence: float = 0.0
    target_confidence: float = 0.0
    latency_ms: float = 0.0
    error: Optional[str] = None
    # raw answers for inspection
    op_choice: Optional[str] = None
    target_choice: Optional[str] = None


@dataclass
class Report:
    n_cases: int = 0
    n_scored_op: int = 0
    n_scored_target: int = 0
    op_correct: int = 0
    target_top1: int = 0
    step_correct: int = 0
    rank_sum: float = 0.0
    op_cal_pairs: List[tuple] = field(default_factory=list)
    target_cal_pairs: List[tuple] = field(default_factory=list)
    by_source: Dict[str, List[int]] = field(default_factory=dict)      # [n, op_ok, tgt_ok, tgt_n, step_ok]
    by_operation: Dict[str, List[int]] = field(default_factory=dict)   # [n, op_ok, tgt_ok, tgt_n]
    latencies: List[float] = field(default_factory=list)
    errors: int = 0

    def add(self, r: CaseResult) -> None:
        self.n_cases += 1
        if r.error:
            self.errors += 1
            return
        self.latencies.append(r.latency_ms)

        if r.gold_op is None:
            return

        # --- operation metric (the operation question always exists) ---
        self.n_scored_op += 1
        self.op_correct += int(r.op_ok)
        self.op_cal_pairs.append((r.op_confidence, r.op_ok))

        src = self.by_source.setdefault(r.source, [0, 0, 0, 0, 0])
        src[0] += 1
        src[1] += int(r.op_ok)
        opk = self.by_operation.setdefault(r.gold_op, [0, 0, 0, 0])
        opk[0] += 1
        opk[1] += int(r.op_ok)

        # --- target metric (only when the case has a gold element) ---
        tgt_ok: Optional[bool] = None
        if r.gold_index is not None and r.target_rank is not None:
            self.n_scored_target += 1
            tgt_ok = bool(r.target_ok)
            self.target_top1 += int(tgt_ok)
            self.rank_sum += r.target_rank / max(1, r.target_n or 1)
            self.target_cal_pairs.append((r.target_confidence, tgt_ok))
            src[2] += int(tgt_ok)
            src[3] += 1
            opk[2] += int(tgt_ok)
            opk[3] += 1

        # --- end-to-end step: operation right AND (no target needed OR target top-1) ---
        step = r.op_ok and (tgt_ok is None or tgt_ok)
        self.step_correct += int(step)
        src[4] += int(step)

    # -- derived -----------------------------------------------------------
    @property
    def op_accuracy(self) -> float:
        return self.op_correct / self.n_scored_op if self.n_scored_op else 0.0

    @property
    def target_top1_rate(self) -> float:
        return self.target_top1 / self.n_scored_target if self.n_scored_target else 0.0

    @property
    def mean_norm_rank(self) -> float:
        return self.rank_sum / self.n_scored_target if self.n_scored_target else 0.0

    @property
    def step_accuracy(self) -> float:
        return self.step_correct / self.n_scored_op if self.n_scored_op else 0.0

    @property
    def op_ece(self) -> float:
        return _ece(self.op_cal_pairs)

    @property
    def target_ece(self) -> float:
        return _ece(self.target_cal_pairs)

    def latency_p(self, q: float) -> float:
        if not self.latencies:
            return 0.0
        s = sorted(self.latencies)
        return s[min(len(s) - 1, int(q * (len(s) - 1)))]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_cases": self.n_cases,
            "errors": self.errors,
            "operation": {
                "n": self.n_scored_op,
                "accuracy": round(self.op_accuracy, 4),
                "ece": round(self.op_ece, 4),
            },
            "target": {
                "n": self.n_scored_target,
                "top1": round(self.target_top1_rate, 4),
                "mean_norm_rank": round(self.mean_norm_rank, 4),
                "ece": round(self.target_ece, 4),
            },
            "end_to_end_step_accuracy": round(self.step_accuracy, 4),
            "latency_ms": {
                "p50": round(self.latency_p(0.50), 1),
                "p95": round(self.latency_p(0.95), 1),
            },
            "by_source": {
                k: {"n": v[0], "op_acc": round(v[1] / v[0], 3) if v[0] else 0.0,
                    "target_top1": round(v[2] / v[3], 3) if v[3] else None,
                    "step_acc": round(v[4] / v[0], 3) if v[0] else 0.0}
                for k, v in sorted(self.by_source.items())
            },
            "by_operation": {
                k: {"n": v[0], "op_acc": round(v[1] / v[0], 3) if v[0] else 0.0,
                    "target_top1": round(v[2] / v[3], 3) if v[3] else None}
                for k, v in sorted(self.by_operation.items())
            },
        }
