# liveweb-benchmark report

- generated: `2026-09-27T19:11:01+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 5.0, mean duration 17.1s, decision p50/p95 562.1/651.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 5.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-98aa0daffa718472` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-7b94687ddd9233b9` | done | ✅ | ✅ | 8 | 16 |  |
| `gen-fcc645c7ec152856` | done | ✅ | ✅ | 3 | 6 |  |
| `gen-39eb678b1dda6e59` | bot-challenge | ❌ | ❌ | 7 | 31 | bot_challenge |
| `gen-5435e9fcd39969da` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-079268740cc5a4a2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-50221aeca1cfaadc` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-fe804f28a06c1677` | done | ✅ | ✅ | 10 | 16 |  |

## Step outcomes

- `executed`: 25 (62%)
- `done-rejected`: 6 (15%)
- `stale`: 4 (10%)
- `done`: 3 (8%)
- `refused-empty-enter`: 1 (2%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 4
