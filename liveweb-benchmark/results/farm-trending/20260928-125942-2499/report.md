# liveweb-benchmark report

- generated: `2026-09-28T13:06:21+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **19** (~3.2/task)
- mean steps 8.5, mean duration 57.1s, decision p50/p95 168.2/277.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 8.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-83e98cc99da94722` | blocked | ❌ | ❌ | 11 | 207 | missing evidence: [['fork', 'forks']] |
| `gen-35c154215713a52c` | incomplete | ❌ | ❌ | 23 | 36 | missing evidence: [['fork', 'forks']] |
| `gen-259dd223d5134d3b` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-90aa6b51320dc552` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-72c58ed14e4a376f` | blocked | ❌ | ❌ | 7 | 19 | missing evidence: [['fork', 'forks']] |
| `gen-b4ecc40be1539339` | blocked | ❌ | ❌ | 10 | 76 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 42 (82%)
- `done-rejected`: 3 (6%)
- `refused-empty-enter`: 3 (6%)
- `no-text-model`: 3 (6%)

low-confidence decisions (< τ): 6
