# liveweb-benchmark report

- generated: `2026-09-28T01:37:13+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **14/34** (41%) — DONE **and** independently verified
- independently verified **19/34** (56%)
- found-but-never-stopped: **5**
- mean steps 10.4, mean duration 25.5s, decision p50/p95 219.7/317.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 10 | 30% | 50% | 12.4 |
| google | 24 | 46% | 58% | 9.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `google-ai-anthropic` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-deepmind` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-llm` | done | ✅ | ✅ | 3 | 4 |  |
| `google-ai-agents` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-papers` | done | ✅ | ✅ | 3 | 3 |  |
| `google-ai-zh` | repeat-loop | ✅ | ❌ | 18 | 63 | CLICK on the same target repeats without progress; stopping |
| `google-ai-opensource` | done | ✅ | ✅ | 3 | 4 |  |
| `github-trending-view` | done | ✅ | ✅ | 2 | 4 |  |
| `github-trending-ai-repo` | blocked | ✅ | ❌ | 13 | 32 |  |
| `github-search-llm` | done | ✅ | ✅ | 6 | 6 |  |
| `github-trending-first-repo` | blocked | ✅ | ❌ | 6 | 51 |  |
| `google-news-tab` | done | ❌ | ❌ | 3 | 4 | url lacks 'tbm=nws' |
| `google-images-tab` | done | ❌ | ❌ | 16 | 19 | url lacks 'tbm=isch' |
| `google-page2` | done | ❌ | ❌ | 15 | 44 | url lacks 'start=10' |
| `google-wikipedia` | repeat-loop | ✅ | ❌ | 28 | 76 | CLICK on the same target repeats without progress; stopping |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 28 | 35 | url lacks 'github.com/trending/python' |
| `github-topic-llm` | done | ❌ | ❌ | 9 | 46 | url lacks 'github.com/topics/llm' |
| `github-open-pytorch` | blocked | ❌ | ❌ | 5 | 58 | missing evidence: [['fork', 'forks']] |
| `github-search-first` | done | ❌ | ❌ | 20 | 19 | missing evidence: [['fork', 'forks']] |
| `google-it-asyncio` | done | ✅ | ✅ | 4 | 49 |  |
| `google-it-rust-go` | done | ✅ | ✅ | 3 | 3 |  |
| `google-it-k8s` | done | ✅ | ✅ | 3 | 3 |  |
| `google-it-pydantic` | done | ✅ | ✅ | 3 | 3 |  |
| `google-it-stackoverflow` | done | ❌ | ❌ | 18 | 61 | missing evidence: [['memory leak']] |
| `google-it-mdn` | repeat-loop | ❌ | ❌ | 22 | 31 | missing evidence: [['array']] |
| `google-it-fastapi-docs` | bot-challenge | ✅ | ❌ | 8 | 65 |  |
| `github-it-http-server` | done | ✅ | ✅ | 6 | 6 |  |
| `google-multi-python-rust` | done | ❌ | ❌ | 10 | 13 | url lacks 'q=rust' |
| `google-multi-frameworks` | unstable-page | ❌ | ❌ | 7 | 6 | url lacks 'q=django' |
| `google-multi-pytorch-tensorflow` | repeat-loop | ❌ | ❌ | 18 | 56 | missing evidence: [['tensorflow']] |
| `google-multi-k8s-docker` | done | ✅ | ✅ | 10 | 10 |  |
| `google-multi-cpp-go` | repeat-loop | ❌ | ❌ | 25 | 40 | missing evidence: [['garbage', 'go ']] |
| `github-multi-search` | repeat-loop | ❌ | ❌ | 29 | 32 | missing evidence: [['rate']] |

## Step outcomes

- `executed`: 256 (72%)
- `stale`: 34 (10%)
- `done`: 21 (6%)
- `done-rejected`: 18 (5%)
- `refused-empty-enter`: 11 (3%)
- `page changed since the decision (url or marker mismatch)`: 10 (3%)
- `no-text-model`: 3 (1%)
- `target occluded`: 2 (1%)

low-confidence decisions (< τ): 33
