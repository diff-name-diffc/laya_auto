# liveweb-benchmark report

- generated: `2026-09-27T22:44:19+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 12.1, mean duration 23.8s, decision p50/p95 581.9/772.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 50% | 50% | 12.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-b0d0d99855aa0758` | done | ✅ | ✅ | 16 | 27 |  |
| `gen-ff42a119f4011e73` | done | ✅ | ✅ | 14 | 45 |  |
| `gen-db172941c123fc81` | done | ❌ | ❌ | 16 | 31 | url lacks 'q=langchain' |
| `gen-53befbf089d28331` | done | ❌ | ❌ | 4 | 9 | url lacks 'q=django' |
| `gen-931942796a428228` | done | ✅ | ✅ | 4 | 8 |  |
| `gen-5690973d17a67a9b` | done | ✅ | ✅ | 22 | 37 |  |
| `gen-fede450ac89b37d9` | done | ❌ | ❌ | 11 | 18 | url lacks 'q=pipelines' |
| `gen-f546f8355d8746a9` | done | ❌ | ❌ | 10 | 15 | missing evidence: [['spring', 'boot']] |

## Step outcomes

- `executed`: 57 (59%)
- `stale`: 12 (12%)
- `done-rejected`: 11 (11%)
- `done`: 8 (8%)
- `page changed since the decision (url or marker mismatch)`: 8 (8%)
- `refused-empty-enter`: 1 (1%)

low-confidence decisions (< τ): 9
