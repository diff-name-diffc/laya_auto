# liveweb-benchmark report

- generated: `2026-09-27T21:55:31+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 3.9, mean duration 18.0s, decision p50/p95 482.7/654.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 12.0 |
| google | 7 | 0% | 0% | 2.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-30857e051c8a15c7` | bot-challenge | ❌ | ❌ | 6 | 29 | bot_challenge |
| `gen-6bcaa9ad8d001df9` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-4ac33b9bce327cab` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e2d21344a18e936f` | done | ❌ | ❌ | 12 | 23 | missing evidence: [['postgresql']] |
| `gen-c64d2ace10c29907` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-b260d8befb8a5db1` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e9e5495465ba7d7b` | bot-challenge | ❌ | ❌ | 3 | 18 | bot_challenge |
| `gen-3f713d6719a984ea` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 19 (61%)
- `done-rejected`: 5 (16%)
- `refused-empty-enter`: 3 (10%)
- `stale`: 2 (6%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)
- `done`: 1 (3%)

low-confidence decisions (< τ): 0
