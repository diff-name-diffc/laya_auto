# liveweb-benchmark report

- generated: `2026-09-27T21:46:50+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 2.0, mean duration 16.0s, decision p50/p95 552.4/703.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 2.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-ce202ef00a048684` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-56dcb6f82fad5ada` | bot-challenge | ❌ | ❌ | 3 | 33 | bot_challenge |
| `gen-e3e9b9d6ce6e1ac0` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-52ed1276b0b65e0c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-3c6e1472ecd1ffd3` | bot-challenge | ❌ | ❌ | 3 | 20 | bot_challenge |
| `gen-6367c56eaa59796b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-fba84d0a2e4b7a6a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f398fc80b3121732` | incomplete | ❌ | ❌ | 0 | 0 | harness error |

## Step outcomes

- `executed`: 14 (88%)
- `done-rejected`: 2 (12%)

low-confidence decisions (< τ): 1
