# liveweb-benchmark report

- generated: `2026-09-27T21:58:53+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=4.0s

## Summary

- success **2/6** (33%) — DONE **and** independently verified
- independently verified **2/6** (33%)
- found-but-never-stopped: **0**
- mean steps 3.5, mean duration 5.1s, decision p50/p95 276.2/396.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 3 | 0% | 0% | 4.0 |
| google | 3 | 67% | 67% | 3.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | done | ✅ | ✅ | 3 | 15 |  |
| `google-ai-papers` | done | ✅ | ✅ | 3 | 2 |  |
| `google-news-tab` | done | ❌ | ❌ | 3 | 2 | url lacks 'tbm=nws' |
| `github-trending-first-repo` | repeat-loop | ❌ | ❌ | 3 | 4 | missing evidence: [['fork', 'forks']] |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 3 | 3 | url lacks 'github.com/trending/python' |
| `github-search-first` | done | ❌ | ❌ | 6 | 5 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 17 (81%)
- `done`: 4 (19%)

low-confidence decisions (< τ): 2
