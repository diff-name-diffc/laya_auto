# liveweb-benchmark report

- generated: `2026-09-27T17:19:43+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 7.9, mean duration 12.6s, decision p50/p95 520.9/927.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 100% | 100% | 13.0 |
| google | 7 | 71% | 71% | 7.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-2d6f9385192be34b` | done | ✅ | ✅ | 8 | 12 |  |
| `gen-903b721aec5a3b02` | done | ✅ | ✅ | 8 | 11 |  |
| `gen-ec37ac049fe8138f` | done | ✅ | ✅ | 13 | 19 |  |
| `gen-e603d06bde89f079` | done | ✅ | ✅ | 9 | 15 |  |
| `gen-e27a58441409a794` | done | ❌ | ❌ | 8 | 15 | missing evidence: [['scala']] |
| `gen-5b703b12a71f168b` | done | ✅ | ✅ | 4 | 7 |  |
| `gen-42b36b58004a9415` | done | ❌ | ❌ | 10 | 17 | missing evidence: [['review', 'code']] |
| `gen-bd0a0cf5903abe2f` | done | ✅ | ✅ | 3 | 5 |  |

## Step outcomes

- `executed`: 31 (49%)
- `done-rejected`: 12 (19%)
- `done`: 8 (13%)
- `stale`: 6 (10%)
- `page changed since the decision (url or marker mismatch)`: 4 (6%)
- `refused-empty-enter`: 2 (3%)

low-confidence decisions (< τ): 4
