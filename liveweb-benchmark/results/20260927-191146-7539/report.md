# liveweb-benchmark report

- generated: `2026-09-27T19:17:52+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 6.8, mean duration 22.0s, decision p50/p95 537.4/617.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 10.0 |
| google | 7 | 43% | 43% | 6.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-7a89222c83ec54ef` | bot-challenge | ❌ | ❌ | 5 | 26 | bot_challenge |
| `gen-b330bfa6e1cccf6c` | done | ✅ | ✅ | 16 | 21 |  |
| `gen-381be6c20ee31001` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-e03c60fd3d34a793` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-dc1c589166ad77ec` | done | ❌ | ❌ | 10 | 17 | missing evidence: [['zig']] |
| `gen-5ad8f0a3221f3393` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |
| `gen-6db6211048bfc14f` | done | ❌ | ❌ | 12 | 71 | missing evidence: [['refactoring']] |
| `gen-f0fdb9c63886d6ae` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 32 (59%)
- `stale`: 8 (15%)
- `done-rejected`: 7 (13%)
- `done`: 5 (9%)
- `refused-empty-enter`: 1 (2%)
- `failed`: 1 (2%)

low-confidence decisions (< τ): 8
