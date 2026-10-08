# liveweb-benchmark report

- generated: `2026-09-27T22:48:40+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 7.2, mean duration 32.1s, decision p50/p95 564.8/731.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 10.0 |
| google | 7 | 14% | 14% | 6.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-39350fb40053501a` | max-steps | ❌ | ❌ | 30 | 85 | missing evidence: [['generation', 'retrieval']] |
| `gen-9ee34ec20cdb81db` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-78c0ca7246d97f67` | bot-challenge | ❌ | ❌ | 3 | 18 | bot_challenge |
| `gen-b1cdcaa746361e90` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-037cf59bc2110b9e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-9fb0163dad1db017` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-3ea8675e960bc2ab` | bot-challenge | ❌ | ❌ | 6 | 57 | bot_challenge |
| `gen-ec7c1c34634768bd` | done | ❌ | ❌ | 10 | 49 | missing evidence: [['programming', 'async']] |

## Step outcomes

- `executed`: 41 (71%)
- `done-rejected`: 7 (12%)
- `stale`: 7 (12%)
- `done`: 2 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 3
