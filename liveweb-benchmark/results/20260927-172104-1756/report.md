# liveweb-benchmark report

- generated: `2026-09-27T17:24:53+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 10.0, mean duration 21.5s, decision p50/p95 462.1/716.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 9.5 |
| google | 6 | 83% | 83% | 10.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-59aaa35e5c6ae17e` | done | ✅ | ✅ | 7 | 12 |  |
| `gen-7b710b15d811023e` | repeat-loop | ❌ | ❌ | 29 | 78 | missing evidence: [['review', 'code']] |
| `gen-a3be65d573618cd1` | done | ❌ | ❌ | 11 | 23 | url lacks 'github.com/search' |
| `gen-eb4c30e441c28bec` | done | ✅ | ✅ | 7 | 21 |  |
| `gen-cd580449bd0764e7` | done | ✅ | ✅ | 12 | 18 |  |
| `gen-feb71c944ca11f77` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-de4ec62e43396b2f` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-97ece0da7c1f955d` | done | ❌ | ❌ | 8 | 12 | missing evidence: [['vllm']] |

## Step outcomes

- `executed`: 48 (60%)
- `stale`: 10 (12%)
- `done-rejected`: 8 (10%)
- `done`: 7 (9%)
- `page changed since the decision (url or marker mismatch)`: 4 (5%)
- `refused-empty-enter`: 3 (4%)

low-confidence decisions (< τ): 3
