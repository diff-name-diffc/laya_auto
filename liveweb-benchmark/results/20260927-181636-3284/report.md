# liveweb-benchmark report

- generated: `2026-09-27T18:21:34+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 4.2, mean duration 13.5s, decision p50/p95 500.2/641.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 50% | 50% | 4.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-1b8155274d50b20a` | bot-challenge | ❌ | ❌ | 5 | 19 | bot_challenge |
| `gen-c55dfedf6887ed40` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-8962f4d251ea3599` | done | ✅ | ✅ | 3 | 6 |  |
| `gen-9f7c8662ea3417fc` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-3a836bd3df99af1a` | done | ✅ | ✅ | 5 | 10 |  |
| `gen-ceb8f6c0d4b3f617` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-c1380d84f62c939e` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |
| `gen-74a858c313c8570a` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |

## Step outcomes

- `executed`: 18 (53%)
- `done-rejected`: 7 (21%)
- `done`: 4 (12%)
- `refused-empty-enter`: 3 (9%)
- `stale`: 2 (6%)

low-confidence decisions (< τ): 3
