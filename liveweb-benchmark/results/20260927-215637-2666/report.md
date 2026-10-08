# liveweb-benchmark report

- generated: `2026-09-27T22:00:59+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 10.1, mean duration 25.9s, decision p50/p95 584.4/789.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 10.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-e9177e12e87fdfa9` | done | ❌ | ❌ | 11 | 18 | missing evidence: [['django']] |
| `gen-6cfbe6cdbd27ac20` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-b69a3f3fccc75b4b` | done | ❌ | ❌ | 8 | 17 | missing evidence: [['patterns', 'design']] |
| `gen-d8f726710c936586` | done | ✅ | ✅ | 23 | 88 |  |
| `gen-eb2cc365ea3f4fc4` | done | ❌ | ❌ | 8 | 14 | url lacks 'q=fine-tuning' |
| `gen-91617ded8d31171e` | done | ✅ | ✅ | 12 | 30 |  |
| `gen-8bdf5adc0276315d` | done | ❌ | ❌ | 8 | 16 | missing evidence: [['mysql']] |
| `gen-aced0752ef30460e` | done | ❌ | ❌ | 8 | 18 | missing evidence: [['flask']] |

## Step outcomes

- `executed`: 42 (52%)
- `stale`: 10 (12%)
- `done-rejected`: 10 (12%)
- `page changed since the decision (url or marker mismatch)`: 10 (12%)
- `done`: 8 (10%)
- `refused-empty-enter`: 1 (1%)

low-confidence decisions (< τ): 5
