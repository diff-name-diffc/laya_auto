# liveweb-benchmark report

- generated: `2026-09-28T12:19:57+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **30** (~5.0/task)
- mean steps 13.5, mean duration 71.5s, decision p50/p95 193.2/322.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 13.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-ed7f92f0c69cc53a` | blocked | ❌ | ❌ | 14 | 66 | missing evidence: [['fork', 'forks']] |
| `gen-62a5f2f92d5b75a1` | blocked | ❌ | ❌ | 7 | 37 | missing evidence: [['fork', 'forks']] |
| `gen-22bee9df978935fa` | blocked | ❌ | ❌ | 7 | 16 | missing evidence: [['fork', 'forks']] |
| `gen-0d8378df06a4908d` | done | ❌ | ❌ | 16 | 119 | url still contains '/search' |
| `gen-69037d2a4d11f63c` | blocked | ❌ | ❌ | 10 | 116 | missing evidence: [['fork', 'forks']] |
| `gen-22e75c366e6d4beb` | repeat-loop | ❌ | ❌ | 27 | 76 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 64 (79%)
- `refused-empty-enter`: 6 (7%)
- `no-text-model`: 4 (5%)
- `done-rejected`: 3 (4%)
- `page changed since the decision (url or marker mismatch)`: 2 (2%)
- `stale`: 1 (1%)
- `done`: 1 (1%)

low-confidence decisions (< τ): 7
