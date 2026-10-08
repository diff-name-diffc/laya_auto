# liveweb-benchmark report

- generated: `2026-09-27T19:09:43+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 6.6, mean duration 16.7s, decision p50/p95 534.3/664.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 16.0 |
| google | 7 | 43% | 43% | 5.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-bf7a2f94d6ab42f4` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-cc12380900316cc1` | done | ✅ | ✅ | 7 | 12 |  |
| `gen-01589b7871dcb24f` | done | ❌ | ❌ | 16 | 23 | url lacks 'github.com/search' |
| `gen-40bccac05ae3c8de` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-a00efeac1fb94b8e` | done | ✅ | ✅ | 4 | 9 |  |
| `gen-826fced32bbcee40` | bot-challenge | ❌ | ❌ | 10 | 27 | bot_challenge |
| `gen-4b11f0fc21ffe0b9` | bot-challenge | ❌ | ❌ | 4 | 16 | bot_challenge |
| `gen-2705634d6c276445` | bot-challenge | ❌ | ❌ | 3 | 20 | bot_challenge |

## Step outcomes

- `executed`: 31 (58%)
- `done-rejected`: 9 (17%)
- `refused-empty-enter`: 5 (9%)
- `done`: 4 (8%)
- `stale`: 3 (6%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 1
