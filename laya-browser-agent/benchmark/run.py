"""Benchmark runner.

Two transports so the same suite can score a served endpoint or a checkpoint
directly:

* ``--base-url``   score a running ``/v1/systemone`` server (the real deployment
                   path, including the HTTP contract).
* ``--model``      load a checkpoint in-process (fast, for model-vs-model).

Example:

    python -m benchmark.run --dataset zh --base-url http://127.0.0.1:8801
    python -m benchmark.run --dataset mind2web --model /path/to/v10s --max-cases 200
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import mind2web, parallel_cases, zh_cases
from .browser_request import build_request, gold_for
from .metrics import CaseResult, Report


# ---------------------------------------------------------------------------
# transports
# ---------------------------------------------------------------------------

class HttpModel:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 120,
                 model: Optional[str] = None):
        self.url = base_url.rstrip("/") + "/v1/systemone"
        self.key = api_key
        self.timeout = timeout
        self.model = model

    def predict(self, state, questions) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        body: Dict[str, Any] = {"state": state, "questions": questions}
        if self.model:
            body["model"] = self.model
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(self.url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.load(resp)["answers"]


class LocalModel:
    def __init__(self, model: str, subfolder: Optional[str] = None, device: Optional[str] = None):
        os.environ.setdefault("USE_TF", "0")
        import laya

        kwargs: Dict[str, Any] = {"device": device}
        if subfolder:
            kwargs["subfolder"] = subfolder
        self.agent = laya.load(model, **kwargs)
        cfg = getattr(self.agent, "cfg", {}) or {}
        if cfg.get("head_max_len_train"):
            cfg["head_max_len"] = cfg["head_max_len_train"]

    def predict(self, state, questions) -> Dict[str, Any]:
        return self.agent.predict(state, questions)["answers"]


# ---------------------------------------------------------------------------
# scoring
# ---------------------------------------------------------------------------

def _top1(probs: Dict[str, float]) -> Optional[str]:
    return max(probs, key=probs.get) if probs else None


def score_case(model, case: Dict[str, Any]) -> CaseResult:
    state, questions, targets, controls = build_request(case["page"], case["goal"], case.get("history", []))
    gold_op, gold_index = gold_for(case, targets, controls)

    r = CaseResult(case_id=case["case_id"], source=case["source"], gold_op=gold_op, gold_index=gold_index)

    if gold_op is None:
        r.error = "gold operation not present in this page's vocabulary"
        return r

    try:
        t0 = time.perf_counter()
        answers = model.predict(state, questions)
        r.latency_ms = (time.perf_counter() - t0) * 1000
    except Exception as exc:  # noqa: BLE001
        r.error = str(exc)[:200]
        return r

    op = answers.get("operation", {})
    op_probs = op.get("probabilities", {})
    r.op_choice = op.get("choice") or _top1(op_probs)
    r.op_confidence = float(op_probs.get(r.op_choice, 0.0)) if r.op_choice else 0.0
    r.op_ok = r.op_choice == gold_op

    if gold_index is not None:
        tq = gold_op.lower() + "_target"
        ta = answers.get(tq, {})
        tprobs = ta.get("probabilities", {})
        r.target_choice = ta.get("choice") or _top1(tprobs)
        r.target_confidence = float(tprobs.get(r.target_choice, 0.0)) if r.target_choice else 0.0
        r.target_n = len(tprobs)
        if gold_index in tprobs:
            order = sorted(tprobs, key=tprobs.get, reverse=True)
            r.target_rank = order.index(gold_index) + 1
            r.target_ok = r.target_rank == 1
    return r


def run(model, cases: List[Dict[str, Any]], progress: bool = True) -> Report:
    report = Report()
    for i, case in enumerate(cases):
        res = score_case(model, case)
        report.add(res)
        if progress and (i + 1) % 50 == 0:
            print(f"  ... {i + 1}/{len(cases)}  op_acc={report.op_accuracy:.3f}", file=sys.stderr)
    return report


# ---------------------------------------------------------------------------
# datasets
# ---------------------------------------------------------------------------

def load_zh() -> List[Dict[str, Any]]:
    return zh_cases.cases()


def load_parallel() -> List[Dict[str, Any]]:
    return parallel_cases.cases()


def load_mind2web(data_dir: Path, split: str = "train", max_cases: int = 200) -> List[Dict[str, Any]]:
    mind2web._require_bs4()
    files: List[Path]
    if split == "train":
        files = sorted((data_dir / "train").glob("*.json"))
    else:
        raise SystemExit(
            f"unknown split {split!r}. Mind2Web's test split ships as an ENCRYPTED "
            f"zip (see benchmark/README.md); the public shards are train only. "
            f"Download them with: python -m benchmark.download --split train"
        )
    if not files:
        raise SystemExit(
            f"no task files under {data_dir} for split {split!r}. "
            f"Download with: python -m benchmark.download --split train"
        )
    return list(mind2web.iter_cases(files, max_cases=max_cases))


def main() -> int:
    ap = argparse.ArgumentParser(description="Browser-agent decision benchmark for Laya")
    ap.add_argument("--dataset", choices=["zh", "parallel", "mind2web"], required=True)
    ap.add_argument("--base-url", help="score a running /v1/systemone server")
    ap.add_argument("--api-key", default=os.environ.get("INFER_API_KEY"))
    ap.add_argument("--model-name", help="model id to send to the server (honoured if it serves it)")
    ap.add_argument("--model", help="load a checkpoint in-process instead")
    ap.add_argument("--subfolder")
    ap.add_argument("--device", default=os.environ.get("LAYA_DEVICE") or None)
    ap.add_argument("--split", default="train", choices=["train"])
    ap.add_argument("--data-dir", default="benchmark/data")
    ap.add_argument("--max-cases", type=int, default=200)
    ap.add_argument("--label", default="", help="name for this run in the output")
    ap.add_argument("--out", help="write the JSON report here")
    ap.add_argument("--dump-cases", help="write the resolved cases to this JSONL and exit")
    args = ap.parse_args()

    if args.dataset == "zh":
        cases = load_zh()
    elif args.dataset == "parallel":
        cases = load_parallel()
    else:
        cases = load_mind2web(Path(args.data_dir), args.split, args.max_cases)

    if args.dump_cases:
        with open(args.dump_cases, "w") as f:
            for c in cases:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"wrote {len(cases)} cases to {args.dump_cases}")
        return 0

    if args.base_url:
        model = HttpModel(args.base_url, args.api_key, model=args.model_name)
        label = args.label or (args.model_name or args.base_url)
    elif args.model:
        model = LocalModel(args.model, args.subfolder, args.device)
        label = args.label or args.model + (f"/{args.subfolder}" if args.subfolder else "")
    else:
        return int(bool(print("need --base-url or --model", file=sys.stderr)))

    print(f"benchmark: dataset={args.dataset} split={args.split if args.dataset=='mind2web' else '-'} "
          f"cases={len(cases)} target={label}", file=sys.stderr)
    report = run(model, cases)
    out = report.to_dict()
    out["dataset"] = args.dataset
    out["split"] = args.split if args.dataset == "mind2web" else None
    out["label"] = label

    print(json.dumps(out, indent=1, ensure_ascii=False))
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False))
        print(f"wrote {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
