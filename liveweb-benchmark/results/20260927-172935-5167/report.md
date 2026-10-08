# liveweb-benchmark report

- generated: `2026-09-27T17:32:59+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 10.4, mean duration 18.7s, decision p50/p95 573.4/683.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 10.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-e5004ccd2d96dd44` | done | ✅ | ✅ | 7 | 12 |  |
| `gen-55799d5b5d522a4e` | done | ❌ | ❌ | 12 | 20 | missing evidence: [['patterns', 'design']] |
| `gen-17497531a153bb9c` | done | ✅ | ✅ | 8 | 13 |  |
| `gen-449f2b1ab76c8701` | done | ❌ | ❌ | 6 | 24 | missing evidence: [['profiling']] |
| `gen-bc21f16f8df123d6` | done | ❌ | ❌ | 13 | 25 | missing evidence: [['next.js']] |
| `gen-7c53df2b31c02f7a` | done | ❌ | ❌ | 9 | 15 | url lacks 'q=review' |
| `gen-541a9fdff6e5bb25` | done | ❌ | ❌ | 25 | 36 | url lacks 'q=c++' |
| `gen-f6ebbc1ed94f0a8f` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 47 (57%)
- `done-rejected`: 10 (12%)
- `stale`: 9 (11%)
- `done`: 8 (10%)
- `page changed since the decision (url or marker mismatch)`: 7 (8%)
- `refused-empty-enter`: 2 (2%)

low-confidence decisions (< τ): 13
