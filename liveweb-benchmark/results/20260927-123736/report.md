# liveweb-benchmark report

- generated: `2026-09-27T12:40:40+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/4** (0%) — DONE **and** independently verified
- independently verified **0/4** (0%)
- found-but-never-stopped: **0**
- mean steps 10.2, mean duration 27.8s, decision p50/p95 509.7/683.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 11.0 |
| google | 2 | 0% | 0% | 9.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-news-tab` | bot-challenge | ❌ | ❌ | 4 | 16 | bot_challenge |
| `google-images-tab` | done | ❌ | ❌ | 15 | 19 | url lacks 'tbm=isch' |
| `github-search-llm` | done | ❌ | ❌ | 13 | 59 | url lacks 'github.com/search' |
| `github-open-pytorch` | done | ❌ | ❌ | 9 | 17 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |

## Step outcomes

- `executed`: 23 (56%)
- `refused-empty-enter`: 6 (15%)
- `done-rejected`: 5 (12%)
- `stale`: 3 (7%)
- `done`: 3 (7%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 3
