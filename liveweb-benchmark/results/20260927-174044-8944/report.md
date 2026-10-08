# liveweb-benchmark report

- generated: `2026-09-27T17:44:12+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 9.6, mean duration 19.1s, decision p50/p95 572.2/811.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 100% | 100% | 8.0 |
| google | 7 | 57% | 57% | 9.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-5745ca3aa3d39f5d` | done | ✅ | ✅ | 7 | 12 |  |
| `gen-741f9db4c883b749` | done | ✅ | ✅ | 7 | 12 |  |
| `gen-a39dc9673a521d63` | done | ❌ | ❌ | 10 | 18 | url lacks 'q=quantization' |
| `gen-96b7ef1caee44705` | max-steps | ❌ | ❌ | 26 | 51 | missing evidence: [['typescript']] |
| `gen-a452bcb1a2ed4fb7` | done | ❌ | ❌ | 10 | 31 | url lacks 'q=generation' |
| `gen-0ee06bbe00b58660` | done | ✅ | ✅ | 6 | 9 |  |
| `gen-b6a4ed19ba05c11a` | done | ✅ | ✅ | 8 | 15 |  |
| `gen-26d249892575ca79` | done | ✅ | ✅ | 3 | 5 |  |

## Step outcomes

- `executed`: 39 (51%)
- `stale`: 13 (17%)
- `done-rejected`: 9 (12%)
- `done`: 7 (9%)
- `refused-empty-enter`: 6 (8%)
- `page changed since the decision (url or marker mismatch)`: 3 (4%)

low-confidence decisions (< τ): 6
