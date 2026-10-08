# liveweb-benchmark report

- generated: `2026-09-27T18:25:29+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 6.9, mean duration 40.9s, decision p50/p95 494.6/653.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 13.5 |
| google | 6 | 33% | 33% | 4.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-da0077f4aed52fdf` | done | ❌ | ❌ | 14 | 106 | url lacks 'github.com/search' |
| `gen-e9e07e03c8be74da` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-da34794cfd756b41` | done | ✅ | ✅ | 7 | 10 |  |
| `gen-53ac6fef40d4946e` | done | ✅ | ✅ | 6 | 32 |  |
| `gen-8a9485b0254c69b7` | bot-challenge | ❌ | ❌ | 5 | 21 | bot_challenge |
| `gen-5b8d4b5c5d9a91ef` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-6b7e8af03b457609` | done | ❌ | ❌ | 13 | 106 | url lacks 'github.com/search' |
| `gen-40677e7e03800d54` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 36 (65%)
- `done-rejected`: 10 (18%)
- `done`: 4 (7%)
- `stale`: 2 (4%)
- `refused-empty-enter`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 1
