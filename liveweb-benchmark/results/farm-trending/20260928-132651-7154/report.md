# liveweb-benchmark report

- generated: `2026-09-28T13:35:32+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **27** (~4.5/task)
- mean steps 9.5, mean duration 77.6s, decision p50/p95 140.2/264.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 9.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-950b8d6ea9b18ffe` | blocked | ❌ | ❌ | 13 | 111 | missing evidence: [['fork', 'forks']] |
| `gen-d7bc164e9166bf6e` | blocked | ❌ | ❌ | 10 | 64 | missing evidence: [['fork', 'forks']] |
| `gen-99a055b842569fdb` | repeat-loop | ❌ | ❌ | 11 | 70 | missing evidence: [['fork', 'forks']] |
| `gen-025e9cc3cfbde41c` | blocked | ❌ | ❌ | 7 | 36 | missing evidence: [['fork', 'forks']] |
| `gen-ccd1b50ff8227618` | blocked | ❌ | ❌ | 8 | 24 | missing evidence: [['fork', 'forks']] |
| `gen-91cb5455d9eaf8db` | blocked | ❌ | ❌ | 8 | 161 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |

## Step outcomes

- `executed`: 42 (74%)
- `refused-empty-enter`: 7 (12%)
- `no-text-model`: 5 (9%)
- `stale`: 2 (4%)
- `done-rejected`: 1 (2%)

low-confidence decisions (< τ): 7
