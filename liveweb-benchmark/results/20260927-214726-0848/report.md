# liveweb-benchmark report

- generated: `2026-09-27T21:56:22+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 4.2, mean duration 20.7s, decision p50/p95 564.4/640.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 4.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-daf3b9fccf87a327` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-01455f0621c00021` | bot-challenge | ❌ | ❌ | 5 | 18 | bot_challenge |
| `gen-edc65baf0073e2a2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-fc48410ae33a2fa5` | bot-challenge | ❌ | ❌ | 7 | 54 | bot_challenge |
| `gen-25c27eaa3ecbe6c3` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-893e2872b366227b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-8e951e24fb3ba88c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e7b11cd77293e25f` | done | ❌ | ❌ | 12 | 19 | url lacks 'q=patterns' |

## Step outcomes

- `executed`: 21 (62%)
- `stale`: 4 (12%)
- `done-rejected`: 4 (12%)
- `refused-empty-enter`: 2 (6%)
- `page changed since the decision (url or marker mismatch)`: 2 (6%)
- `done`: 1 (3%)

low-confidence decisions (< τ): 2
