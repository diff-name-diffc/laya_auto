# liveweb-benchmark report

- generated: `2026-09-27T19:17:50+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 4.6, mean duration 18.0s, decision p50/p95 577.2/628.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 4.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-d9b31e7df372ed82` | bot-challenge | ❌ | ❌ | 6 | 28 | bot_challenge |
| `gen-37e7b83364b41d7f` | done | ✅ | ✅ | 8 | 25 |  |
| `gen-f55d6f6fdd1ea5c5` | done | ✅ | ✅ | 10 | 16 |  |
| `gen-165bcf97966c297f` | done | ✅ | ✅ | 5 | 17 |  |
| `gen-0abac9e03d71065e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-fca15324650983dd` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-37dbd25d83c43e14` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-47963c579f4ac5b4` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 23 (62%)
- `done-rejected`: 5 (14%)
- `stale`: 4 (11%)
- `done`: 3 (8%)
- `refused-empty-enter`: 2 (5%)

low-confidence decisions (< τ): 3
