# liveweb-benchmark report

- generated: `2026-09-27T02:57:44+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=True)
- max_steps=25, delay=8.0s

## Summary

- success **1/12** (8%) — DONE **and** independently verified
- independently verified **1/12** (8%)
- found-but-never-stopped: **0**
- mean steps 3.8, mean duration 5.2s, decision p50/p95 474.3/623.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 4 | 25% | 25% | 4.0 |
| google | 8 | 0% | 0% | 3.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | repeat-loop | ❌ | ❌ | 4 | 4 | missing evidence: [['openai']] |
| `google-ai-anthropic` | bot-challenge | ❌ | ❌ | 2 | 3 | bot_challenge |
| `google-ai-deepmind` | bot-challenge | ❌ | ❌ | 2 | 3 | bot_challenge |
| `google-ai-llm` | bot-challenge | ❌ | ❌ | 2 | 3 | bot_challenge |
| `google-ai-agents` | repeat-loop | ❌ | ❌ | 10 | 12 | missing evidence: [['agent']] |
| `google-ai-papers` | done | ❌ | ❌ | 3 | 4 | missing evidence: [['arxiv', 'paper']] |
| `google-ai-zh` | bot-challenge | ❌ | ❌ | 2 | 3 | bot_challenge |
| `google-ai-opensource` | repeat-loop | ❌ | ❌ | 4 | 4 | missing evidence: [['open source', '开源']] |
| `github-trending-view` | done | ✅ | ✅ | 2 | 3 |  |
| `github-trending-ai-repo` | done | ❌ | ❌ | 2 | 2 | missing evidence: [['fork', 'forks']] |
| `github-search-llm` | repeat-loop | ❌ | ❌ | 8 | 18 | missing evidence: [['llm']] |
| `github-trending-first-repo` | done | ❌ | ❌ | 4 | 5 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 33 (73%)
- `stale`: 6 (13%)
- `done`: 4 (9%)
- `failed`: 2 (4%)

low-confidence decisions (< τ): 2
