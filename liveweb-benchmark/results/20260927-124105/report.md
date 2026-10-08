# liveweb-benchmark report

- generated: `2026-09-27T12:45:00+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/4** (0%) — DONE **and** independently verified
- independently verified **0/4** (0%)
- found-but-never-stopped: **0**
- mean steps 15.0, mean duration 40.4s, decision p50/p95 468.3/633.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 10.0 |
| google | 2 | 0% | 0% | 20.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-images-tab` | bot-challenge | ❌ | ❌ | 14 | 41 | bot_challenge |
| `github-search-llm` | done | ❌ | ❌ | 11 | 71 | missing evidence: [['llm']] |
| `github-open-pytorch` | done | ❌ | ❌ | 9 | 20 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |
| `google-news-tab` | max-steps | ❌ | ❌ | 26 | 29 | missing evidence: [['openai']] |

## Step outcomes

- `executed`: 36 (60%)
- `stale`: 8 (13%)
- `refused-empty-enter`: 6 (10%)
- `done-rejected`: 5 (8%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)
- `done`: 2 (3%)
- `failed`: 1 (2%)

low-confidence decisions (< τ): 2
