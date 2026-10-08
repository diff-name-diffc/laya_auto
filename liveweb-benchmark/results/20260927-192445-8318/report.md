# liveweb-benchmark report

- generated: `2026-09-27T19:32:33+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 4.6, mean duration 17.9s, decision p50/p95 563.5/767.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 4.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-fcb05abefb49a758` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-f88de05a32881c12` | done | ❌ | ❌ | 14 | 21 | url lacks 'q=generation' |
| `gen-207e6cd5859c41af` | bot-challenge | ❌ | ❌ | 7 | 25 | bot_challenge |
| `gen-ca6faf27feaa909a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f8e7c4206767be2d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d1415de4d6d2cc7e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-8c3e8ec5bc033841` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-684aae578524c0dd` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 24 (65%)
- `stale`: 5 (14%)
- `done-rejected`: 4 (11%)
- `refused-empty-enter`: 2 (5%)
- `done`: 1 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 6
