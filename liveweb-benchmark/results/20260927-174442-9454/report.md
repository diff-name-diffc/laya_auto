# liveweb-benchmark report

- generated: `2026-09-27T17:48:59+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **7/8** (88%) — DONE **and** independently verified
- independently verified **7/8** (88%)
- found-but-never-stopped: **0**
- mean steps 11.5, mean duration 25.2s, decision p50/p95 576.3/760.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 100% | 100% | 8.0 |
| google | 7 | 86% | 86% | 12.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-3cb66c26f00af3b1` | done | ✅ | ✅ | 8 | 20 |  |
| `gen-b2a869396d96f69c` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-a4c57f85232ff1ee` | done | ✅ | ✅ | 18 | 31 |  |
| `gen-99edd46e3439c21d` | done | ✅ | ✅ | 16 | 24 |  |
| `gen-e4bd4d9615553ea1` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-257d31524e173401` | done | ✅ | ✅ | 4 | 9 |  |
| `gen-20849025700c78ab` | done | ❌ | ❌ | 25 | 88 | url lacks 'google.com/search' |
| `gen-614d685e70a6f242` | done | ✅ | ✅ | 11 | 15 |  |

## Step outcomes

- `executed`: 59 (64%)
- `stale`: 13 (14%)
- `done-rejected`: 8 (9%)
- `done`: 8 (9%)
- `refused-empty-enter`: 2 (2%)
- `page changed since the decision (url or marker mismatch)`: 2 (2%)

low-confidence decisions (< τ): 6
