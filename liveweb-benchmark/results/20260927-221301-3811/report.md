# liveweb-benchmark report

- generated: `2026-09-27T22:16:59+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 7.5, mean duration 17.2s, decision p50/p95 582.4/671.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 62% | 62% | 7.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-88ae5ce0f62f275e` | bot-challenge | ❌ | ❌ | 4 | 22 | bot_challenge |
| `gen-d70ccbdcb5a5916c` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-380d9f7d16d75a6c` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-210635e2323db944` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-521b220002397fd5` | done | ✅ | ✅ | 13 | 24 |  |
| `gen-9504d5f0552739a7` | done | ❌ | ❌ | 22 | 45 | url lacks 'q=transformers' |
| `gen-2328638e1aa743d8` | done | ✅ | ✅ | 9 | 15 |  |
| `gen-8cd12ea281e05b4f` | bot-challenge | ❌ | ❌ | 3 | 18 | bot_challenge |

## Step outcomes

- `executed`: 38 (63%)
- `stale`: 6 (10%)
- `done-rejected`: 6 (10%)
- `done`: 6 (10%)
- `page changed since the decision (url or marker mismatch)`: 3 (5%)
- `refused-empty-enter`: 1 (2%)

low-confidence decisions (< τ): 12
