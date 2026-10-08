# liveweb-benchmark report

- generated: `2026-09-27T02:59:09+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=4.0s

## Summary

- success **2/4** (50%) — DONE **and** independently verified
- independently verified **2/4** (50%)
- found-but-never-stopped: **0**
- mean steps 3.8, mean duration 4.7s, decision p50/p95 552.4/619.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 4 | 50% | 50% | 3.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-anthropic` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-deepmind` | bot-challenge | ❌ | ❌ | 2 | 3 | bot_challenge |
| `google-ai-llm` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-zh` | repeat-loop | ❌ | ❌ | 7 | 8 | url lacks 'google.com/search' |

## Step outcomes

- `executed`: 10 (67%)
- `stale`: 3 (20%)
- `done`: 2 (13%)

low-confidence decisions (< τ): 0
