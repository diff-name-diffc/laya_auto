# liveweb-benchmark report

- generated: `2026-09-27T20:14:30+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 9.5, mean duration 17.4s, decision p50/p95 586.2/703.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 9.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-f6011e2a20017610` | done | ✅ | ✅ | 7 | 23 |  |
| `gen-7d6c8fc152c50893` | done | ✅ | ✅ | 15 | 21 |  |
| `gen-b5bd930a5d7d9421` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-1c933db108f29a38` | bot-challenge | ❌ | ❌ | 27 | 48 | missing evidence: [['pipelines', 'ci/cd']] |
| `gen-df135f793227c8c3` | done | ✅ | ✅ | 4 | 5 |  |
| `gen-21ef65c168ae5e01` | done | ❌ | ❌ | 6 | 8 | url lacks 'google.com/search' |
| `gen-c6c7f90b182620d8` | done | ✅ | ✅ | 7 | 13 |  |
| `gen-e523fb8de7088bc7` | done | ✅ | ✅ | 7 | 16 |  |

## Step outcomes

- `executed`: 43 (57%)
- `stale`: 12 (16%)
- `done-rejected`: 7 (9%)
- `done`: 7 (9%)
- `refused-empty-enter`: 6 (8%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 17
