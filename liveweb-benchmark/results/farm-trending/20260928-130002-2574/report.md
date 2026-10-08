# liveweb-benchmark report

- generated: `2026-09-28T13:04:24+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **12** (~2.0/task)
- mean steps 6.8, mean duration 27.2s, decision p50/p95 213.8/287.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 4 | 0% | 0% | 5.5 |
| google | 2 | 0% | 0% | 9.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-07b98c46e96a4145` | blocked | ❌ | ❌ | 14 | 109 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |
| `gen-e3f97e74ce0c21b9` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-46a40c1f65a5eea7` | blocked | ❌ | ❌ | 8 | 15 | missing evidence: [['fork', 'forks']] |
| `gen-4578e5aed8728252` | incomplete | ❌ | ❌ | 17 | 21 | missing evidence: [['elixir']] |
| `gen-ba1a3f56f920bd3e` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-abcc9d1a524ce7d3` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 32 (78%)
- `stale`: 3 (7%)
- `refused-empty-enter`: 2 (5%)
- `no-text-model`: 2 (5%)
- `done-rejected`: 1 (2%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 5
