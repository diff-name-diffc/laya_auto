# liveweb-benchmark report

- generated: `2026-09-27T17:33:05+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 4.4, mean duration 17.7s, decision p50/p95 569.5/897.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 4.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-bc6dec5f9f2c8d75` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-d8cadd8945c764de` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-a6ac7889c328734b` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-3f5e3d2d540b0c44` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-26fa2cfe24d2b7e2` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-3f45ac6d90b49012` | done | ❌ | ❌ | 5 | 95 | url lacks 'react.dev' |
| `gen-0d006751f71bbd22` | done | ❌ | ❌ | 4 | 8 | url lacks 'q=rabbitmq' |
| `gen-65a566a5a1371e7b` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 16 (46%)
- `done`: 8 (23%)
- `done-rejected`: 7 (20%)
- `stale`: 2 (6%)
- `refused-empty-enter`: 2 (6%)

low-confidence decisions (< τ): 0
