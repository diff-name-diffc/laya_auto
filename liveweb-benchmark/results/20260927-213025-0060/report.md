# liveweb-benchmark report

- generated: `2026-09-27T21:37:49+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 6.2, mean duration 20.4s, decision p50/p95 466.4/626.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 12% | 6.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-eedefad68b612961` | max-steps | ❌ | ❌ | 28 | 47 | url lacks 'q=testing' |
| `gen-4e2ce4df8db956c8` | done | ✅ | ✅ | 10 | 27 |  |
| `gen-916e881e7a2c9c0d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-9813e90ae88a6b81` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-0341c2c953d830ab` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-9018022b4061d29c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-406bb5aab2ecea72` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-fe8042a328876924` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 39 (78%)
- `stale`: 3 (6%)
- `done-rejected`: 3 (6%)
- `page changed since the decision (url or marker mismatch)`: 3 (6%)
- `refused-empty-enter`: 1 (2%)
- `done`: 1 (2%)

low-confidence decisions (< τ): 0
