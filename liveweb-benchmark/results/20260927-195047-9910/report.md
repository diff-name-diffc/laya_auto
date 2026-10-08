# liveweb-benchmark report

- generated: `2026-09-27T19:59:50+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 4.9, mean duration 27.2s, decision p50/p95 511.7/632.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 15.0 |
| google | 7 | 0% | 0% | 3.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-54f935439e39af32` | bot-challenge | ❌ | ❌ | 5 | 18 | bot_challenge |
| `gen-860a882ff42f991f` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-6d28be153a7eb9e8` | done | ❌ | ❌ | 15 | 90 | url lacks 'github.com/search' |
| `gen-5d4dd5517f6acc90` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-6e2f3659fcaa1b62` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-93c842ef38fe703c` | bot-challenge | ❌ | ❌ | 3 | 22 | bot_challenge |
| `gen-eef02e404f967f36` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-1a433ddac6fe5a1e` | bot-challenge | ❌ | ❌ | 4 | 23 | bot_challenge |

## Step outcomes

- `executed`: 27 (69%)
- `done-rejected`: 6 (15%)
- `refused-empty-enter`: 3 (8%)
- `stale`: 2 (5%)
- `done`: 1 (3%)

low-confidence decisions (< τ): 1
