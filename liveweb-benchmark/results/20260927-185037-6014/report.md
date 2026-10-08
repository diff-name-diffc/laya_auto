# liveweb-benchmark report

- generated: `2026-09-27T18:54:04+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 4.6, mean duration 13.4s, decision p50/p95 568.8/636.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 4.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-88893885e5a626e0` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-ba18ee0d190218d9` | done | ✅ | ✅ | 4 | 8 |  |
| `gen-9467fa2be5352f82` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-f3766d87c0e07b1e` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-29311d2ee1fb49ae` | done | ✅ | ✅ | 12 | 37 |  |
| `gen-09d8a1cfc9b280a8` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-71182272a98531dd` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-1224f8df5cde0120` | bot-challenge | ❌ | ❌ | 7 | 29 | missing evidence: [['profiling']] |

## Step outcomes

- `executed`: 23 (62%)
- `done`: 6 (16%)
- `done-rejected`: 5 (14%)
- `page changed since the decision (url or marker mismatch)`: 2 (5%)
- `refused-empty-enter`: 1 (3%)

low-confidence decisions (< τ): 0
