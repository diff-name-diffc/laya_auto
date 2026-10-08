# liveweb-benchmark report

- generated: `2026-09-27T17:59:37+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 7.0, mean duration 18.9s, decision p50/p95 524.5/748.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 11.0 |
| google | 6 | 67% | 67% | 5.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-1b9887fb31dc2276` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-b1281773c8710363` | done | ❌ | ❌ | 11 | 41 | url lacks 'github.com/search' |
| `gen-57d3b574e2c1b7b8` | done | ✅ | ✅ | 4 | 13 |  |
| `gen-2b399c7d32c25394` | done | ✅ | ✅ | 12 | 26 |  |
| `gen-90df65e9dfadf468` | done | ❌ | ❌ | 10 | 22 | missing evidence: [['debugging', 'memory']] |
| `gen-e67cbfae733ff24c` | done | ✅ | ✅ | 3 | 7 |  |
| `gen-da528a2bd09aa8bc` | done | ❌ | ❌ | 11 | 23 | missing evidence: [['flask']] |
| `gen-9ac5c73700780596` | done | ✅ | ✅ | 3 | 5 |  |

## Step outcomes

- `executed`: 35 (62%)
- `done-rejected`: 7 (12%)
- `done`: 7 (12%)
- `page changed since the decision (url or marker mismatch)`: 5 (9%)
- `stale`: 2 (4%)

low-confidence decisions (< τ): 2
