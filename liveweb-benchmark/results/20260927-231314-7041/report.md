# liveweb-benchmark report

- generated: `2026-09-27T23:22:05+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 5.6, mean duration 20.1s, decision p50/p95 590.5/668.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 5.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-cefe5ac80bbd20f1` | bot-challenge | ❌ | ❌ | 5 | 19 | bot_challenge |
| `gen-4a1684c43e601b5c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-3127af88988e05e8` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |
| `gen-528090e26cb0121c` | bot-challenge | ❌ | ❌ | 3 | 21 | bot_challenge |
| `gen-8120b92e6d110ffe` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-73527b940fe5eca6` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d62deb11add2a753` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d9b9bfd6a7ad4ce2` | max-steps | ❌ | ❌ | 26 | 43 | missing evidence: [['swift']] |

## Step outcomes

- `executed`: 28 (62%)
- `stale`: 12 (27%)
- `done-rejected`: 3 (7%)
- `refused-empty-enter`: 1 (2%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 11
