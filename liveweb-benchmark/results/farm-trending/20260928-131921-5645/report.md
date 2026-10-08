# liveweb-benchmark report

- generated: `2026-09-28T13:26:21+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **1/6** (17%) — DONE **and** independently verified
- independently verified **2/6** (33%)
- found-but-never-stopped: **1**
- VLM rescues: **12** (~2.0/task)
- mean steps 7.3, mean duration 61.1s, decision p50/p95 194.8/428.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 17% | 33% | 7.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-2361e781774f0097` | done | ❌ | ❌ | 12 | 19 | missing evidence: [['fork', 'forks']] |
| `gen-83d70b016b0732c7` | incomplete | ✅ | ❌ | 10 | 151 | model error: network error persisted: <urlopen error [Errno  |
| `gen-3bcbd6961962ddde` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-9a47f8403a50c294` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-092bc763362762f6` | done | ✅ | ✅ | 13 | 152 |  |
| `gen-8976d62a098412a2` | blocked | ❌ | ❌ | 9 | 40 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 21 (48%)
- `refused-empty-enter`: 15 (34%)
- `page changed since the decision (url or marker mismatch)`: 2 (5%)
- `stale`: 2 (5%)
- `done`: 2 (5%)
- `done-rejected`: 1 (2%)
- `no-text-model`: 1 (2%)

low-confidence decisions (< τ): 9
