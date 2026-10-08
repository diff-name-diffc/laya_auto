"""Convert distill/dataset.jsonl into the official laya-browser finetune contract.

Pre-research findings (from cklxx/laya-browser on HF, code/finetune/):

* trainer  = their ``train.py`` (RLCD: noisy-logit PG + soft CE), continue-
  trained FROM a checkpoint via ``LAYA_BASE`` -- exactly how v17s continued
  v15s. No peft/LoRA support; the practical equivalent is a 1-epoch
  continuation with lowered encoder LR (2.5e-5 default).
* data in  = ``build_items.py pages.jsonl cases.jsonl [more cases...]`` where a
  case carries either ``page`` (int index into pages.jsonl) or an inline
  ``page_obj``; required keys: goal / history / gold_op / gold_id / source.
  Non-(mind2web|nnetnav) sources need an int ``page`` (used only for the
  held-out split); DONE-kind cases MUST carry ``page_obj``; ``source ==
  "dagger"`` is skipped entirely.

This converter emits ONE case file with inline ``page_obj`` (self-contained,
no page store to keep in sync), maps our three sources to their ``kind``
field, and validates every case against the gold_for contract before writing.

    python finetune/convert_distill.py distill/dataset.jsonl finetune/out/cases_liveweb.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agentbench.request_builder import action_space  # the byte-compatible port of common_ft

_KIND = {"liveweb:rescue": "rescue", "liveweb:model-step": "step", "liveweb:done": "done"}


def convert_case(case: Dict[str, Any]) -> Dict[str, Any]:
    page = case["page"]
    return {
        "case_id": case["case_id"],
        "page_obj": {"url": page.get("url"), "title": page.get("title"),
                     "text": page.get("text"), "actions": page.get("actions", [])},
        "page": -1,  # no pages store (inline page_obj); -1 short-circuits the
        # suite-URL filter and lands outside the 1-in-5 held-out split (-1 % 5 == 4)
        "goal": case["goal"],
        "history": case.get("history", []),
        "gold_op": case["gold_op"],
        "gold_id": case.get("gold_id"),
        "source": "liveweb",
        "kind": _KIND.get(case["source"], "step"),
        "website": page.get("url", "").split("/")[2] if "/" in page.get("url", "") else "",
        "note": case.get("rationale", "")[:200],
    }


def validate(converted: Dict[str, Any]) -> str:
    """Return an error string, or '' if the case passes the gold_for contract."""
    c = converted
    if not c["page_obj"].get("actions"):
        return "empty action table"
    if c["gold_op"] == "DONE":
        return "" if c.get("kind") == "done" else "DONE gold needs kind=done (page_obj present)"
    _, targets, controls = action_space(c["page_obj"]["actions"])
    if c["gold_op"] in targets:
        if not any(a["id"] == c["gold_id"] for a in targets[c["gold_op"]].values()):
            return f"gold_id {c['gold_id']!r} not in {c['gold_op']} targets"
    elif c["gold_op"] in controls:
        if controls[c["gold_op"]]["id"] != c["gold_id"]:
            return f"control id mismatch for {c['gold_op']}"
    else:
        return f"gold_op {c['gold_op']} not representable"
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset", help="distill/dataset.jsonl (our schema)")
    ap.add_argument("out", help="output cases file for build_items.py")
    args = ap.parse_args()

    cases = [json.loads(l) for l in open(args.dataset, encoding="utf-8")]

    # eval hygiene: a case whose goal verbatim matches a benchmark-suite task
    # makes that task a memorisation test -- never train on it
    from agentbench.tasks import TASKS
    suite = {t.goal for t in TASKS}
    leaks = [c for c in cases if c["goal"] in suite]
    cases = [c for c in cases if c["goal"] not in suite]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bad = []
    with out_path.open("w", encoding="utf-8") as fh:
        for case in cases:
            converted = convert_case(case)
            err = validate(converted)
            if err:
                bad.append((converted["case_id"], err))
                continue
            fh.write(json.dumps(converted, ensure_ascii=False) + "\n")
    print(f"converted {len(cases) - len(bad)}/{len(cases)} cases "
          f"(leaked-skipped {len(leaks)}) -> {out_path}")
    for cid, err in bad[:10]:
        print(f"  dropped {cid}: {err}")
    return 0 if len(bad) < len(cases) / 2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
