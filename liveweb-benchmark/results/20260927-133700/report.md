# liveweb-benchmark report

- generated: `2026-09-27T13:42:06+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 9.9, mean duration 25.6s, decision p50/p95 524.2/667.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 100% | 100% | 18.0 |
| google | 7 | 57% | 57% | 8.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `google-it-asyncio` | done | ✅ | ✅ | 7 | 13 |  |
| `google-it-rust-go` | done | ✅ | ✅ | 7 | 10 |  |
| `google-it-k8s` | done | ✅ | ✅ | 3 | 4 |  |
| `google-it-pydantic` | done | ✅ | ✅ | 3 | 4 |  |
| `google-it-stackoverflow` | done | ❌ | ❌ | 24 | 29 | missing evidence: [['memory leak']] |
| `google-it-mdn` | done | ❌ | ❌ | 7 | 98 | url lacks 'developer.mozilla.org' |
| `google-it-fastapi-docs` | bot-challenge | ❌ | ❌ | 10 | 26 | url lacks 'fastapi.tiangolo.com' |
| `github-it-http-server` | done | ✅ | ✅ | 18 | 19 |  |

## Step outcomes

- `executed`: 50 (63%)
- `done-rejected`: 9 (11%)
- `stale`: 8 (10%)
- `done`: 7 (9%)
- `refused-empty-enter`: 4 (5%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 8
