# liveweb-benchmark report

- generated: `2026-09-27T21:48:12+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=4.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- mean steps 4.5, mean duration 3.9s, decision p50/p95 478.6/594.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 3 | 0% | 0% | 6.0 |
| google | 3 | 0% | 0% | 3.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | done | ❌ | ❌ | 2 | 2 | missing evidence: [['openai']] |
| `google-ai-papers` | done | ❌ | ❌ | 3 | 2 | missing evidence: [['arxiv', 'paper']] |
| `google-news-tab` | repeat-loop | ❌ | ❌ | 4 | 4 | missing evidence: [['openai']] |
| `github-trending-first-repo` | done | ❌ | ❌ | 2 | 3 | missing evidence: [['fork', 'forks']] |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 3 | 4 | url lacks 'github.com/trending/python' |
| `github-search-first` | done | ❌ | ❌ | 13 | 9 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 14 (52%)
- `refused-empty-enter`: 6 (22%)
- `done`: 4 (15%)
- `stale`: 3 (11%)

low-confidence decisions (< τ): 2
