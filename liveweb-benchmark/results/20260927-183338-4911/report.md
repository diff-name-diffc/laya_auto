# liveweb-benchmark report

- generated: `2026-09-27T18:39:33+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 4.8, mean duration 15.0s, decision p50/p95 568.9/654.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 4.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-6761251e39bbd897` | bot-challenge | ❌ | ❌ | 7 | 22 | bot_challenge |
| `gen-7a9ca5f880daafd9` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-fe21fe06ab8760d8` | done | ✅ | ✅ | 5 | 9 |  |
| `gen-f4a8012c2f154f54` | done | ❌ | ❌ | 11 | 20 | url lacks 'q=debugging' |
| `gen-18ba54904541c08d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-ecffba535e70b32c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-53d9fbdf03d99242` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-bff1dfcbda1bee61` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |

## Step outcomes

- `executed`: 25 (66%)
- `stale`: 5 (13%)
- `done-rejected`: 3 (8%)
- `done`: 3 (8%)
- `refused-empty-enter`: 2 (5%)

low-confidence decisions (< τ): 4
