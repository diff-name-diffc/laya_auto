# liveweb-benchmark report

- generated: `2026-09-28T12:33:35+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **1/6** (17%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **0**
- VLM rescues: **26** (~4.3/task)
- mean steps 8.8, mean duration 40.6s, decision p50/p95 170.0/274.8 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 0% | 7.4 |
| google | 1 | 100% | 100% | 16.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-2734fa5d77401663` | done | ✅ | ✅ | 16 | 25 |  |
| `gen-eb986caff606fc49` | blocked | ❌ | ❌ | 7 | 25 | missing evidence: [['fork', 'forks']] |
| `gen-a85bcc13eedffc59` | blocked | ❌ | ❌ | 8 | 107 | missing evidence: [['fork', 'forks']] |
| `gen-3c0d71361ce34588` | blocked | ❌ | ❌ | 7 | 18 | missing evidence: [['fork', 'forks']] |
| `gen-3d2afd0be42af0c5` | blocked | ❌ | ❌ | 11 | 42 | missing evidence: [['fork', 'forks']] |
| `gen-2e3e4f1c4b76d03b` | incomplete | ❌ | ❌ | 4 | 27 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 40 (75%)
- `no-text-model`: 4 (8%)
- `stale`: 3 (6%)
- `done-rejected`: 2 (4%)
- `refused-empty-enter`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)
- `done`: 1 (2%)

low-confidence decisions (< τ): 4
