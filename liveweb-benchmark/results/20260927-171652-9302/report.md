# liveweb-benchmark report

- generated: `2026-09-27T17:20:04+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **7/8** (88%) — DONE **and** independently verified
- independently verified **7/8** (88%)
- found-but-never-stopped: **0**
- mean steps 9.0, mean duration 17.2s, decision p50/p95 572.0/854.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 11.0 |
| google | 7 | 100% | 100% | 8.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-98a0abe56d3dcbf0` | done | ✅ | ✅ | 7 | 14 |  |
| `gen-b4b96899c13aed0f` | done | ✅ | ✅ | 8 | 15 |  |
| `gen-4b5378efdc92ada0` | done | ✅ | ✅ | 3 | 6 |  |
| `gen-f17be885bc1cc1c3` | done | ✅ | ✅ | 21 | 31 |  |
| `gen-fe3c35caa7fc5772` | done | ❌ | ❌ | 11 | 37 | missing evidence: [['vue']] |
| `gen-c39848cc7edd262f` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-0d82835f574cd0dc` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-9ed586160894bb19` | done | ✅ | ✅ | 16 | 27 |  |

## Step outcomes

- `executed`: 43 (60%)
- `stale`: 9 (12%)
- `done`: 8 (11%)
- `done-rejected`: 7 (10%)
- `refused-empty-enter`: 3 (4%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)

low-confidence decisions (< τ): 7
