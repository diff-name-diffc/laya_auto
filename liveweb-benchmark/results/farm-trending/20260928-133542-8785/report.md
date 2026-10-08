# liveweb-benchmark report

- generated: `2026-09-28T13:38:00+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **1**
- VLM rescues: **2** (~0.3/task)
- mean steps 1.0, mean duration 14.2s, decision p50/p95 238.7/309.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 20% | 1.2 |
| google | 1 | 0% | 0% | 0.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-c8906f50390e2e23` | incomplete | ✅ | ❌ | 6 | 75 | model error: network error persisted: <urlopen error [Errno  |
| `gen-eb29b7d2344509ff` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['rabbitmq']] |
| `gen-9a752709137939fc` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-250a99f2c24f90c4` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-f44708643b193e3c` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-e2fdcf7d6ab7304f` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 4 (67%)
- `refused-empty-enter`: 1 (17%)
- `page changed since the decision (url or marker mismatch)`: 1 (17%)

low-confidence decisions (< τ): 1
