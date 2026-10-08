# liveweb-benchmark report

- generated: `2026-09-27T12:37:08+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 8.2, mean duration 29.3s, decision p50/p95 598.7/655.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 11.0 |
| google | 6 | 50% | 50% | 7.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-ai-openai` | bot-challenge | ❌ | ❌ | 5 | 20 | bot_challenge |
| `google-ai-opensource` | done | ✅ | ✅ | 7 | 12 |  |
| `google-news-tab` | done | ❌ | ❌ | 5 | 48 | url lacks 'tbm=nws' |
| `google-images-tab` | done | ❌ | ❌ | 5 | 51 | url lacks 'tbm=isch' |
| `google-page2` | done | ✅ | ✅ | 17 | 20 |  |
| `google-wikipedia` | done | ✅ | ✅ | 5 | 11 |  |
| `github-search-llm` | done | ❌ | ❌ | 13 | 52 | url lacks 'github.com/search' |
| `github-open-pytorch` | done | ❌ | ❌ | 9 | 20 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |

## Step outcomes

- `executed`: 36 (55%)
- `done-rejected`: 12 (18%)
- `done`: 7 (11%)
- `refused-empty-enter`: 6 (9%)
- `stale`: 3 (5%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)

low-confidence decisions (< τ): 3
