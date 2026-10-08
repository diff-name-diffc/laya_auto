"""A deterministic fake backend: exercises the protocol layer without a model."""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.backends.base import Backend, BackendError, DecisionResult, register


class FakeBackend(Backend):
    name = "fake"

    def load(self) -> None:
        self._loaded = True

    def models(self):
        return ["fake"]

    def predict(self, state, questions, model: Optional[str] = None) -> DecisionResult:
        # Mirror Laya's answer shapes so the protocol layer is tested for real.
        answers: Dict[str, Any] = {}
        for qid, q in questions.items():
            qtype = q.get("type")
            if qtype == "choice":
                keys = list(q.get("criteria", {}).keys()) or ["a", "b"]
                answers[qid] = {
                    "type": "choice",
                    "choice": keys[0],
                    "probabilities": {k: round(1.0 / len(keys), 4) for k in keys},
                    "confidence": 0.5,
                    "answer_confidence": 0.5,
                    "action": {"act_probability": 1.0},
                }
            elif qtype == "noul":
                answers[qid] = {"type": "noul", "noul": 0.5, "confidence": 0.5,
                                "answer_confidence": 0.5, "action": {"act_probability": 1.0}}
            elif qtype == "score":
                crit = q.get("criteria", [])
                answers[qid] = {"type": "score", "score": 0.0,
                                "legend": {str(i): c for i, c in enumerate(crit)},
                                "probabilities": {str(i): round(1.0 / max(1, len(crit)), 4)
                                                  for i in range(len(crit))},
                                "confidence": 0.5, "answer_confidence": 0.5,
                                "action": {"act_probability": 1.0}}
            else:
                answers[qid] = {"type": qtype}

        payload = {
            "model": "fake-rl-agent",
            "answers": answers,
            "usage": {"input_tokens": 0, "output_tokens": 0},
            "routing": {"model": "fake", "repo": "local", "reason": "fake backend"},
        }
        return DecisionResult(payload=payload, latency_ms=0.0, backend=self.name)


class ErrorBackend(Backend):
    """Raises a client-correctable error, to test the 422 mapping."""

    name = "error"

    def load(self) -> None:
        self._loaded = True

    def models(self):
        return ["error"]

    def predict(self, state, questions, model: Optional[str] = None) -> DecisionResult:
        raise BackendError("question 'x': options do not fit in head_max_len")


register("fake", FakeBackend)
register("error", ErrorBackend)
