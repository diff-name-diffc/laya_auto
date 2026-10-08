# liveweb-benchmark report

- generated: `2026-09-28T12:57:25+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **25** (~4.2/task)
- mean steps 9.2, mean duration 69.2s, decision p50/p95 156.1/274.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 0% | 10.6 |
| google | 1 | 0% | 0% | 2.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-15ae128d139b8db4` | blocked | ❌ | ❌ | 7 | 75 | missing evidence: [['fork', 'forks']] |
| `gen-42d8d37c4f7b02eb` | blocked | ❌ | ❌ | 11 | 152 | missing evidence: [['fork', 'forks']] |
| `gen-87aadadc92e151b0` | blocked | ❌ | ❌ | 8 | 29 | missing evidence: [['fork', 'forks']] |
| `gen-2dae4fcffcf7d6a3` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-e4204230ed00889e` | blocked | ❌ | ❌ | 13 | 105 | missing evidence: [['fork', 'forks']] |
| `gen-a67757782bd08c2c` | blocked | ❌ | ❌ | 14 | 38 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 40 (73%)
- `no-text-model`: 5 (9%)
- `stale`: 5 (9%)
- `target occluded`: 2 (4%)
- `refused-empty-enter`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 2
