# liveweb-benchmark report

- generated: `2026-09-28T01:11:11+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **1/6** (17%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **0**
- mean steps 3.2, mean duration 4.5s, decision p50/p95 188.9/238.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 3 | 0% | 0% | 3.7 |
| google | 3 | 33% | 33% | 2.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `google-ai-papers` | done | ✅ | ✅ | 3 | 2 |  |
| `google-news-tab` | done | ❌ | ❌ | 3 | 2 | url lacks 'tbm=nws' |
| `github-trending-first-repo` | repeat-loop | ❌ | ❌ | 3 | 4 | missing evidence: [['fork', 'forks']] |
| `github-trending-python` | repeat-loop | ❌ | ❌ | 3 | 3 | url lacks 'github.com/trending/python' |
| `github-search-first` | no-progress | ❌ | ❌ | 5 | 3 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 17 (89%)
- `done`: 2 (11%)

low-confidence decisions (< τ): 1
