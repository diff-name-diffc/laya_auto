# liveweb-benchmark report

- generated: `2026-09-27T17:25:06+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 9.2, mean duration 19.5s, decision p50/p95 462.3/693.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 50% | 50% | 9.5 |
| google | 6 | 67% | 67% | 9.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-408e730d94c5adc2` | done | ❌ | ❌ | 8 | 40 | url lacks 'q=svelte' |
| `gen-c6e2ff238c32a2f4` | max-steps | ❌ | ❌ | 26 | 31 | missing evidence: [['postgresql']] |
| `gen-9845770cb949a9f3` | done | ✅ | ✅ | 8 | 14 |  |
| `gen-e24858a42be9faa1` | done | ✅ | ✅ | 5 | 9 |  |
| `gen-a94bf85646b4930a` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-ff6a89375b5eb2ad` | done | ❌ | ❌ | 11 | 33 | missing evidence: [['quantization', 'model']] |
| `gen-97221521fd9aeafb` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-6926974aba7bbad7` | done | ✅ | ✅ | 10 | 21 |  |

## Step outcomes

- `executed`: 51 (69%)
- `done-rejected`: 8 (11%)
- `done`: 7 (9%)
- `stale`: 4 (5%)
- `refused-empty-enter`: 2 (3%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)

low-confidence decisions (< τ): 1
