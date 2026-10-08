# liveweb-benchmark report

- generated: `2026-09-27T17:44:07+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 7.6, mean duration 16.6s, decision p50/p95 564.5/821.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 100% | 100% | 12.0 |
| google | 7 | 57% | 57% | 7.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-338ad99f553fe76a` | done | ❌ | ❌ | 13 | 17 | url lacks 'q=c++' |
| `gen-68265638891c503b` | done | ❌ | ❌ | 10 | 57 | missing evidence: [['quantization', 'model']] |
| `gen-eb59522557d61659` | done | ❌ | ❌ | 4 | 9 | url lacks 'q=kubernetes' |
| `gen-c483d8cba345d04b` | done | ✅ | ✅ | 11 | 14 |  |
| `gen-e755761c27824672` | done | ✅ | ✅ | 12 | 18 |  |
| `gen-e8d568c5ce5b721e` | done | ✅ | ✅ | 3 | 6 |  |
| `gen-80ed89e888510725` | done | ✅ | ✅ | 5 | 9 |  |
| `gen-010e5ce84c066be1` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 34 (56%)
- `done`: 8 (13%)
- `done-rejected`: 7 (11%)
- `stale`: 6 (10%)
- `refused-empty-enter`: 4 (7%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)

low-confidence decisions (< τ): 5
