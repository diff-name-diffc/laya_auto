# liveweb-benchmark report

- generated: `2026-09-27T19:30:52+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 3.8, mean duration 14.7s, decision p50/p95 561.6/767.8 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 3.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-3d4fe6a831f078ec` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a9afbe25b3348dcc` | done | ✅ | ✅ | 9 | 25 |  |
| `gen-da1114f6593522b8` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-d80dda6a47f99a3b` | done | ✅ | ✅ | 4 | 7 |  |
| `gen-a38ad6104595d761` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-d090e61dc97a2d07` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-eb61042263c48e31` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-84def353ba7e3ac0` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 21 (70%)
- `done`: 3 (10%)
- `stale`: 2 (7%)
- `done-rejected`: 2 (7%)
- `refused-empty-enter`: 1 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 0
