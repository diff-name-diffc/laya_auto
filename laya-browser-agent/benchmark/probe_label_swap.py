"""Decisive memorisation probe: label swap.

The earlier goal-swap probe can be passed by simple label matching (the swapped
goal literally names the label). This one cannot.

For a real page + annotated gold we swap the *labels* of the gold element and a
distractor, keeping every index and role identical. Then:

  * a model that **memorised** (page -> index) keeps answering the same index,
    which after the swap holds the wrong label;
  * a model that **reasons** from the goal follows the label to its new index.

Reported:
  followed_label  -- picked the index that now carries the element the goal
                     describes (index changed after the swap) => reasoning
  kept_index      -- picked the original index regardless of the swap => recall
  neither         -- picked something else entirely
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmark.browser_request import build_request, gold_for  # noqa: E402
from benchmark.mind2web import iter_cases, action_to_case  # noqa: E402
from benchmark.run import HttpModel  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "benchmark" / "data" / "train" / "train_0.json"


def _gold(case):
    _, _, targets, controls = build_request(case["page"], case["goal"], case["history"])
    return gold_for(case, targets, controls), targets


def make_swap_case(case, rng):
    (gold_op, gold_idx), targets = _gold(case)
    if gold_op != "CLICK" or gold_idx is None:
        return None
    click = targets.get("CLICK", {})
    if len(click) < 2:
        return None
    others = [i for i in click if i != gold_idx]
    if not others:
        return None
    swap_idx = rng.choice(others)

    # deep-copy the page and swap the two elements' labels
    import copy
    page = copy.deepcopy(case["page"])
    node_of = {}
    for a in page["actions"]:
        node_of[a.get("node")] = a
    # find actions by their id in the click targets
    gold_action = click[gold_idx]
    swap_action = click[swap_idx]
    a_gold = node_of.get(gold_action.get("node"))
    a_swap = node_of.get(swap_action.get("node"))
    if a_gold is None or a_swap is None:
        return None
    lg, ls = a_gold["label"], a_swap["label"]
    a_gold["label"], a_swap["label"] = ls, lg   # labels exchanged, indices unchanged

    # after the swap, the goal's described element now sits at swap_idx
    return {
        "case_id": case["case_id"],
        "page": page,
        "history": case["history"],
        "goal": case["goal"],
        "orig_index": gold_idx,
        "orig_label": lg,
        "new_index": swap_idx,     # where the goal's element now lives
        "new_label_at_orig": ls,
    }


def main():
    spec = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8831"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    rng = random.Random(3)

    raw = list(iter_cases([DATA], max_cases=400))
    probes = []
    for c in raw:
        if c["gold_op"] != "CLICK":
            continue
        p = make_swap_case(c, rng)
        if p:
            probes.append(p)
        if len(probes) >= n:
            break
    print(f"built {len(probes)} label-swap probes", file=sys.stderr)

    model = HttpModel(spec)
    followed = kept = neither = 0
    rows = []
    for p in probes:
        state, questions, targets, controls = build_request(p["page"], p["goal"], p["history"])
        r = model.predict(state, questions)
        pick = r["click_target"]["choice"] if "click_target" in r else None
        if pick == p["new_index"]:
            followed += 1
            v = "follows-label"
        elif pick == p["orig_index"]:
            kept += 1
            v = "kept-INDEX"
        else:
            neither += 1
            v = "other"
        rows.append((p["case_id"], p["orig_index"], p["new_index"], pick, v,
                     p["orig_label"][:22], p["new_label_at_orig"][:22]))

    N = len(probes)
    print(f"\n=== label-swap probes = {N} ===")
    print(f"  follows the label to its new index (reasoning) : {followed}/{N} = {followed/N:.2f}")
    print(f"  kept the original index (memorisation)         : {kept}/{N} = {kept/N:.2f}")
    print(f"  neither                                        : {neither}/{N} = {neither/N:.2f}")
    print("\n  per-probe:")
    for r in rows[:20]:
        print(f"    {r[0][:30]:30} orig={r[1]:>4} new={r[2]:>4} pick={r[3]:>4} {r[4]:<14} goal={r[5]!r} atOrigNow={r[6]!r}")


if __name__ == "__main__":
    main()
