"""Aggregate run results into the JSON + Markdown capability report.

Reported separately on purpose (spec §6): ``success`` requires BOTH the agent
stopping on DONE and independent verification; ``verified`` alone is reported
too, because "found the right page but never stopped" is a distinct, measurable
failure mode (3/6 in the reference evaluation).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List

from .tasks import Task


def _pct(values: List[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(len(s) - 1, max(0, int(q * (len(s) - 1) + 0.5)))
    return round(s[idx], 1)


def summarize(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """records: [{task, result(RunResult), verdict, fingerprint, ...}]"""
    n = len(records)
    successes = sum(1 for r in records if r["success"])
    verified = sum(1 for r in records if r["verified"])
    steps = [len(r["result"].steps) for r in records]
    durations = [r["result"].total_ms for r in records]
    latencies = [s.latency_ms for r in records for s in r["result"].steps]
    outcome_counts: Dict[str, int] = {}
    low_conf = 0
    vlm_rescues = 0
    for r in records:
        for s in r["result"].steps:
            key = s.outcome.split(":")[0]
            outcome_counts[key] = outcome_counts.get(key, 0) + 1
            if s.low_confidence:
                low_conf += 1
            if s.operation == "VLM_RESCUE":
                vlm_rescues += 1

    by_source: Dict[str, Dict[str, Any]] = {}
    for source in sorted({r["task"].source for r in records}):
        sub = [r for r in records if r["task"].source == source]
        by_source[source] = {
            "n": len(sub),
            "success": sum(1 for r in sub if r["success"]),
            "success_rate": round(sum(1 for r in sub if r["success"]) / len(sub), 3),
            "verified": sum(1 for r in sub if r["verified"]),
            "verified_rate": round(sum(1 for r in sub if r["verified"]) / len(sub), 3),
            "mean_steps": round(sum(len(r["result"].steps) for r in sub) / len(sub), 1),
        }

    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "n_tasks": n,
        "success": successes,
        "success_rate": round(successes / n, 3) if n else 0.0,
        "verified": verified,
        "verified_rate": round(verified / n, 3) if n else 0.0,
        "found_but_not_stopped": verified - successes,
        "mean_steps": round(sum(steps) / n, 1) if n else 0.0,
        "mean_duration_ms": round(sum(durations) / n) if n else 0,
        "decision_latency_ms": {"p50": _pct(latencies, 0.5), "p95": _pct(latencies, 0.95)},
        "step_outcomes": outcome_counts,
        "low_confidence_steps": low_conf,
        "vlm_rescues": vlm_rescues,
        "by_source": by_source,
    }


def write_report(out_dir: Path, meta: Dict[str, Any], records: List[Dict[str, Any]]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = summarize(records)

    payload = {
        "meta": meta,
        "summary": summary,
        "tasks": [
            {
                "task_id": r["task"].task_id,
                "source": r["task"].source,
                "goal": r["task"].goal,
                "fingerprint": r.get("fingerprint"),
                "status": r["result"].status,
                "verified": r["verified"],
                "success": r["success"],
                "steps": len(r["result"].steps),
                "vlm_rescues": sum(1 for s in r["result"].steps
                                   if s.operation == "VLM_RESCUE"),
                "total_ms": round(r["result"].total_ms),
                "error": r["result"].error,
                "verification": r["result"].verification or r["verdict"],
                "trajectory": [s.as_dict() for s in r["result"].steps],
            }
            for r in records
        ],
    }
    json_path = out_dir / "report.json"
    json_path.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")

    md_path = out_dir / "report.md"
    md_path.write_text(_markdown(meta, summary, records), encoding="utf-8")
    return out_dir


def _markdown(meta: Dict[str, Any], summary: Dict[str, Any], records: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# liveweb-benchmark report\n")
    lines.append(f"- generated: `{summary['generated_at']}`")
    lines.append(f"- backend: `{meta.get('base_url')}`")
    lines.append(f"- browser: CloakBrowser `{meta.get('browser_version')}` "
                 f"(humanize={meta.get('humanize')}, headless={meta.get('headless')})")
    lines.append(f"- max_steps={meta.get('max_steps')}, delay={meta.get('delay')}s\n")

    lines.append("## Summary\n")
    lines.append(f"- success **{summary['success']}/{summary['n_tasks']}** "
                 f"({summary['success_rate']:.0%}) — DONE **and** independently verified")
    lines.append(f"- independently verified **{summary['verified']}/{summary['n_tasks']}** "
                 f"({summary['verified_rate']:.0%})")
    lines.append(f"- found-but-never-stopped: **{summary['found_but_not_stopped']}**")
    lines.append(f"- VLM rescues: **{summary['vlm_rescues']}** "
                 f"(~{summary['vlm_rescues']/summary['n_tasks']:.1f}/task)")
    lines.append(f"- mean steps {summary['mean_steps']}, mean duration "
                 f"{summary['mean_duration_ms']/1000:.1f}s, decision p50/p95 "
                 f"{summary['decision_latency_ms']['p50']}/"
                 f"{summary['decision_latency_ms']['p95']} ms\n")

    lines.append("## By source\n")
    lines.append("| source | n | success | verified | mean steps |")
    lines.append("|---|---|---|---|---|")
    for source, s in summary["by_source"].items():
        lines.append(f"| {source} | {s['n']} | {s['success_rate']:.0%} "
                     f"| {s['verified_rate']:.0%} | {s['mean_steps']} |")

    lines.append("\n## Tasks\n")
    lines.append("| task | status | verified | success | steps | s | fail reason |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in records:
        secs = r["result"].total_ms / 1000
        reason = (r["verdict"].get("reason") if not r["verified"] else "") or (r["result"].error or "")
        lines.append(f"| `{r['task'].task_id}` | {r['result'].status} | "
                     f"{'✅' if r['verified'] else '❌'} | {'✅' if r['success'] else '❌'} | "
                     f"{len(r['result'].steps)} | {secs:.0f} | {str(reason)[:60]} |")

    lines.append("\n## Step outcomes\n")
    total = sum(summary["step_outcomes"].values())
    for k, v in sorted(summary["step_outcomes"].items(), key=lambda kv: -kv[1]):
        lines.append(f"- `{k}`: {v} ({v/total:.0%})" if total else f"- `{k}`: {v}")
    lines.append(f"\nlow-confidence decisions (< τ): {summary['low_confidence_steps']}")
    return "\n".join(lines) + "\n"
