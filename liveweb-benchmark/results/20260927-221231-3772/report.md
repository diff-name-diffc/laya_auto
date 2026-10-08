# liveweb-benchmark report

- generated: `2026-09-27T22:21:17+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 4.8, mean duration 19.4s, decision p50/p95 561.2/628.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 12% | 4.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-a9482154d606036b` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-af05850450e38873` | bot-challenge | ❌ | ❌ | 5 | 18 | bot_challenge |
| `gen-ccc46e67e7cdf582` | bot-challenge | ❌ | ❌ | 6 | 37 | bot_challenge |
| `gen-87275247f10383f5` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-374f7856a958e3b8` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-851ae04b90f1e399` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-87e5678e6c43243a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a02155ee8f1a9a71` | done | ✅ | ✅ | 13 | 20 |  |

## Step outcomes

- `executed`: 28 (74%)
- `stale`: 5 (13%)
- `refused-empty-enter`: 2 (5%)
- `done-rejected`: 2 (5%)
- `done`: 1 (3%)

low-confidence decisions (< τ): 2
