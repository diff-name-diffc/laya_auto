# liveweb-benchmark report

- generated: `2026-09-28T12:33:59+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **12** (~2.0/task)
- mean steps 4.7, mean duration 41.6s, decision p50/p95 198.9/288.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 4.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-01833c08ef125173` | blocked | ❌ | ❌ | 7 | 20 | missing evidence: [['fork', 'forks']] |
| `gen-49571a7155754d22` | blocked | ❌ | ❌ | 12 | 64 | missing evidence: [['fork', 'forks']] |
| `gen-b507420b0818902e` | blocked | ❌ | ❌ | 8 | 158 | missing evidence: [['fork', 'forks']] |
| `gen-d98a24a5cbc7c6df` | incomplete | ❌ | ❌ | 1 | 4 | missing evidence: [['fork', 'forks']] |
| `gen-d5eb84cfb4ed6f8d` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-e27a3aa5b9fd2bdf` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 21 (75%)
- `no-text-model`: 3 (11%)
- `done-rejected`: 2 (7%)
- `refused-empty-enter`: 2 (7%)

low-confidence decisions (< τ): 2
