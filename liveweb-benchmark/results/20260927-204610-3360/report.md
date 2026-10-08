# liveweb-benchmark report

- generated: `2026-09-27T20:54:33+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 8.6, mean duration 27.9s, decision p50/p95 483.4/629.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 8.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-034ebfb1fa4f0b8b` | repeat-loop | ❌ | ❌ | 27 | 79 | missing evidence: [['express']] |
| `gen-1a9e48891f29e23a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f66d3f0b181054c7` | max-steps | ❌ | ❌ | 30 | 56 | missing evidence: [['redis']] |
| `gen-f3a7f9511dc63d14` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-b0ec1e6a13437f71` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-40ec381ebc3c7622` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-0161eb6403e8c1ad` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e547f0c637567e4a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 57 (83%)
- `stale`: 9 (13%)
- `refused-empty-enter`: 2 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 2
