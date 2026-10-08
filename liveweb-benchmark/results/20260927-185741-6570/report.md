# liveweb-benchmark report

- generated: `2026-09-27T19:03:34+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 4.8, mean duration 14.9s, decision p50/p95 563.6/847.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 4.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-f5d0ea252e04c174` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-25278e866b5ca427` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-4151e7847394781f` | done | ❌ | ❌ | 18 | 28 | url lacks 'q=quantization' |
| `gen-9fe240bdcdf92b0e` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-e4f2639891e36221` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a5e41302547a8350` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-062d88882f42ec3d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-59054b7ed53cb3a9` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 27 (71%)
- `done-rejected`: 4 (11%)
- `done`: 3 (8%)
- `page changed since the decision (url or marker mismatch)`: 2 (5%)
- `stale`: 1 (3%)
- `refused-empty-enter`: 1 (3%)

low-confidence decisions (< τ): 3
