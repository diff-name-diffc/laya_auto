# liveweb-benchmark report

- generated: `2026-09-27T12:09:33+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **12/20** (60%) — DONE **and** independently verified
- independently verified **13/20** (65%)
- found-but-never-stopped: **1**
- mean steps 5.7, mean duration 14.1s, decision p50/p95 511.4/636.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 8 | 50% | 50% | 5.6 |
| google | 12 | 67% | 75% | 5.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | done | ✅ | ✅ | 6 | 11 |  |
| `google-ai-anthropic` | done | ✅ | ✅ | 7 | 17 |  |
| `google-ai-deepmind` | done | ✅ | ✅ | 3 | 13 |  |
| `google-ai-llm` | done | ✅ | ✅ | 6 | 12 |  |
| `google-ai-agents` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-papers` | done | ✅ | ✅ | 4 | 7 |  |
| `google-ai-zh` | repeat-loop | ✅ | ❌ | 7 | 24 | CLICK on the same target repeats without progress; stopping |
| `google-ai-opensource` | done | ✅ | ✅ | 4 | 9 |  |
| `github-trending-view` | done | ✅ | ✅ | 2 | 5 |  |
| `github-trending-ai-repo` | repeat-loop | ❌ | ❌ | 4 | 11 | missing evidence: [['fork', 'forks']] |
| `github-search-llm` | repeat-loop | ❌ | ❌ | 7 | 17 | missing evidence: [['llm']] |
| `github-trending-first-repo` | done | ✅ | ✅ | 5 | 12 |  |
| `google-news-tab` | done | ❌ | ❌ | 5 | 32 | url lacks 'tbm=nws' |
| `google-images-tab` | done | ❌ | ❌ | 5 | 29 | url lacks 'tbm=isch' |
| `google-page2` | repeat-loop | ❌ | ❌ | 13 | 25 | missing evidence: [['language model', 'llm']] |
| `google-wikipedia` | done | ✅ | ✅ | 6 | 14 |  |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 9 | 14 | url lacks 'github.com/trending/python' |
| `github-topic-llm` | done | ✅ | ✅ | 2 | 4 |  |
| `github-open-pytorch` | done | ✅ | ✅ | 2 | 3 |  |
| `github-search-first` | done | ❌ | ❌ | 14 | 19 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 68 (60%)
- `done-rejected`: 16 (14%)
- `done`: 15 (13%)
- `refused-empty-enter`: 8 (7%)
- `stale`: 5 (4%)
- `page changed since the decision (url or marker mismatch)`: 2 (2%)

low-confidence decisions (< τ): 3
