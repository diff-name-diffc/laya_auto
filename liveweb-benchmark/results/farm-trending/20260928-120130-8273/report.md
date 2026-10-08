# liveweb-benchmark report

- generated: `2026-09-28T12:11:41+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **1/6** (17%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **0**
- VLM rescues: **26** (~4.3/task)
- mean steps 12.2, mean duration 92.6s, decision p50/p95 180.2/290.8 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 17% | 17% | 12.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-0a5cc34aeae93f66` | blocked | ❌ | ❌ | 16 | 153 | missing evidence: [['fork', 'forks']] |
| `gen-a8a9b5f58ba5bafd` | done | ✅ | ✅ | 10 | 17 |  |
| `gen-d7d4afda569911b4` | blocked | ❌ | ❌ | 14 | 135 | missing evidence: [['fork', 'forks']] |
| `gen-8e38e24f9358cbd3` | blocked | ❌ | ❌ | 12 | 98 | missing evidence: [['fork', 'forks']] |
| `gen-c79cca8787642253` | blocked | ❌ | ❌ | 9 | 16 | missing evidence: [['fork', 'forks']] |
| `gen-b4686711b2a01d54` | blocked | ❌ | ❌ | 12 | 136 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 49 (67%)
- `stale`: 7 (10%)
- `refused-empty-enter`: 6 (8%)
- `no-text-model`: 5 (7%)
- `done-rejected`: 3 (4%)
- `failed`: 1 (1%)
- `done`: 1 (1%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 9
