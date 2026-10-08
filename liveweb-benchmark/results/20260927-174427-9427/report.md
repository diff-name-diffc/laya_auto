# liveweb-benchmark report

- generated: `2026-09-27T17:49:04+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 7.1, mean duration 27.6s, decision p50/p95 561.7/730.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 11.0 |
| google | 7 | 86% | 86% | 6.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-e0f053b9433f92b9` | done | ✅ | ✅ | 20 | 26 |  |
| `gen-c835fa7cc68f9204` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-12371829b45b6568` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-0c2d96cb3a974782` | done | ❌ | ❌ | 11 | 101 | missing evidence: [['ruby']] |
| `gen-432f6ba0dd51c582` | done | ❌ | ❌ | 6 | 12 | missing evidence: [['react']] |
| `gen-e5e4a5e711ea4c03` | done | ✅ | ✅ | 4 | 58 |  |
| `gen-4a581b734ded2346` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-93fb644714672cc7` | done | ✅ | ✅ | 7 | 12 |  |

## Step outcomes

- `executed`: 32 (56%)
- `done-rejected`: 8 (14%)
- `done`: 8 (14%)
- `stale`: 6 (11%)
- `refused-empty-enter`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 5
