# liveweb-benchmark report

- generated: `2026-09-27T15:42:49+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **8/12** (67%) — DONE **and** independently verified
- independently verified **8/12** (67%)
- found-but-never-stopped: **0**
- mean steps 6.2, mean duration 15.8s, decision p50/p95 574.9/634.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 12 | 67% | 67% | 6.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-ede91bc4d9dae188` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-2bb7fb0a11e16b7b` | done | ✅ | ✅ | 14 | 26 |  |
| `gen-c23e0485d08710dd` | done | ❌ | ❌ | 10 | 22 | url lacks 'q=generation' |
| `gen-19d3c85811dc58bf` | done | ❌ | ❌ | 6 | 28 | missing evidence: [['golang']] |
| `gen-b58dd11bc0fd199a` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-328c819befa484e2` | done | ❌ | ❌ | 3 | 5 | url lacks 'q=embeddings' |
| `gen-8ff1cb4610808eb7` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-93ad175dc724614f` | done | ✅ | ✅ | 13 | 22 |  |
| `gen-5ce62e8e5f8bef91` | done | ✅ | ✅ | 10 | 44 |  |
| `gen-52d5f1f1bf5628fc` | done | ✅ | ✅ | 4 | 9 |  |
| `gen-0cd5b6edf3f24ddd` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-105bf26a1c7e178f` | done | ✅ | ✅ | 3 | 5 |  |

## Step outcomes

- `executed`: 48 (65%)
- `done`: 11 (15%)
- `done-rejected`: 6 (8%)
- `stale`: 5 (7%)
- `page changed since the decision (url or marker mismatch)`: 3 (4%)
- `refused-empty-enter`: 1 (1%)

low-confidence decisions (< τ): 7
