# liveweb-benchmark report

- generated: `2026-09-27T20:21:10+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 4.9, mean duration 14.0s, decision p50/p95 492.5/680.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 4.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-570bb4df0c223820` | done | ✅ | ✅ | 6 | 22 |  |
| `gen-66e19c913fc4a898` | repeat-loop | ❌ | ❌ | 8 | 52 | missing evidence: [['debugging', 'memory']] |
| `gen-3980a81f4587083c` | done | ✅ | ✅ | 5 | 8 |  |
| `gen-74e1b5988ad1908d` | done | ❌ | ❌ | 6 | 11 | missing evidence: [['patterns', 'design']] |
| `gen-eaf6b208b5bbe3ad` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-5e7370270cc25afb` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-56d6c2816d559b1d` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-553149439745a7a6` | done | ✅ | ✅ | 5 | 6 |  |

## Step outcomes

- `executed`: 20 (51%)
- `done`: 7 (18%)
- `stale`: 4 (10%)
- `refused-empty-enter`: 4 (10%)
- `done-rejected`: 4 (10%)

low-confidence decisions (< τ): 3
