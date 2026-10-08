# liveweb-benchmark report

- generated: `2026-09-27T19:36:51+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 6.5, mean duration 19.9s, decision p50/p95 576.6/778.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 6.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-d3f0c090c07fe16d` | done | ✅ | ✅ | 7 | 23 |  |
| `gen-1621c24b3bfc8c63` | done | ✅ | ✅ | 11 | 16 |  |
| `gen-7767cb56c8ca7432` | done | ✅ | ✅ | 5 | 10 |  |
| `gen-eebeba67ce824e4b` | done | ❌ | ❌ | 5 | 12 | url lacks 'q=rabbitmq' |
| `gen-db44c1c9fd216f25` | done | ✅ | ✅ | 6 | 16 |  |
| `gen-b2c7898d99471e1d` | done | ✅ | ✅ | 4 | 50 |  |
| `gen-258352d7a3e8e080` | done | ✅ | ✅ | 9 | 17 |  |
| `gen-89a4a6bbc19967a5` | done | ❌ | ❌ | 5 | 15 | missing evidence: [['tensorflow']] |

## Step outcomes

- `executed`: 29 (56%)
- `done-rejected`: 9 (17%)
- `done`: 8 (15%)
- `stale`: 4 (8%)
- `refused-empty-enter`: 2 (4%)

low-confidence decisions (< τ): 5
