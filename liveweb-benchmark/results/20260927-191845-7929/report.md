# liveweb-benchmark report

- generated: `2026-09-27T19:23:42+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 9.2, mean duration 19.1s, decision p50/p95 583.4/823.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 9.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-c84f9ca91a1a5b00` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-83c2890e035a2ae8` | done | ✅ | ✅ | 22 | 51 |  |
| `gen-f8b0eee06f77cd7e` | done | ❌ | ❌ | 15 | 28 | url lacks 'q=laravel' |
| `gen-c470a5e45ab12c0d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-56c9fe7457465edf` | done | ❌ | ❌ | 12 | 14 | url lacks 'q=c++' |
| `gen-88151a8894cdc348` | unstable-page | ❌ | ❌ | 10 | 10 | missing evidence: [['concurrency']] |
| `gen-82f0e5ea636151ce` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-3a31556543708e8a` | done | ✅ | ✅ | 4 | 8 |  |

## Step outcomes

- `executed`: 40 (54%)
- `stale`: 15 (20%)
- `refused-empty-enter`: 5 (7%)
- `done-rejected`: 5 (7%)
- `done`: 5 (7%)
- `page changed since the decision (url or marker mismatch)`: 4 (5%)

low-confidence decisions (< τ): 11
