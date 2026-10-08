# liveweb-benchmark report

- generated: `2026-09-28T12:48:38+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **24** (~4.0/task)
- mean steps 13.2, mean duration 124.8s, decision p50/p95 168.8/378.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 0% | 15.4 |
| google | 1 | 0% | 0% | 2.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-eccf0fd7418fa640` | blocked | ❌ | ❌ | 8 | 40 | missing evidence: [['fork', 'forks']] |
| `gen-aa2872eadc4399ec` | blocked | ❌ | ❌ | 20 | 420 | missing evidence: [['fork', 'forks']] |
| `gen-b44cbedd812dce29` | repeat-loop | ❌ | ❌ | 28 | 143 | missing evidence: [['fork', 'forks']] |
| `gen-f3d497c5cb937d5a` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-bd46074de276eda4` | blocked | ❌ | ❌ | 9 | 22 | missing evidence: [['fork', 'forks']] |
| `gen-69b5b23079f8da36` | blocked | ❌ | ❌ | 12 | 110 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 52 (66%)
- `refused-empty-enter`: 13 (16%)
- `stale`: 7 (9%)
- `no-text-model`: 4 (5%)
- `done-rejected`: 2 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 12
