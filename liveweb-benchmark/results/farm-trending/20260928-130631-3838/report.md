# liveweb-benchmark report

- generated: `2026-09-28T13:13:07+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **27** (~4.5/task)
- mean steps 11.0, mean duration 56.8s, decision p50/p95 193.2/275.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 11.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-6b68e1e26be0c9f0` | blocked | ❌ | ❌ | 9 | 102 | missing evidence: [['fork', 'forks']] |
| `gen-c22fcacd7d5b879c` | blocked | ❌ | ❌ | 13 | 23 | missing evidence: [['fork', 'forks']] |
| `gen-ec0270e1a958cfe9` | blocked | ❌ | ❌ | 17 | 47 | missing evidence: [['fork', 'forks']] |
| `gen-5cb903ba90a49a34` | blocked | ❌ | ❌ | 7 | 37 | missing evidence: [['fork', 'forks']] |
| `gen-5ee2fd89bde20a72` | blocked | ❌ | ❌ | 8 | 20 | missing evidence: [['fork', 'forks']] |
| `gen-c55b7351a38ef9fe` | blocked | ❌ | ❌ | 12 | 111 | missing evidence: [['fork', 'forks']] |

## Step outcomes

- `executed`: 45 (68%)
- `refused-empty-enter`: 6 (9%)
- `no-text-model`: 6 (9%)
- `stale`: 4 (6%)
- `done-rejected`: 3 (5%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)

low-confidence decisions (< τ): 12
