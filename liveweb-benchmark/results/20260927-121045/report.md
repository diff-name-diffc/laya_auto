# liveweb-benchmark report

- generated: `2026-09-27T12:19:10+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **6/20** (30%) — DONE **and** independently verified
- independently verified **7/20** (35%)
- found-but-never-stopped: **1**
- mean steps 4.6, mean duration 15.9s, decision p50/p95 470.0/645.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 8 | 75% | 88% | 7.8 |
| google | 12 | 0% | 0% | 2.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-ai-anthropic` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-ai-deepmind` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-ai-llm` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-ai-agents` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-ai-papers` | bot-challenge | ❌ | ❌ | 6 | 26 | bot_challenge |
| `google-ai-zh` | bot-challenge | ❌ | ❌ | 4 | 18 | bot_challenge |
| `google-ai-opensource` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `github-trending-view` | done | ✅ | ✅ | 2 | 4 |  |
| `github-trending-ai-repo` | blocked | ✅ | ❌ | 6 | 9 |  |
| `github-search-llm` | repeat-loop | ❌ | ❌ | 7 | 16 | missing evidence: [['llm']] |
| `github-trending-first-repo` | done | ✅ | ✅ | 7 | 38 |  |
| `google-news-tab` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-images-tab` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-page2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `google-wikipedia` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `github-trending-python` | done | ✅ | ✅ | 21 | 32 |  |
| `github-topic-llm` | done | ✅ | ✅ | 2 | 4 |  |
| `github-open-pytorch` | done | ✅ | ✅ | 2 | 3 |  |
| `github-search-first` | done | ✅ | ✅ | 15 | 21 |  |

## Step outcomes

- `executed`: 68 (74%)
- `refused-empty-enter`: 8 (9%)
- `done-rejected`: 7 (8%)
- `done`: 6 (7%)
- `stale`: 1 (1%)
- `no-text-model`: 1 (1%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 2
