# liveweb-benchmark report

- generated: `2026-09-27T03:28:14+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **8/20** (40%) — DONE **and** independently verified
- independently verified **9/20** (45%)
- found-but-never-stopped: **1**
- mean steps 4.4, mean duration 5.4s, decision p50/p95 581.6/626.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 8 | 38% | 38% | 3.2 |
| google | 12 | 42% | 50% | 5.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | done | ❌ | ❌ | 2 | 2 | missing evidence: [['openai']] |
| `google-ai-anthropic` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-deepmind` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-llm` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-agents` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-papers` | done | ❌ | ❌ | 5 | 5 | missing evidence: [['arxiv', 'paper']] |
| `google-ai-zh` | max-steps | ✅ | ❌ | 25 | 33 |  |
| `google-ai-opensource` | done | ✅ | ✅ | 3 | 3 |  |
| `github-trending-view` | done | ✅ | ✅ | 2 | 3 |  |
| `github-trending-ai-repo` | done | ❌ | ❌ | 2 | 2 | missing evidence: [['fork', 'forks']] |
| `github-search-llm` | done | ❌ | ❌ | 9 | 18 | missing evidence: [['llm']] |
| `github-trending-first-repo` | repeat-loop | ❌ | ❌ | 3 | 4 | missing evidence: [['fork', 'forks']] |
| `google-news-tab` | repeat-loop | ❌ | ❌ | 4 | 4 | missing evidence: [['openai']] |
| `google-images-tab` | done | ❌ | ❌ | 3 | 3 | url lacks 'tbm=isch' |
| `google-page2` | repeat-loop | ❌ | ❌ | 5 | 4 | url lacks 'start=10' |
| `google-wikipedia` | done | ❌ | ❌ | 3 | 3 | url lacks 'wikipedia.org' |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 3 | 5 | url lacks 'github.com/trending/python' |
| `github-topic-llm` | done | ✅ | ✅ | 2 | 2 |  |
| `github-open-pytorch` | done | ✅ | ✅ | 2 | 2 |  |
| `github-search-first` | done | ❌ | ❌ | 3 | 2 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 68 (77%)
- `done`: 15 (17%)
- `stale`: 3 (3%)
- `failed`: 2 (2%)

low-confidence decisions (< τ): 13
