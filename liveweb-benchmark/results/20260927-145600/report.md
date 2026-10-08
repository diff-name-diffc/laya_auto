# liveweb-benchmark report

- generated: `2026-09-27T14:59:28+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/6** (50%) — DONE **and** independently verified
- independently verified **3/6** (50%)
- found-but-never-stopped: **0**
- mean steps 7.0, mean duration 20.1s, decision p50/p95 475.5/626.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 50% | 50% | 9.5 |
| google | 4 | 50% | 50% | 5.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-0854fb21fe8b1714` | bot-challenge | ❌ | ❌ | 5 | 20 | bot_challenge |
| `gen-019c4104ac06726e` | done | ✅ | ✅ | 9 | 17 |  |
| `gen-c7db7d38f9dc3378` | done | ❌ | ❌ | 10 | 57 | url lacks 'github.com/search' |
| `gen-9bf0bdeaf2a7428a` | done | ❌ | ❌ | 12 | 16 | missing evidence: [['swift']] |
| `gen-82e66ed444578f59` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-3ddcf607874be362` | done | ✅ | ✅ | 3 | 6 |  |

## Step outcomes

- `executed`: 25 (60%)
- `done-rejected`: 5 (12%)
- `done`: 5 (12%)
- `refused-empty-enter`: 4 (10%)
- `stale`: 3 (7%)

low-confidence decisions (< τ): 0
