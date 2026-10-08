# liveweb-benchmark report

- generated: `2026-09-28T11:22:14+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **5** (~0.8/task)
- mean steps 1.2, mean duration 5.7s, decision p50/p95 0.0/210.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 1.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-ba1a3f56f920bd3e` | incomplete | ❌ | ❌ | 7 | 26 | missing evidence: [['fork', 'forks']] |
| `gen-8b488fff2632dc6a` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-229932f524590027` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-d598abf49ca5ecff` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-6b36b0bb22712464` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-a70f41ff7cdf5959` | incomplete | ❌ | ❌ | 0 | 0 | harness error |

## Step outcomes

- `executed`: 6 (86%)
- `refused-empty-enter`: 1 (14%)

low-confidence decisions (< τ): 0
