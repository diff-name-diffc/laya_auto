# liveweb-benchmark report

- generated: `2026-09-27T17:37:43+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 10.0, mean duration 19.6s, decision p50/p95 566.8/924.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 12.0 |
| google | 6 | 67% | 67% | 9.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-5c17e2e338370a6c` | done | ❌ | ❌ | 7 | 11 | url lacks 'fastapi.tiangolo.com' |
| `gen-38a5eb22d84e0988` | done | ✅ | ✅ | 8 | 11 |  |
| `gen-5ad3da0fcc512d72` | done | ❌ | ❌ | 16 | 32 | url lacks 'github.com/search' |
| `gen-2182f209044e7caa` | done | ✅ | ✅ | 17 | 24 |  |
| `gen-cfe3abd83bd83d18` | done | ❌ | ❌ | 8 | 14 | missing evidence: [['golang']] |
| `gen-9107f6090340fe7f` | done | ❌ | ❌ | 8 | 20 | missing evidence: [['swift']] |
| `gen-d2ecf5a0ecb492cb` | done | ✅ | ✅ | 13 | 40 |  |
| `gen-772762b8489546ae` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 48 (60%)
- `done-rejected`: 14 (18%)
- `done`: 8 (10%)
- `page changed since the decision (url or marker mismatch)`: 4 (5%)
- `stale`: 3 (4%)
- `refused-empty-enter`: 3 (4%)

low-confidence decisions (< τ): 3
