# liveweb-benchmark report

- generated: `2026-09-27T21:52:15+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=4.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- mean steps 3.2, mean duration 9.2s, decision p50/p95 276.2/350.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 3 | 0% | 0% | 4.0 |
| google | 3 | 0% | 0% | 2.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-ai-papers` | bot-challenge | ❌ | ❌ | 3 | 15 | bot_challenge |
| `google-news-tab` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `github-trending-first-repo` | repeat-loop | ❌ | ❌ | 3 | 4 | missing evidence: [['fork', 'forks']] |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 3 | 3 | url lacks 'github.com/trending/python' |
| `github-search-first` | done | ❌ | ❌ | 6 | 5 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 17 (89%)
- `stale`: 1 (5%)
- `done`: 1 (5%)

low-confidence decisions (< τ): 0
