# liveweb-benchmark report

- generated: `2026-09-28T12:17:18+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **1/6** (17%) — DONE **and** independently verified
- independently verified **1/6** (17%)
- found-but-never-stopped: **0**
- VLM rescues: **22** (~3.7/task)
- mean steps 11.5, mean duration 42.0s, decision p50/p95 200.7/350.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 5 | 0% | 0% | 11.2 |
| google | 1 | 100% | 100% | 13.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-4effb5fedaac9697` | blocked | ❌ | ❌ | 8 | 27 | missing evidence: [['fork', 'forks']] |
| `gen-7ffeb3ca1d0133cc` | blocked | ❌ | ❌ | 4 | 87 | missing evidence: [['fork', 'forks']] |
| `gen-ed4b9bbc8cefa85e` | done | ✅ | ✅ | 13 | 13 |  |
| `gen-f3090cf73243badc` | max-steps | ❌ | ❌ | 27 | 82 | missing evidence: [['fork', 'forks']] |
| `gen-7780f5fb4a2c4c8b` | blocked | ❌ | ❌ | 8 | 18 | missing evidence: [['fork', 'forks']] |
| `gen-e473dcee1e563432` | blocked | ❌ | ❌ | 9 | 26 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 49 (71%)
- `refused-empty-enter`: 7 (10%)
- `stale`: 5 (7%)
- `no-text-model`: 4 (6%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)
- `done`: 1 (1%)
- `done-rejected`: 1 (1%)

low-confidence decisions (< τ): 9
