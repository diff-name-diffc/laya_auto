# liveweb-benchmark report

- generated: `2026-09-28T12:59:32+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **21** (~3.5/task)
- mean steps 11.7, mean duration 94.4s, decision p50/p95 196.0/269.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 11.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-b298a0b35759b2c5` | blocked | ❌ | ❌ | 8 | 105 | missing evidence: [['fork', 'forks']] |
| `gen-da8768818917f8c1` | blocked | ❌ | ❌ | 21 | 49 | missing evidence: [['fork', 'forks']] |
| `gen-82397896a6540ebb` | blocked | ❌ | ❌ | 17 | 102 | missing evidence: [['fork', 'forks']] |
| `gen-a491901fd5214983` | blocked | ❌ | ❌ | 11 | 105 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |
| `gen-986034e5a212a9b6` | blocked | ❌ | ❌ | 5 | 103 | missing evidence: [['fork', 'forks']] |
| `gen-14ed0d6385af2628` | blocked | ❌ | ❌ | 8 | 103 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 57 (81%)
- `no-text-model`: 6 (9%)
- `refused-empty-enter`: 4 (6%)
- `stale`: 2 (3%)
- `done-rejected`: 1 (1%)

low-confidence decisions (< τ): 8
