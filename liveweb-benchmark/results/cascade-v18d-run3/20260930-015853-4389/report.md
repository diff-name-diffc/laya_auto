# liveweb-benchmark report

- generated: `2026-09-30T02:20:12+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **17/34** (50%) — DONE **and** independently verified
- independently verified **18/34** (53%)
- found-but-never-stopped: **1**
- VLM rescues: **52** (~1.5/task)
- mean steps 13.2, mean duration 25.7s, decision p50/p95 208.8/262.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 10 | 40% | 40% | 19.5 |
| google | 24 | 54% | 58% | 10.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | bot-challenge | ❌ | ❌ | 7 | 19 | bot_challenge |
| `google-ai-anthropic` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-deepmind` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-llm` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-agents` | done | ✅ | ✅ | 3 | 8 |  |
| `google-ai-papers` | done | ✅ | ✅ | 10 | 8 |  |
| `google-ai-zh` | max-steps | ❌ | ❌ | 30 | 30 | missing evidence: [['大模型', 'llm']] |
| `google-ai-opensource` | done | ✅ | ✅ | 3 | 4 |  |
| `github-trending-view` | max-steps | ❌ | ❌ | 26 | 26 | missing evidence: [['trending', 'stars today', 'built by']] |
| `github-trending-ai-repo` | blocked | ❌ | ❌ | 23 | 51 | missing evidence: [['fork', 'forks']] |
| `github-search-llm` | done | ✅ | ✅ | 9 | 10 |  |
| `github-trending-first-repo` | max-steps | ❌ | ❌ | 26 | 30 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |
| `google-news-tab` | done | ✅ | ✅ | 13 | 19 |  |
| `google-images-tab` | done | ❌ | ❌ | 9 | 88 | url lacks 'tbm=isch' |
| `google-page2` | repeat-loop | ❌ | ❌ | 13 | 39 | url lacks 'start=10' |
| `google-wikipedia` | done | ✅ | ✅ | 5 | 5 |  |
| `github-trending-python` | done | ✅ | ✅ | 15 | 32 |  |
| `github-topic-llm` | max-steps | ❌ | ❌ | 26 | 22 | missing evidence: [['llm', 'large language model'], ['star', |
| `github-open-pytorch` | done | ✅ | ✅ | 2 | 3 |  |
| `github-search-first` | repeat-loop | ❌ | ❌ | 30 | 102 | missing evidence: [['fork', 'forks']] |
| `google-it-asyncio` | done | ✅ | ✅ | 3 | 3 |  |
| `google-it-rust-go` | done | ✅ | ✅ | 3 | 3 |  |
| `google-it-k8s` | done | ✅ | ✅ | 3 | 3 |  |
| `google-it-pydantic` | done | ✅ | ✅ | 3 | 3 |  |
| `google-it-stackoverflow` | no-progress | ❌ | ❌ | 28 | 35 | missing evidence: [['memory leak']] |
| `google-it-mdn` | repeat-loop | ❌ | ❌ | 19 | 37 | missing evidence: [['array']] |
| `google-it-fastapi-docs` | bot-challenge | ✅ | ❌ | 8 | 27 |  |
| `github-it-http-server` | done | ✅ | ✅ | 10 | 16 |  |
| `google-multi-python-rust` | done | ❌ | ❌ | 10 | 13 | url lacks 'q=rust' |
| `google-multi-frameworks` | done | ❌ | ❌ | 13 | 13 | url lacks 'q=django' |
| `google-multi-pytorch-tensorflow` | done | ✅ | ✅ | 14 | 52 |  |
| `google-multi-k8s-docker` | max-steps | ❌ | ❌ | 27 | 33 | missing evidence: [['docker', 'compose']] |
| `google-multi-cpp-go` | done | ❌ | ❌ | 22 | 90 | url lacks 'q=go+garbage' |
| `github-multi-search` | max-steps | ❌ | ❌ | 28 | 41 | missing evidence: [['rate']] |

## Step outcomes

- `executed`: 352 (78%)
- `stale`: 52 (12%)
- `done`: 21 (5%)
- `done-rejected`: 10 (2%)
- `page changed since the decision (url or marker mismatch)`: 7 (2%)
- `refused-empty-enter`: 6 (1%)
- `no-text-model`: 1 (0%)
- `failed`: 1 (0%)

low-confidence decisions (< τ): 5
