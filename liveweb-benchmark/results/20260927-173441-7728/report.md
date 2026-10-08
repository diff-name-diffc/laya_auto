# liveweb-benchmark report

- generated: `2026-09-27T17:37:16+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 6.9, mean duration 12.5s, decision p50/p95 533.4/790.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 14.0 |
| google | 7 | 86% | 86% | 5.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-e9857dc62238133b` | done | ✅ | ✅ | 13 | 23 |  |
| `gen-84fb72a998622e8b` | done | ✅ | ✅ | 8 | 13 |  |
| `gen-d27d61bbeb2b7514` | done | ✅ | ✅ | 5 | 9 |  |
| `gen-999b35774398544e` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-5e8b5cdfd77bb6e7` | done | ❌ | ❌ | 14 | 29 | url lacks 'github.com/search' |
| `gen-0651def5165e251b` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-bb0f972563ad21cf` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-8c6a82df9f1f663a` | done | ❌ | ❌ | 6 | 11 | missing evidence: [['logging']] |

## Step outcomes

- `executed`: 31 (56%)
- `done-rejected`: 9 (16%)
- `done`: 8 (15%)
- `refused-empty-enter`: 3 (5%)
- `stale`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 2 (4%)

low-confidence decisions (< τ): 3
