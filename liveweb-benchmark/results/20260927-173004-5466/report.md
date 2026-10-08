# liveweb-benchmark report

- generated: `2026-09-27T17:33:55+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 11.0, mean duration 22.0s, decision p50/p95 524.9/713.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 75% | 75% | 11.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-a94aacfe02d1d7ac` | done | ✅ | ✅ | 14 | 21 |  |
| `gen-c2192624ec52e896` | max-steps | ❌ | ❌ | 29 | 73 | missing evidence: [['rust']] |
| `gen-26bfd47a4b2f2e3d` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-f3d28af8c95b5c7b` | done | ✅ | ✅ | 6 | 9 |  |
| `gen-4035ae5446a38f2a` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-5662cb0feb744f3e` | done | ❌ | ❌ | 5 | 6 | url lacks 'q=python' |
| `gen-6769a1e870308b6f` | done | ✅ | ✅ | 6 | 10 |  |
| `gen-dbf8c428cff67e4d` | done | ✅ | ✅ | 22 | 48 |  |

## Step outcomes

- `executed`: 63 (72%)
- `stale`: 9 (10%)
- `done`: 7 (8%)
- `refused-empty-enter`: 5 (6%)
- `done-rejected`: 3 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 8
