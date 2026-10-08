# liveweb-benchmark report

- generated: `2026-09-27T19:48:56+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 6.1, mean duration 18.8s, decision p50/p95 414.1/598.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 6.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-d8c9e781342b5533` | max-steps | ❌ | ❌ | 25 | 20 | missing evidence: [['logging']] |
| `gen-e2453e2a56b54a79` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-4ec7a2bcdba12523` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |
| `gen-057be2abc1420aca` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-1640b0231bf0bd6f` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-5c38948420a475b0` | bot-challenge | ❌ | ❌ | 3 | 20 | bot_challenge |
| `gen-35a06dc0e226d1ad` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-60058cf3f39d3044` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 30 (61%)
- `stale`: 10 (20%)
- `done-rejected`: 6 (12%)
- `refused-empty-enter`: 3 (6%)

low-confidence decisions (< τ): 2
