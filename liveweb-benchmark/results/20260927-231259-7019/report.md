# liveweb-benchmark report

- generated: `2026-09-27T23:21:43+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 6.1, mean duration 24.9s, decision p50/p95 457.0/611.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 6.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-3f7c259630628dd7` | bot-challenge | ❌ | ❌ | 5 | 24 | bot_challenge |
| `gen-bb28be7b61f6cb22` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a70b3d004c347e09` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d14e8df5b900fa69` | bot-challenge | ❌ | ❌ | 6 | 61 | bot_challenge |
| `gen-f525a66c7946318f` | max-steps | ❌ | ❌ | 28 | 40 | url lacks 'q=how' |
| `gen-824dadb4340fbb9e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-1b849a570d416cd4` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f53dc7b1ff1d73ee` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 36 (73%)
- `stale`: 6 (12%)
- `refused-empty-enter`: 4 (8%)
- `done-rejected`: 3 (6%)

low-confidence decisions (< τ): 2
