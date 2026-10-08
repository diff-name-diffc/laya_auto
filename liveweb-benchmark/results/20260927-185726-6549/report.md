# liveweb-benchmark report

- generated: `2026-09-27T19:02:27+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 4.2, mean duration 14.0s, decision p50/p95 512.1/734.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 4.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-91c3b56d5596b1f4` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-77114f8b33f5b595` | done | ❌ | ❌ | 10 | 28 | url lacks 'q=golang' |
| `gen-8ff9d96fd38c94ed` | done | ✅ | ✅ | 5 | 8 |  |
| `gen-395c77cb24368565` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-8bdb15efd3a32042` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-38b59f30c1c0501e` | bot-challenge | ❌ | ❌ | 3 | 15 | bot_challenge |
| `gen-da0928d928b167ee` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a9ac13efbe14c4c4` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 19 (56%)
- `done-rejected`: 5 (15%)
- `done`: 4 (12%)
- `stale`: 3 (9%)
- `refused-empty-enter`: 3 (9%)

low-confidence decisions (< τ): 2
