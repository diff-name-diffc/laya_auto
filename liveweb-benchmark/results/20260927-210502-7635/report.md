# liveweb-benchmark report

- generated: `2026-09-27T21:07:45+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 7.9, mean duration 13.6s, decision p50/p95 583.6/916.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 7.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-8bf9896ebbf1ac39` | done | ❌ | ❌ | 16 | 30 | missing evidence: [['kubernetes']] |
| `gen-e776a8a2ae291a98` | done | ✅ | ✅ | 11 | 16 |  |
| `gen-a9c7d9601f5dce02` | done | ❌ | ❌ | 8 | 18 | missing evidence: [['golang']] |
| `gen-93bf859cada7402e` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-ea9371ba23095132` | done | ✅ | ✅ | 11 | 19 |  |
| `gen-608f1eee97f7ebfe` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-1be9d5f889701dc7` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-8258ba0de7fc7587` | done | ✅ | ✅ | 8 | 12 |  |

## Step outcomes

- `executed`: 36 (57%)
- `done`: 8 (13%)
- `stale`: 6 (10%)
- `page changed since the decision (url or marker mismatch)`: 6 (10%)
- `done-rejected`: 5 (8%)
- `refused-empty-enter`: 2 (3%)

low-confidence decisions (< τ): 8
