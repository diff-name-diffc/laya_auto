# liveweb-benchmark report

- generated: `2026-09-28T13:37:49+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **5** (~0.8/task)
- mean steps 1.3, mean duration 8.8s, decision p50/p95 0.0/301.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 1.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-d13ef174b9f29785` | blocked | ❌ | ❌ | 8 | 42 | missing evidence: [['fork', 'forks']] |
| `gen-82503f1b3aa18f29` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-76937f75455ef658` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-60636fb23624c432` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-1938a42cc3f545a5` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |
| `gen-145b2ff33c9d2815` | incomplete | ❌ | ❌ | 0 | 2 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 6 (75%)
- `refused-empty-enter`: 1 (12%)
- `no-text-model`: 1 (12%)

low-confidence decisions (< τ): 0
