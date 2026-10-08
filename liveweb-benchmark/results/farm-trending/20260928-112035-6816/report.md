# liveweb-benchmark report

- generated: `2026-09-28T11:22:07+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **1**
- VLM rescues: **7** (~1.2/task)
- mean steps 2.7, mean duration 6.7s, decision p50/p95 188.5/284.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 17% | 2.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-c2a77b3b10bfab57` | blocked | ❌ | ❌ | 7 | 19 | missing evidence: [['fork', 'forks']] |
| `gen-a8a9b5f58ba5bafd` | incomplete | ✅ | ❌ | 9 | 13 | model error: network error persisted: <urlopen error [Errno  |
| `gen-d3e118546cdd519c` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-0d8378df06a4908d` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-4d4d5e2fbc6bb6f7` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-4e88e150b7ee968f` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 15 (94%)
- `no-text-model`: 1 (6%)

low-confidence decisions (< τ): 3
