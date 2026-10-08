# liveweb-benchmark report

- generated: `2026-09-28T11:22:21+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **3** (~0.5/task)
- mean steps 1.3, mean duration 10.8s, decision p50/p95 211.4/494.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 0% | 1.6 |
| google | 1 | 0% | 0% | 0.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-84850bbef646a3ca` | incomplete | ❌ | ❌ | 8 | 55 | missing evidence: [['fork', 'forks']] |
| `gen-18d8e2a92820a49c` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-4c8fc6d75d579316` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['concurrency']] |
| `gen-d3675484d6543cf0` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-4effb5fedaac9697` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-48cee79a60f77ef6` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |

## Step outcomes

- `executed`: 5 (62%)
- `done-rejected`: 1 (12%)
- `refused-empty-enter`: 1 (12%)
- `page changed since the decision (url or marker mismatch)`: 1 (12%)

low-confidence decisions (< τ): 0
