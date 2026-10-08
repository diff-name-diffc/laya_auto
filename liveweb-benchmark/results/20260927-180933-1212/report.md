# liveweb-benchmark report

- generated: `2026-09-27T18:14:59+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 7.2, mean duration 17.0s, decision p50/p95 492.4/777.8 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 7.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-42e4421e6145c76c` | bot-challenge | ❌ | ❌ | 5 | 18 | bot_challenge |
| `gen-5fe8d7bea9e019d4` | max-steps | ❌ | ❌ | 27 | 32 | missing evidence: [['programming', 'async']] |
| `gen-e070196ea5954339` | done | ✅ | ✅ | 7 | 17 |  |
| `gen-2f43c0f3ae329a76` | done | ✅ | ✅ | 6 | 13 |  |
| `gen-643099c57d7cd331` | done | ❌ | ❌ | 7 | 12 | url lacks 'q=langchain' |
| `gen-18d7ed094f30045a` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-796dfe9231e363a2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-590974a6e58ae27f` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 38 (66%)
- `stale`: 8 (14%)
- `done-rejected`: 5 (9%)
- `refused-empty-enter`: 3 (5%)
- `done`: 3 (5%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 3
