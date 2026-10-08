# liveweb-benchmark report

- generated: `2026-09-27T20:54:23+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 5.1, mean duration 24.6s, decision p50/p95 529.7/635.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 15.0 |
| google | 7 | 0% | 0% | 3.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-7aed4fc2ba363b9e` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-3109b9882d9c15cd` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-df756bb2748f8e5a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-0e2ef4147783e4f6` | bot-challenge | ❌ | ❌ | 10 | 25 | bot_challenge |
| `gen-580e2d244378868f` | done | ❌ | ❌ | 15 | 74 | url lacks 'github.com/search' |
| `gen-cd746c52c47b1a14` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-fec190da0906ce8e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d0a793bc7c39b5c0` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 31 (76%)
- `done-rejected`: 5 (12%)
- `refused-empty-enter`: 3 (7%)
- `stale`: 1 (2%)
- `done`: 1 (2%)

low-confidence decisions (< τ): 2
