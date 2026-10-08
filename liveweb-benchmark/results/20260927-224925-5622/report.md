# liveweb-benchmark report

- generated: `2026-09-27T22:54:40+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 7.2, mean duration 26.6s, decision p50/p95 565.9/786.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 11.0 |
| google | 7 | 71% | 71% | 6.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-2396d891199c4bb4` | done | ❌ | ❌ | 6 | 34 | url lacks 'q=flask' |
| `gen-31c7aaae11d1081c` | done | ✅ | ✅ | 11 | 23 |  |
| `gen-094ac939cde4e89b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-7de5990271dad74b` | done | ✅ | ✅ | 4 | 12 |  |
| `gen-a85793d257e4c690` | done | ✅ | ✅ | 5 | 7 |  |
| `gen-09675267d27e0f31` | done | ❌ | ❌ | 11 | 76 | url lacks 'github.com/search' |
| `gen-e2eff16e878c6079` | done | ✅ | ✅ | 10 | 20 |  |
| `gen-1d2da08c53ae8d89` | done | ✅ | ✅ | 9 | 27 |  |

## Step outcomes

- `executed`: 33 (57%)
- `done-rejected`: 10 (17%)
- `done`: 7 (12%)
- `stale`: 4 (7%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)
- `refused-empty-enter`: 2 (3%)

low-confidence decisions (< τ): 7
