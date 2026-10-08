# liveweb-benchmark report

- generated: `2026-09-27T18:33:23+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 6.1, mean duration 20.5s, decision p50/p95 573.0/874.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 13.0 |
| google | 7 | 14% | 14% | 5.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-e12b2a25d69b8039` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-2ecd2705c8e70c96` | done | ✅ | ✅ | 9 | 15 |  |
| `gen-b1655506cfcae502` | bot-challenge | ❌ | ❌ | 12 | 31 | bot_challenge |
| `gen-276cce85a7cdd54e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-bc3f28ebc34271af` | done | ❌ | ❌ | 13 | 30 | url lacks 'github.com/search' |
| `gen-f5bafeea9c652ae1` | bot-challenge | ❌ | ❌ | 3 | 20 | bot_challenge |
| `gen-883e9a27063ed32b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-62e09f560ddcf9b6` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 28 (57%)
- `done-rejected`: 7 (14%)
- `stale`: 6 (12%)
- `refused-empty-enter`: 4 (8%)
- `done`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 2 (4%)

low-confidence decisions (< τ): 7
