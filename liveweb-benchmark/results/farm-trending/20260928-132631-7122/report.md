# liveweb-benchmark report

- generated: `2026-09-28T13:33:45+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **1**
- VLM rescues: **21** (~3.5/task)
- mean steps 9.7, mean duration 55.9s, decision p50/p95 163.5/400.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 20% | 11.2 |
| google | 1 | 0% | 0% | 2.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-4105fa40826e2766` | blocked | ❌ | ❌ | 16 | 25 | missing evidence: [['fork', 'forks']] |
| `gen-c8a85380f0b47dc1` | unstable-page | ❌ | ❌ | 8 | 13 | missing evidence: [['star', 'stars'], ['fork', 'forks']] |
| `gen-8d53eda117e97afb` | blocked | ❌ | ❌ | 9 | 39 | missing evidence: [['fork', 'forks']] |
| `gen-9e9ec363a7e0e5cb` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-5a0c7e66e8b06dcf` | blocked | ✅ | ❌ | 14 | 213 |  |
| `gen-4c3a485552c42851` | blocked | ❌ | ❌ | 9 | 32 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 31 (53%)
- `refused-empty-enter`: 12 (21%)
- `stale`: 6 (10%)
- `no-text-model`: 4 (7%)
- `done-rejected`: 3 (5%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)

low-confidence decisions (< τ): 10
