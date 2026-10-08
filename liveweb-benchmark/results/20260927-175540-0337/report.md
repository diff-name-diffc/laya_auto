# liveweb-benchmark report

- generated: `2026-09-27T17:59:16+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 7.6, mean duration 14.5s, decision p50/p95 522.9/782.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 7.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-6b8aa406b8449cc7` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-8a1fd723a75f719d` | done | ❌ | ❌ | 20 | 31 | missing evidence: [['fastapi']] |
| `gen-6cfe3d4318b0e2f2` | done | ❌ | ❌ | 14 | 28 | missing evidence: [['react']] |
| `gen-69e1096d911dbf19` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-53bb80e0126bd4c0` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-7d56e41316f9e3b3` | done | ❌ | ❌ | 3 | 4 | url lacks 'q=quantization' |
| `gen-b8dd55b59f1dda70` | done | ❌ | ❌ | 9 | 18 | missing evidence: [['elasticsearch']] |
| `gen-fa1f46fd1fc88bda` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 30 (49%)
- `stale`: 9 (15%)
- `done-rejected`: 8 (13%)
- `done`: 7 (11%)
- `page changed since the decision (url or marker mismatch)`: 5 (8%)
- `refused-empty-enter`: 2 (3%)

low-confidence decisions (< τ): 3
