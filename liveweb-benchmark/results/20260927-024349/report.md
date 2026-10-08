# liveweb-benchmark report

- generated: `2026-09-27T02:46:11+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=True)
- max_steps=25, delay=8.0s

## Summary

- success **1/12** (8%) — DONE **and** independently verified
- independently verified **1/12** (8%)
- found-but-never-stopped: **0**
- mean steps 1.0, mean duration 0.5s, decision p50/p95 473.9/529.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 4 | 25% | 25% | 1.0 |
| google | 8 | 0% | 0% | 1.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | done | ❌ | ❌ | 1 | 0 | missing evidence: [['openai']] |
| `google-ai-anthropic` | done | ❌ | ❌ | 1 | 0 | missing evidence: [['anthropic', 'claude']] |
| `google-ai-deepmind` | done | ❌ | ❌ | 1 | 0 | missing evidence: [['deepmind']] |
| `google-ai-llm` | done | ❌ | ❌ | 1 | 0 | missing evidence: [['language model', 'llm']] |
| `google-ai-agents` | done | ❌ | ❌ | 1 | 0 | missing evidence: [['agent']] |
| `google-ai-papers` | done | ❌ | ❌ | 1 | 0 | missing evidence: [['arxiv', 'paper']] |
| `google-ai-zh` | done | ❌ | ❌ | 1 | 0 | missing evidence: [['大模型', 'llm']] |
| `google-ai-opensource` | done | ❌ | ❌ | 1 | 0 | missing evidence: [['open source', '开源']] |
| `github-trending-view` | done | ✅ | ✅ | 1 | 1 |  |
| `github-trending-ai-repo` | done | ❌ | ❌ | 1 | 1 | missing evidence: [['fork', 'forks']] |
| `github-search-llm` | done | ❌ | ❌ | 1 | 1 | missing evidence: [['llm']] |
| `github-trending-first-repo` | done | ❌ | ❌ | 1 | 1 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `done`: 12 (100%)

low-confidence decisions (< τ): 8
