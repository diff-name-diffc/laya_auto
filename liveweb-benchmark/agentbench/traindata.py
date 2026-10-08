"""Distillation data: every VLM rescue (and every step of a verified-successful
run) becomes a fine-tuning case, live, as the run happens.

The case schema matches the laya browser fine-tune's training format (the same
dicts ``benchmark/browser_request.build_request`` consumes), so the exported
JSONL plugs straight into the fine-tune pipeline:

    {"case_id", "source", "goal", "page": {url,title,text,actions},
     "history": [...], "gold_op", "gold_id", "rationale"}

Signal hierarchy (what makes a case trustworthy):

* ``liveweb:rescue`` -- the fast model stalled and a VLM chose the corrective
  action on that exact observation. Teacher labels: the highest-signal data
  this pipeline produces, and the explicit remedy for the measured weaknesses
  (premature DONE, third-step cliff, list selection).
* ``liveweb:model-step`` -- steps the fast model itself executed, emitted only
  when the run ENDED verified-successful, so the whole trajectory sat on a
  gold path.

Rescue cases are exported regardless of the run's final verdict: the VLM's
choice on the observed page is the label for that page, independent of what
happened later.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

_KIND_TO_OP = {
    "click": "CLICK",
    "fill": "TYPE_TEXT",
    "select": "SELECT",
    "enter": "PRESS_ENTER",
    "wait": "WAIT",
}


def gold_of(action: Dict[str, Any]) -> Optional[tuple]:
    """(gold_op, gold_id) for an observed action, or None if unmappable."""
    kind = action.get("kind")
    if kind == "scroll":
        op = "SCROLL_DOWN" if int(action.get("delta", 0) or 0) > 0 else "SCROLL_UP"
        return op, action["id"]
    op = _KIND_TO_OP.get(kind)
    if op is None:
        return None
    return op, action["id"]


def make_case(kind: str, goal: str, page: Dict[str, Any], history: List[Dict[str, Any]],
              action: Dict[str, Any], rationale: str, task_id: str, seq: int) -> Optional[Dict[str, Any]]:
    gold = gold_of(action)
    if gold is None:
        return None
    gold_op, gold_id = gold
    return {
        "case_id": f"lw-{task_id}-{seq}-{kind}",
        "source": f"liveweb:{kind}",
        "goal": goal,
        "page": {"url": page.get("url"), "title": page.get("title"),
                 "text": page.get("text"), "actions": page.get("actions", [])},
        "history": [dict(h) for h in (history or [])[-10:]],
        "gold_op": gold_op,
        "gold_id": gold_id,
        "rationale": rationale[:300],
    }


def make_done_case(goal: str, page: Dict[str, Any], history: List[Dict[str, Any]],
                   task_id: str, seq: int, rationale: str) -> Dict[str, Any]:
    """The terminal DONE on a satisfied page: the ONLY positive signal that
    teaches *when stopping is correct* -- premature DONE and never-stop are both
    measured weaknesses, and pure failure data cannot teach the second one."""
    return {
        "case_id": f"lw-{task_id}-{seq}-done",
        "source": "liveweb:done",
        "goal": goal,
        "page": {"url": page.get("url"), "title": page.get("title"),
                 "text": page.get("text"), "actions": page.get("actions", [])},
        "history": [dict(h) for h in (history or [])[-10:]],
        "gold_op": "DONE",
        "gold_id": None,
        "rationale": rationale[:300],
    }


# rare/weak operations first: the cap keeps verified-run replay from drowning
# the corrective signal in easy TYPE_TEXT/PRESS_ENTER steps the model aces
_OP_PRIORITY = ["SELECT", "SCROLL_DOWN", "SCROLL_UP", "CLICK",
                "TYPE_TEXT", "PRESS_ENTER", "WAIT"]


# run3: the VLM teacher itself mis-picks nav/filter controls on GitHub's
# trending feed (run2 measured 7/11 rescue picks were "Repositories" /
# "Language: Any"). A rescue case on a trending page only teaches the right
# lesson when its gold is a content row (an "owner / repo" entry link) or a
# language the goal itself names -- everything else is quarantined.
_NAV_BAIT = {"repositories", "trending", "home", "explore", "topics",
             "collections", "events", "sponsors", "back to search",
             "search or jump to"}


def _trending_rescue_ok(case: Dict[str, Any]) -> bool:
    url = (case.get("page", {}).get("url") or "").lower()
    if "github.com/trending" not in url:
        return True
    label = ""
    for a in case.get("page", {}).get("actions", []):
        if a.get("id") == case.get("gold_id"):
            label = str(a.get("label") or "").strip()
            break
    low = label.lower()
    if not low or low in _NAV_BAIT or low.startswith("language:") \
            or low.startswith("search or jump to"):
        return False
    if " / " in label:                       # "owner / repo" content row
        return True
    return low in (case.get("goal") or "").lower()   # language-filter gold


class CaseSink:
    """Failure-primary distillation policy:

    * rescue cases -- always written (every one is a point of failure);
    * the terminal DONE case (verified runs only) teaches correct stopping;
    * at most ``step_cap`` intermediate model steps from verified runs, ordered
      rare-op-first and deduped -- replay to stabilise, not to drown.
    """

    def __init__(self, task_id: str, step_cap: int = 3):
        self.task_id = task_id
        self.step_cap = step_cap
        self.cases: List[Dict[str, Any]] = []
        self.quarantined: List[str] = []

    def add(self, case: Dict[str, Any]) -> None:
        if case:
            self.cases.append(case)

    def _keep_rescues(self, cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        keep = []
        for c in cases:
            if c["source"] == "liveweb:rescue" and not _trending_rescue_ok(c):
                self.quarantined.append(c["case_id"])
                continue
            keep.append(c)
        return keep

    def finalize(self, verified: bool) -> List[Dict[str, Any]]:
        if not verified:
            # failed runs contribute ONLY the corrective rescue cases; an
            # unverified DONE as positive data would be a poison sample
            return self._keep_rescues(
                [c for c in self.cases if c["source"] == "liveweb:rescue"])
        out = self._keep_rescues([c for c in self.cases
                                  if c["source"] in ("liveweb:rescue", "liveweb:done")])
        seen: set = set()
        steps: List[Dict[str, Any]] = []
        for c in self.cases:
            if c["source"] != "liveweb:model-step":
                continue
            key = (c["page"].get("url", "").split("&zx=")[0], c["gold_op"], c["gold_id"])
            if key in seen:
                continue
            seen.add(key)
            steps.append(c)
        steps.sort(key=lambda c: _OP_PRIORITY.index(c["gold_op"])
                   if c["gold_op"] in _OP_PRIORITY else 99)
        return out + steps[:self.step_cap]


def append_jsonl(path: Path, cases: List[Dict[str, Any]]) -> int:
    if not cases:
        return 0
    with path.open("a", encoding="utf-8") as fh:
        for case in cases:
            fh.write(json.dumps(case, ensure_ascii=False) + "\n")
    return len(cases)


# --- merge CLI: consolidate run outputs into one deduped dataset -------------


def _dedup_key(case: Dict[str, Any]) -> tuple:
    import hashlib
    url = (case.get("page", {}).get("url") or "").split("&zx=")[0].split("?t=")[0]
    text_head = (case.get("page", {}).get("text") or "")[:200]
    # page-text head carries dynamic noise (doodles, timestamps) that let
    # near-identical lessons slip through; url+goal+gold IS the lesson identity
    payload = f"{url}|{case.get('gold_op')}|{case.get('gold_id')}|{case.get('goal')}"
    return hashlib.sha1(payload.encode()).hexdigest()


def merge(results_root: str, out_path: str) -> Dict[str, Any]:
    """Merge every results/*/traindata.jsonl under results_root into one
    deduplicated dataset. Near-identical cases (same page state + same gold)
    collapse to one -- repeated runs on the same pages would otherwise
    overweight a handful of Google homepage fills."""
    seen: set = set()
    merged: List[Dict[str, Any]] = []
    # one level (results/<run>/traindata.jsonl) plus two (results/<batch>/<ts>/…)
    files = sorted(set(Path(results_root).glob("*/traindata.jsonl"))
                   | set(Path(results_root).glob("*/*/traindata.jsonl")))
    for path in files:
        for line in path.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            case = json.loads(line)
            key = _dedup_key(case)
            if key in seen:
                continue
            seen.add(key)
            merged.append(case)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for case in merged:
            fh.write(json.dumps(case, ensure_ascii=False) + "\n")
    from collections import Counter
    stats = {
        "files": len(files),
        "merged_cases": len(merged),
        "by_source": dict(Counter(c["source"] for c in merged)),
        "by_gold_op": dict(Counter(c["gold_op"] for c in merged)),
        "by_task": dict(Counter(c["case_id"].rsplit("-", 2)[0] for c in merged)),
        "out": str(out),
    }
    return stats


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "results"
    dest = sys.argv[2] if len(sys.argv) > 2 else "distill/dataset.jsonl"
    print(json.dumps(merge(root, dest), indent=1, ensure_ascii=False))
