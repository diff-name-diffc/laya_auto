# liveweb-benchmark report

- generated: `2026-09-27T15:37:19+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/12** (50%) — DONE **and** independently verified
- independently verified **6/12** (50%)
- found-but-never-stopped: **0**
- mean steps 8.0, mean duration 23.9s, decision p50/p95 584.8/714.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 15.0 |
| google | 10 | 60% | 60% | 6.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-68925aee21e8ec1d` | done | ❌ | ❌ | 11 | 19 | url lacks 'google.com/search' |
| `gen-36c71b329e08a93d` | done | ❌ | ❌ | 8 | 20 | missing evidence: [['typescript']] |
| `gen-749cc9d72abc1a67` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-7a11e3b8a34f687a` | done | ❌ | ❌ | 11 | 19 | url lacks 'q=transformers' |
| `gen-96aeaec0faffc3f3` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-7973b06af6fc9f4b` | done | ❌ | ❌ | 15 | 94 | url lacks 'github.com/search' |
| `gen-2778afbe56ee45b1` | done | ✅ | ✅ | 8 | 15 |  |
| `gen-a5dc5ebb76b29854` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-d1d6c63130ab92e8` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-b9493c999f5710ae` | done | ❌ | ❌ | 15 | 68 | url lacks 'github.com/search' |
| `gen-6671274708dd23e9` | done | ✅ | ✅ | 4 | 8 |  |
| `gen-09c89e979c24cb54` | done | ❌ | ❌ | 8 | 18 | missing evidence: [['mysql']] |

## Step outcomes

- `executed`: 60 (62%)
- `done-rejected`: 13 (14%)
- `done`: 12 (12%)
- `stale`: 6 (6%)
- `page changed since the decision (url or marker mismatch)`: 3 (3%)
- `refused-empty-enter`: 2 (2%)

low-confidence decisions (< τ): 12
