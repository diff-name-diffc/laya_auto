# liveweb-benchmark report

- generated: `2026-09-27T11:45:31+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=4.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- mean steps 3.8, mean duration 3.1s, decision p50/p95 458.8/579.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 3 | 0% | 0% | 5.3 |
| google | 3 | 0% | 0% | 2.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | done | ❌ | ❌ | 2 | 1 | missing evidence: [['openai']] |
| `google-news-tab` | done | ❌ | ❌ | 3 | 2 | missing evidence: [['openai']] |
| `google-ai-papers` | done | ❌ | ❌ | 2 | 1 | missing evidence: [['arxiv', 'paper']] |
| `github-trending-first-repo` | repeat-loop | ❌ | ❌ | 4 | 3 | missing evidence: [['fork', 'forks']] |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 8 | 8 | url lacks 'github.com/trending/python' |
| `github-search-first` | no-progress | ❌ | ❌ | 4 | 4 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 20 (87%)
- `done`: 3 (13%)

low-confidence decisions (< τ): 2
