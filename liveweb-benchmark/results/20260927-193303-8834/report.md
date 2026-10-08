# liveweb-benchmark report

- generated: `2026-09-27T19:39:37+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 4.2, mean duration 20.0s, decision p50/p95 517.7/631.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 4.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-689cee7ad5576a96` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-39a436d7a90b2cb0` | done | ❌ | ❌ | 7 | 19 | url lacks 'q=generation' |
| `gen-b305b55787053d69` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-6940db71dd16e024` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-25dd7644da26d4bc` | done | ✅ | ✅ | 3 | 17 |  |
| `gen-2ba4a69b1eed169c` | bot-challenge | ❌ | ❌ | 7 | 59 | url lacks 'google.com/search' |
| `gen-8debb0b5bde27fe2` | done | ✅ | ✅ | 4 | 9 |  |
| `gen-a04682fb3f31a155` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 18 (53%)
- `done-rejected`: 7 (21%)
- `done`: 4 (12%)
- `stale`: 2 (6%)
- `refused-empty-enter`: 2 (6%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 3
