# liveweb-benchmark report

- generated: `2026-09-28T12:09:19+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **1**
- VLM rescues: **30** (~5.0/task)
- mean steps 12.5, mean duration 72.4s, decision p50/p95 188.7/316.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 17% | 12.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-c969140d4dee8cbf` | blocked | ❌ | ❌ | 19 | 84 | missing evidence: [['fork', 'forks']] |
| `gen-8e1c53480dd51627` | blocked | ❌ | ❌ | 9 | 19 | missing evidence: [['fork', 'forks']] |
| `gen-7d2e20f42881fc2d` | blocked | ✅ | ❌ | 18 | 71 |  |
| `gen-6cbc3ba45fd94e61` | blocked | ❌ | ❌ | 13 | 222 | missing evidence: [['fork', 'forks']] |
| `gen-84850bbef646a3ca` | blocked | ❌ | ❌ | 9 | 19 | missing evidence: [['fork', 'forks']] |
| `gen-2746e815da2b48f5` | blocked | ❌ | ❌ | 7 | 19 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 53 (71%)
- `refused-empty-enter`: 10 (13%)
- `no-text-model`: 6 (8%)
- `done-rejected`: 4 (5%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)
- `stale`: 1 (1%)

low-confidence decisions (< τ): 6
