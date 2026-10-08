# liveweb-benchmark report

- generated: `2026-09-27T03:09:41+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **3/12** (25%) — DONE **and** independently verified
- independently verified **3/12** (25%)
- found-but-never-stopped: **0**
- mean steps 3.8, mean duration 5.4s, decision p50/p95 480.4/616.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 4 | 25% | 25% | 4.0 |
| google | 8 | 25% | 25% | 3.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | done | ❌ | ❌ | 2 | 1 | missing evidence: [['openai']] |
| `google-ai-anthropic` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-deepmind` | done | ✅ | ✅ | 3 | 2 |  |
| `google-ai-llm` | no-progress | ❌ | ❌ | 5 | 19 | missing evidence: [['language model', 'llm']] |
| `google-ai-agents` | repeat-loop | ❌ | ❌ | 3 | 2 | missing evidence: [['agent']] |
| `google-ai-papers` | repeat-loop | ❌ | ❌ | 5 | 4 | missing evidence: [['arxiv', 'paper']] |
| `google-ai-zh` | done | ❌ | ❌ | 3 | 3 | missing evidence: [['大模型', 'llm']] |
| `google-ai-opensource` | no-progress | ❌ | ❌ | 5 | 5 | missing evidence: [['open source', '开源']] |
| `github-trending-view` | done | ✅ | ✅ | 2 | 3 |  |
| `github-trending-ai-repo` | done | ❌ | ❌ | 2 | 2 | missing evidence: [['fork', 'forks']] |
| `github-search-llm` | done | ❌ | ❌ | 9 | 18 | missing evidence: [['llm']] |
| `github-trending-first-repo` | done | ❌ | ❌ | 3 | 3 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 28 (62%)
- `done`: 8 (18%)
- `failed`: 5 (11%)
- `stale`: 4 (9%)

low-confidence decisions (< τ): 1
