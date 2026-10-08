# liveweb-benchmark report

- generated: `2026-09-27T18:32:07+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 6.0, mean duration 18.5s, decision p50/p95 543.2/823.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 6.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-eccd9f362bc507a4` | bot-challenge | ❌ | ❌ | 11 | 24 | bot_challenge |
| `gen-a54bef7bf2d9a56a` | done | ❌ | ❌ | 9 | 18 | missing evidence: [['logging']] |
| `gen-8e7a7715d2b3caf6` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-fafe13eb2e4f5786` | done | ✅ | ✅ | 17 | 42 |  |
| `gen-6f4a07e2f4568d06` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-39db37521e3c9ea5` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-652c0c3c71f80295` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-cb3b3efcb4aab508` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 32 (67%)
- `stale`: 5 (10%)
- `done-rejected`: 4 (8%)
- `done`: 3 (6%)
- `refused-empty-enter`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 2 (4%)

low-confidence decisions (< τ): 1
