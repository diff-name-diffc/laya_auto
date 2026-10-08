"""Contamination / memorisation probe.

If a model scored well by *memorising* (page -> gold element), it will return the
same element regardless of the goal. If it is genuinely deciding, changing the
goal to name a different element on the same page should change its answer.

For each real Mind2Web page we build two cases:
  A) the annotated goal           -> expect the annotated gold element
  B) a goal that explicitly names a *different* element on the same page
     -> expect that other element

Metrics:
  goal_following_rate = of the swapped cases, how many picked the newly-named
                        element (B). High = reading the goal, not the page.
  memorisation_rate   = of the swapped cases, how many still picked the original
                        annotated gold (A). High = recall, not reasoning.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmark.browser_request import build_request, gold_for  # noqa: E402
from benchmark.mind2web import action_to_case  # noqa: E402
from benchmark.run import HttpModel  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "benchmark" / "data" / "train" / "train_0.json"


def _candidate_targets(case):
    """Clickable elements in the case's page, as (index, action)."""
    _, _, targets, _ = build_request(case["page"], case["goal"], case["history"])
    return targets.get("CLICK", {})


def build_probe(cases, n=40, seed=7):
    rng = random.Random(seed)
    probes = []
    for c in cases:
        targets = _candidate_targets(c)
        gold_a, gold_idx_a = gold_for(c, *_targets_tuple(c))
        if gold_a != "CLICK" or gold_idx_a is None:
            continue
        # pick a different clickable with a distinctive label
        others = [(idx, a) for idx, a in targets.items()
                  if idx != gold_idx_a and len(a["label"].split()) >= 1 and len(a["label"]) >= 3]
        if not others:
            continue
        idx_b, act_b = rng.choice(others)
        label_b = act_b["label"].split(" → ")[0]
        probes.append({
            "case_id": c["case_id"],
            "page": c["page"],
            "history": c["history"],
            "orig_goal": c["goal"],
            "gold_a": gold_idx_a,
            "gold_a_label": targets[gold_idx_a]["label"],
            "swap_goal": f"Click the control labelled '{label_b}'.",
            "gold_b": idx_b,
            "gold_b_label": act_b["label"],
        })
        if len(probes) >= n:
            break
    return probes


def _targets_tuple(case):
    _, _, targets, controls = build_request(case["page"], case["goal"], case["history"])
    return targets, controls


def main():
    model_spec = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8811"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 40

    from benchmark.mind2web import iter_cases
    raw = list(iter_cases([DATA], max_cases=400))
    probes = build_probe(raw, n=n)
    print(f"built {len(probes)} probes from {len(raw)} Mind2Web cases", file=sys.stderr)

    model = HttpModel(model_spec)

    follow = recall = other = 0
    rows = []
    for p in probes:
        # A: original goal
        sa, qa, ta, ca = build_request(p["page"], p["orig_goal"], p["history"])
        ra = model.predict(sa, qa)
        pick_a = ra["click_target"]["choice"] if "click_target" in ra else None

        # B: swapped goal naming a different element
        sb, qb, tb, cb = build_request(p["page"], p["swap_goal"], p["history"])
        rb = model.predict(sb, qb)
        pick_b = rb["click_target"]["choice"] if "click_target" in rb else None

        if pick_b == p["gold_b"]:
            follow += 1
            verdict = "goal-following"
        elif pick_b == p["gold_a"]:
            recall += 1
            verdict = "MEMORISED(orig gold)"
        else:
            other += 1
            verdict = "other"
        rows.append((p["case_id"], pick_a == p["gold_a"], pick_b, p["gold_b"], verdict,
                     p["gold_a_label"][:24], p["gold_b_label"][:24]))

    N = len(probes)
    print(f"\n=== probes={N} ===")
    print(f"  goal-following (picked the newly named element) : {follow}/{N} = {follow/N:.2f}")
    print(f"  memorised      (kept original annotated gold)   : {recall}/{N} = {recall/N:.2f}")
    print(f"  other                                           : {other}/{N} = {other/N:.2f}")
    print("\n  per-probe (orig_ok | swap_pick vs expected):")
    for r in rows[:20]:
        print(f"    {r[0][:34]:34} orig_ok={str(r[1]):5} swap={r[2]:>4} expect={r[3]:>4} {r[4]:<20} A={r[5]!r} B={r[6]!r}")


if __name__ == "__main__":
    main()
