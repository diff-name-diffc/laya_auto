# liveweb-benchmark report

- generated: `2026-09-30T01:53:24+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **0** (~0.0/task)
- mean steps 5.3, mean duration 3.5s, decision p50/p95 197.1/237.8 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 3 | 0% | 0% | 4.0 |
| google | 3 | 0% | 0% | 6.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | no-progress | ❌ | ❌ | 5 | 3 | missing evidence: [['openai']] |
| `google-ai-papers` | repeat-loop | ❌ | ❌ | 12 | 5 | missing evidence: [['arxiv', 'paper']] |
| `google-news-tab` | done | ❌ | ❌ | 3 | 2 | url lacks 'tbm=nws' |
| `github-trending-first-repo` | repeat-loop | ❌ | ❌ | 3 | 4 | missing evidence: [['fork', 'forks']] |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 3 | 3 | url lacks 'github.com/trending/python' |
| `github-search-first` | repeat-loop | ❌ | ❌ | 6 | 3 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 25 (78%)
- `refused-empty-enter`: 3 (9%)
- `stale`: 3 (9%)
- `done`: 1 (3%)

low-confidence decisions (< τ): 0
