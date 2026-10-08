# liveweb-benchmark report

- generated: `2026-09-27T11:58:11+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **10/20** (50%) — DONE **and** independently verified
- independently verified **10/20** (50%)
- found-but-never-stopped: **0**
- mean steps 4.3, mean duration 6.4s, decision p50/p95 524.1/664.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 8 | 38% | 38% | 4.8 |
| google | 12 | 58% | 58% | 4.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | done | ✅ | ✅ | 3 | 6 |  |
| `google-ai-anthropic` | done | ✅ | ✅ | 3 | 14 |  |
| `google-ai-deepmind` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-llm` | done | ✅ | ✅ | 3 | 6 |  |
| `google-ai-agents` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-papers` | done | ❌ | ❌ | 5 | 7 | missing evidence: [['arxiv', 'paper']] |
| `google-ai-zh` | done | ❌ | ❌ | 5 | 6 | url lacks 'google.com/search' |
| `google-ai-opensource` | done | ✅ | ✅ | 3 | 4 |  |
| `github-trending-view` | done | ✅ | ✅ | 2 | 4 |  |
| `github-trending-ai-repo` | repeat-loop | ❌ | ❌ | 3 | 4 | missing evidence: [['fork', 'forks']] |
| `github-search-llm` | repeat-loop | ❌ | ❌ | 7 | 6 | missing evidence: [['llm']] |
| `github-trending-first-repo` | done | ❌ | ❌ | 5 | 7 | missing evidence: [['fork', 'forks']] |
| `google-news-tab` | done | ❌ | ❌ | 5 | 10 | url lacks 'tbm=nws' |
| `google-images-tab` | done | ❌ | ❌ | 5 | 9 | url lacks 'tbm=isch' |
| `google-page2` | repeat-loop | ❌ | ❌ | 5 | 4 | url lacks 'start=10' |
| `google-wikipedia` | done | ✅ | ✅ | 5 | 9 |  |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 3 | 5 | url lacks 'github.com/trending/python' |
| `github-topic-llm` | done | ✅ | ✅ | 2 | 6 |  |
| `github-open-pytorch` | done | ✅ | ✅ | 2 | 4 |  |
| `github-search-first` | repeat-loop | ❌ | ❌ | 14 | 9 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 47 (55%)
- `done`: 15 (17%)
- `refused-empty-enter`: 13 (15%)
- `done-rejected`: 10 (12%)
- `stale`: 1 (1%)

low-confidence decisions (< τ): 5
