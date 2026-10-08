# liveweb-benchmark report

- generated: `2026-09-27T19:10:05+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 4.4, mean duration 17.6s, decision p50/p95 505.8/724.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 4.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-335cac06b1167507` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-802d0e0fd93ed9b6` | done | ✅ | ✅ | 7 | 13 |  |
| `gen-b216aac8c2f2dd14` | done | ✅ | ✅ | 4 | 25 |  |
| `gen-8e1990c84e3494ee` | done | ❌ | ❌ | 7 | 15 | missing evidence: [['fine-tuning']] |
| `gen-520670b21731e038` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-b9653211c7c6c068` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-29afb978b556f4a9` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |
| `gen-40389dae51a34ff0` | bot-challenge | ❌ | ❌ | 4 | 18 | bot_challenge |

## Step outcomes

- `executed`: 17 (49%)
- `done-rejected`: 9 (26%)
- `refused-empty-enter`: 3 (9%)
- `done`: 3 (9%)
- `stale`: 2 (6%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 2
