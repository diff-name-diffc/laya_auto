# liveweb-benchmark report

- generated: `2026-09-28T12:28:24+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **1/6** (17%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **0**
- VLM rescues: **24** (~4.0/task)
- mean steps 11.5, mean duration 70.4s, decision p50/p95 201.9/282.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 0% | 11.2 |
| google | 1 | 100% | 100% | 13.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-d3e0aa3505f8b3e4` | blocked | ❌ | ❌ | 10 | 134 | missing evidence: [['fork', 'forks']] |
| `gen-fcce6216d8aaf69b` | done | ✅ | ✅ | 13 | 18 |  |
| `gen-d2cc52ddda93c207` | blocked | ❌ | ❌ | 10 | 133 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |
| `gen-ee48aca1d3497e3b` | blocked | ❌ | ❌ | 8 | 33 | missing evidence: [['fork', 'forks']] |
| `gen-52c1301e9f8fd354` | blocked | ❌ | ❌ | 8 | 14 | missing evidence: [['fork', 'forks']] |
| `gen-4c1d04e500d6777c` | blocked | ❌ | ❌ | 20 | 90 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 49 (71%)
- `refused-empty-enter`: 8 (12%)
- `no-text-model`: 5 (7%)
- `stale`: 2 (3%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)
- `done-rejected`: 2 (3%)
- `done`: 1 (1%)

low-confidence decisions (< τ): 7
