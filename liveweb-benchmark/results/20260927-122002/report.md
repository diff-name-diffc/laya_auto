# liveweb-benchmark report

- generated: `2026-09-27T12:30:58+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **12/20** (60%) — DONE **and** independently verified
- independently verified **12/20** (60%)
- found-but-never-stopped: **0**
- mean steps 6.7, mean duration 21.1s, decision p50/p95 497.5/670.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 8 | 75% | 75% | 8.8 |
| google | 12 | 50% | 50% | 5.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | bot-challenge | ❌ | ❌ | 5 | 20 | bot_challenge |
| `google-ai-anthropic` | done | ✅ | ✅ | 7 | 11 |  |
| `google-ai-deepmind` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-llm` | done | ✅ | ✅ | 3 | 5 |  |
| `google-ai-agents` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-papers` | done | ✅ | ✅ | 5 | 9 |  |
| `google-ai-zh` | done | ✅ | ✅ | 6 | 11 |  |
| `google-ai-opensource` | done | ❌ | ❌ | 6 | 15 | missing evidence: [['open source', '开源']] |
| `github-trending-view` | done | ✅ | ✅ | 2 | 4 |  |
| `github-trending-ai-repo` | done | ✅ | ✅ | 7 | 15 |  |
| `github-search-llm` | repeat-loop | ❌ | ❌ | 7 | 25 | missing evidence: [['llm']] |
| `github-trending-first-repo` | done | ✅ | ✅ | 7 | 57 |  |
| `google-news-tab` | repeat-loop | ❌ | ❌ | 11 | 38 | missing evidence: [['openai']] |
| `google-images-tab` | done | ❌ | ❌ | 5 | 47 | url lacks 'tbm=isch' |
| `google-page2` | repeat-loop | ❌ | ❌ | 5 | 25 | url lacks 'start=10' |
| `google-wikipedia` | done | ❌ | ❌ | 5 | 46 | url lacks 'wikipedia.org' |
| `github-trending-python` | done | ✅ | ✅ | 21 | 42 |  |
| `github-topic-llm` | done | ✅ | ✅ | 2 | 7 |  |
| `github-open-pytorch` | done | ❌ | ❌ | 9 | 15 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |
| `github-search-first` | done | ✅ | ✅ | 15 | 23 |  |

## Step outcomes

- `executed`: 78 (58%)
- `done-rejected`: 20 (15%)
- `done`: 16 (12%)
- `refused-empty-enter`: 12 (9%)
- `stale`: 4 (3%)
- `page changed since the decision (url or marker mismatch)`: 4 (3%)

low-confidence decisions (< τ): 9
