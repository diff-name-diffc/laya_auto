# liveweb-benchmark report

- generated: `2026-09-27T23:02:57+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 6.0, mean duration 22.2s, decision p50/p95 439.8/622.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 6.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-97971a5c242cefed` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-31392eaf196126bf` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-423159f9a7f566d4` | done | ❌ | ❌ | 8 | 28 | missing evidence: [['next.js']] |
| `gen-c6826baf11e8768e` | bot-challenge | ❌ | ❌ | 3 | 20 | bot_challenge |
| `gen-43c94438ebe050b5` | repeat-loop | ❌ | ❌ | 23 | 47 | missing evidence: [['review', 'code']] |
| `gen-f169275a290a4ee2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e8ee906794c28bee` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-af89d2a01bb6c9ae` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 32 (67%)
- `done-rejected`: 7 (15%)
- `stale`: 5 (10%)
- `refused-empty-enter`: 2 (4%)
- `done`: 1 (2%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 1
