# liveweb-benchmark report

- generated: `2026-09-27T23:08:38+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 9.4, mean duration 25.2s, decision p50/p95 580.3/660.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 9.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-8dde046e43d4f89e` | done | ✅ | ✅ | 14 | 39 |  |
| `gen-1959c74ab6b8ad93` | done | ✅ | ✅ | 13 | 19 |  |
| `gen-fa33e4f433622253` | done | ❌ | ❌ | 14 | 71 | missing evidence: [['java']] |
| `gen-4bfb49173487843c` | unstable-page | ❌ | ❌ | 6 | 4 | missing evidence: [['golang']] |
| `gen-8a6fdcac3536a362` | done | ✅ | ✅ | 13 | 50 |  |
| `gen-35791f724b205828` | done | ✅ | ✅ | 9 | 11 |  |
| `gen-acfb58831edb3b2e` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-ba059d870cdd8a33` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 44 (59%)
- `stale`: 18 (24%)
- `done`: 7 (9%)
- `page changed since the decision (url or marker mismatch)`: 4 (5%)
- `done-rejected`: 2 (3%)

low-confidence decisions (< τ): 14
