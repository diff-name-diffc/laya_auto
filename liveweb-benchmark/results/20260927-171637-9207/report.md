# liveweb-benchmark report

- generated: `2026-09-27T17:20:07+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 9.6, mean duration 19.4s, decision p50/p95 498.9/744.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 9.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-674c806711b46a94` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-d3bc799db78002a8` | max-steps | ❌ | ❌ | 30 | 81 | missing evidence: [['next.js']] |
| `gen-537fb0fb433f29f1` | done | ✅ | ✅ | 7 | 10 |  |
| `gen-95fdca212f66362c` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-32d2db5d9ca4ac13` | done | ✅ | ✅ | 12 | 14 |  |
| `gen-ff56420ed8b7a718` | done | ❌ | ❌ | 10 | 19 | url lacks 'q=review' |
| `gen-80a4500d0b7f13f5` | done | ✅ | ✅ | 4 | 8 |  |
| `gen-850321af747c0fe3` | done | ✅ | ✅ | 4 | 8 |  |

## Step outcomes

- `executed`: 50 (65%)
- `stale`: 9 (12%)
- `done-rejected`: 7 (9%)
- `done`: 7 (9%)
- `refused-empty-enter`: 3 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 1
