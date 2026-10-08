"""run3 additions: trending-gold quarantine, two-level merge, vlm_rescues report."""

from __future__ import annotations

import json
from pathlib import Path

from agentbench.loop import RunResult, StepRecord
from agentbench.report import summarize
from agentbench.traindata import CaseSink, _trending_rescue_ok, merge


def _rescue(page_url, gold_id, label, goal="Open a repo about AI."):
    return {
        "case_id": "lw-x-1-rescue", "source": "liveweb:rescue", "goal": goal,
        "page": {"url": page_url, "title": "t", "text": "x", "actions": [
            {"id": gold_id, "label": label, "kind": "click"},
        ]},
        "history": [], "gold_op": "CLICK", "gold_id": gold_id, "rationale": "r",
    }


TREND = "https://github.com/trending"


def test_trending_quarantine_drops_nav_bait_keeps_content_rows():
    assert not _trending_rescue_ok(_rescue(TREND, "click:1", "Repositories"))
    assert not _trending_rescue_ok(_rescue(TREND, "click:1", "Language: Any"))
    assert not _trending_rescue_ok(_rescue(TREND, "scroll_down", ""))  # control gold
    ok_row = _trending_rescue_ok(_rescue(TREND, "click:9", "torvalds / linux"))
    assert ok_row
    # a language link is gold only when the goal names it (language-filter task)
    assert _trending_rescue_ok(_rescue(TREND, "click:4", "Python",
                                       goal="show only the Python language repositories"))
    assert not _trending_rescue_ok(_rescue(TREND, "click:4", "Python",
                                           goal="open a repo about AI"))
    # non-trending pages are untouched
    assert _trending_rescue_ok(_rescue("https://github.com/", "click:1", "Repositories"))


def test_case_sink_finalizes_with_quarantine():
    sink = CaseSink("t")
    good = _rescue(TREND, "click:9", "foo / bar")
    bait = _rescue(TREND, "click:1", "Repositories")
    sink.add(good)
    sink.add(bait)
    out = sink.finalize(verified=False)
    assert out == [good]
    assert sink.quarantined == [bait["case_id"]]


def test_merge_reads_two_level_run_dirs(tmp_path: Path):
    one = tmp_path / "run-a"; one.mkdir()
    (one / "traindata.jsonl").write_text(
        json.dumps(_rescue("https://x/", "click:1", "Go")) + "\n")
    two = tmp_path / "batch-b" / "20260101-000000-1"; two.mkdir(parents=True)
    (two / "traindata.jsonl").write_text(
        json.dumps(_rescue("https://y/", "click:2", "Rust")) + "\n")
    out_path = tmp_path / "merged.jsonl"
    stats = merge(str(tmp_path), str(out_path))
    lines = [json.loads(l) for l in out_path.read_text().splitlines()]
    assert stats["files"] == 2
    assert len(lines) == 2


def _record(rescues: int):
    steps = [StepRecord(step=i, operation="CLICK", operation_confidence=0.9,
                        outcome="executed") for i in range(rescues)]
    steps += [StepRecord(step=len(steps), operation="VLM_RESCUE",
                         operation_confidence=1.0, outcome="executed")]
    result = RunResult(goal="g", status="done", steps=steps, total_ms=1.0)
    return {"task": type("T", (), {"source": "github", "task_id": "t"})(),
            "result": result, "verified": True, "success": True}


def test_summarize_counts_vlm_rescues():
    s = summarize([_record(0), _record(2)])
    assert s["vlm_rescues"] == 2
