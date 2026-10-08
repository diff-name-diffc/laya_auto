# liveweb-benchmark report

- generated: `2026-09-27T17:54:55+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 9.0, mean duration 24.0s, decision p50/p95 579.6/748.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 50% | 50% | 9.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-27cfc3885f75afba` | bot-challenge | ❌ | ❌ | 5 | 20 | bot_challenge |
| `gen-885d0932984fc063` | done | ✅ | ✅ | 8 | 13 |  |
| `gen-43a23604636c0493` | done | ❌ | ❌ | 3 | 4 | url lacks 'q=kubernetes' |
| `gen-a0d655e654c55dfa` | done | ❌ | ❌ | 13 | 90 | missing evidence: [['golang']] |
| `gen-cafed8939658267c` | done | ✅ | ✅ | 3 | 3 |  |
| `gen-e855cb0c7771993f` | done | ✅ | ✅ | 5 | 9 |  |
| `gen-b575b82f349b92e5` | done | ✅ | ✅ | 5 | 6 |  |
| `gen-2a37507525b70816` | repeat-loop | ❌ | ❌ | 30 | 46 | url lacks 'q=java' |

## Step outcomes

- `executed`: 52 (72%)
- `stale`: 6 (8%)
- `done`: 6 (8%)
- `done-rejected`: 5 (7%)
- `refused-empty-enter`: 3 (4%)

low-confidence decisions (< τ): 4
