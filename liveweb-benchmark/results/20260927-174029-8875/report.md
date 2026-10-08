# liveweb-benchmark report

- generated: `2026-09-27T17:43:51+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 10.2, mean duration 18.3s, decision p50/p95 576.6/891.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 100% | 100% | 8.0 |
| google | 7 | 43% | 43% | 10.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-b882ce5cc7b4b2f8` | done | ✅ | ✅ | 3 | 6 |  |
| `gen-da9a7877585ee771` | done | ✅ | ✅ | 14 | 21 |  |
| `gen-a8bee57bf8528e36` | done | ❌ | ❌ | 10 | 17 | url lacks 'q=review' |
| `gen-3a976fbbfd3bae26` | done | ✅ | ✅ | 8 | 14 |  |
| `gen-7d690f84a0e93177` | done | ❌ | ❌ | 13 | 20 | missing evidence: [['golang']] |
| `gen-e86c49d39ba67686` | done | ❌ | ❌ | 4 | 10 | url lacks 'q=next.js' |
| `gen-cad70c09d8789b26` | done | ✅ | ✅ | 12 | 26 |  |
| `gen-f715cc00c286812c` | done | ❌ | ❌ | 18 | 32 | url lacks 'q=programming' |

## Step outcomes

- `executed`: 50 (61%)
- `done-rejected`: 11 (13%)
- `done`: 8 (10%)
- `page changed since the decision (url or marker mismatch)`: 7 (9%)
- `stale`: 4 (5%)
- `refused-empty-enter`: 2 (2%)

low-confidence decisions (< τ): 9
