# liveweb-benchmark report

- generated: `2026-09-27T20:24:57+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 4.0, mean duration 16.1s, decision p50/p95 479.0/599.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 100% | 100% | 8.0 |
| google | 7 | 0% | 0% | 3.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-1793c5a15b0f3b7d` | bot-challenge | ❌ | ❌ | 5 | 18 | bot_challenge |
| `gen-a32bb86c022a8467` | done | ❌ | ❌ | 8 | 19 | missing evidence: [['express']] |
| `gen-936bffcbf38ffd18` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-7bdec8ce11a7d427` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a84d8117c2a41f7f` | done | ✅ | ✅ | 8 | 14 |  |
| `gen-ce242cd16ca14547` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |
| `gen-5e2bc04722c65df6` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-ab16cf9d47469063` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 21 (66%)
- `done-rejected`: 5 (16%)
- `stale`: 2 (6%)
- `refused-empty-enter`: 2 (6%)
- `done`: 2 (6%)

low-confidence decisions (< τ): 1
