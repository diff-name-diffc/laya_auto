# liveweb-benchmark report

- generated: `2026-09-27T18:50:07+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 6.0, mean duration 17.6s, decision p50/p95 593.6/884.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 6.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-9dda530012c9ce17` | bot-challenge | ❌ | ❌ | 7 | 21 | bot_challenge |
| `gen-1a2cbb1eebdeb7b7` | done | ✅ | ✅ | 8 | 12 |  |
| `gen-2476ac09865336ca` | done | ✅ | ✅ | 9 | 12 |  |
| `gen-6c05da664d17519c` | bot-challenge | ❌ | ❌ | 16 | 35 | bot_challenge |
| `gen-801dafaec544e962` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-13efa7db953c8401` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-769c1425662b63ce` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-ed8024948cec2b6a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 35 (73%)
- `stale`: 4 (8%)
- `done-rejected`: 4 (8%)
- `refused-empty-enter`: 2 (4%)
- `done`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 7
