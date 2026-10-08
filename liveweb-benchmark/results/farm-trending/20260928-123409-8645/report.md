# liveweb-benchmark report

- generated: `2026-09-28T12:39:56+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **1/6** (17%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **0**
- VLM rescues: **19** (~3.2/task)
- mean steps 8.0, mean duration 48.6s, decision p50/p95 199.9/278.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 4 | 0% | 0% | 9.5 |
| google | 2 | 50% | 50% | 5.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-21a0fe7cb1821e3f` | blocked | ❌ | ❌ | 9 | 22 | missing evidence: [['fork', 'forks']] |
| `gen-6aa3b5554e3c4ae1` | done | ❌ | ❌ | 5 | 3 | url lacks 'q=review' |
| `gen-57373d914cf97e6a` | done | ✅ | ✅ | 5 | 8 |  |
| `gen-cde44f18e9b61931` | blocked | ❌ | ❌ | 9 | 147 | missing evidence: [['fork', 'forks']] |
| `gen-e12106b842b4152b` | blocked | ❌ | ❌ | 9 | 34 | missing evidence: [['fork', 'forks']] |
| `gen-b08d2231a99fe65c` | repeat-loop | ❌ | ❌ | 11 | 79 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 33 (69%)
- `refused-empty-enter`: 5 (10%)
- `done-rejected`: 3 (6%)
- `no-text-model`: 3 (6%)
- `stale`: 2 (4%)
- `done`: 2 (4%)

low-confidence decisions (< τ): 6
