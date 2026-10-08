# liveweb-benchmark report

- generated: `2026-09-27T19:40:46+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 4.6, mean duration 19.2s, decision p50/p95 496.8/633.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 4.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-1db60cec8e62c48b` | bot-challenge | ❌ | ❌ | 10 | 26 | bot_challenge |
| `gen-cb6ac02b149ee41e` | bot-challenge | ❌ | ❌ | 6 | 18 | bot_challenge |
| `gen-7f4abb4539f73dca` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-5cf921f617fa4e0e` | done | ❌ | ❌ | 7 | 27 | missing evidence: [['express']] |
| `gen-5f1f03ed29ad6d6c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e28fa95767962d24` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-50d0c18802f7e48f` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-22ea52d1815babde` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |

## Step outcomes

- `executed`: 24 (65%)
- `done-rejected`: 5 (14%)
- `refused-empty-enter`: 4 (11%)
- `stale`: 2 (5%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)
- `done`: 1 (3%)

low-confidence decisions (< τ): 4
