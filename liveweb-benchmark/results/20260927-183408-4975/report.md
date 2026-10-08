# liveweb-benchmark report

- generated: `2026-09-27T18:38:59+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 9.2, mean duration 23.7s, decision p50/p95 523.3/664.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 50% | 50% | 12.5 |
| google | 6 | 50% | 50% | 8.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-90cf87655defb685` | done | ❌ | ❌ | 11 | 18 | missing evidence: [['angular']] |
| `gen-3c205246201d2abc` | bot-challenge | ❌ | ❌ | 5 | 24 | bot_challenge |
| `gen-7b119ab071cb9435` | repeat-loop | ❌ | ❌ | 10 | 53 | missing evidence: [['rabbitmq']] |
| `gen-30790d0c743b6110` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-75cbedd385cfadda` | done | ✅ | ✅ | 14 | 19 |  |
| `gen-c9255f1bdf0b47c9` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-610ce139f12426ad` | repeat-loop | ❌ | ❌ | 25 | 62 | missing evidence: [['elasticsearch']] |
| `gen-0da8f98cbb905d71` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 55 (74%)
- `stale`: 7 (9%)
- `done`: 5 (7%)
- `done-rejected`: 4 (5%)
- `refused-empty-enter`: 2 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 1
