# liveweb-benchmark report

- generated: `2026-09-28T13:14:04+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **1**
- VLM rescues: **22** (~3.7/task)
- mean steps 13.8, mean duration 63.3s, decision p50/p95 227.6/280.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 4 | 0% | 25% | 7.2 |
| google | 2 | 0% | 0% | 27.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-9eba9059b0c1cc41` | blocked | ❌ | ❌ | 10 | 158 | missing evidence: [['fork', 'forks']] |
| `gen-569b69651748061e` | blocked | ✅ | ❌ | 5 | 86 |  |
| `gen-fe947587e10d1c15` | blocked | ❌ | ❌ | 7 | 15 | missing evidence: [['fork', 'forks']] |
| `gen-e629ac1a952740c4` | blocked | ❌ | ❌ | 7 | 44 | missing evidence: [['fork', 'forks']] |
| `gen-85033717c5e3a99e` | repeat-loop | ❌ | ❌ | 25 | 44 | missing evidence: [['embeddings', 'vector']] |
| `gen-9e9533f4ad600d6f` | max-steps | ❌ | ❌ | 29 | 32 | missing evidence: [['logging']] |

## Step outcomes

- `executed`: 58 (70%)
- `stale`: 12 (14%)
- `page changed since the decision (url or marker mismatch)`: 5 (6%)
- `no-text-model`: 4 (5%)
- `done-rejected`: 2 (2%)
- `refused-empty-enter`: 2 (2%)

low-confidence decisions (< τ): 2
