# liveweb-benchmark report

- generated: `2026-09-27T21:15:55+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 7.5, mean duration 17.1s, decision p50/p95 589.8/674.8 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 62% | 62% | 7.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-f204cf5036813d6a` | done | ✅ | ✅ | 3 | 6 |  |
| `gen-258c07bb6a01ea68` | done | ❌ | ❌ | 10 | 18 | url lacks 'q=pipelines' |
| `gen-1358e608509e89dc` | done | ❌ | ❌ | 8 | 15 | url lacks 'q=patterns' |
| `gen-63762fa4af266169` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-251d12a01aa43164` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-0265d88d15062976` | repeat-loop | ❌ | ❌ | 23 | 51 | missing evidence: [['embeddings', 'vector']] |
| `gen-7e203bc1119a5499` | done | ✅ | ✅ | 7 | 35 |  |
| `gen-e946ef257ebc583f` | done | ✅ | ✅ | 3 | 5 |  |

## Step outcomes

- `executed`: 42 (70%)
- `done`: 7 (12%)
- `done-rejected`: 5 (8%)
- `page changed since the decision (url or marker mismatch)`: 3 (5%)
- `stale`: 2 (3%)
- `refused-empty-enter`: 1 (2%)

low-confidence decisions (< τ): 4
