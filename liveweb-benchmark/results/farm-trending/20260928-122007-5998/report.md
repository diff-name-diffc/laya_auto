# liveweb-benchmark report

- generated: `2026-09-28T12:25:31+0800`
- backend: `http://127.0.0.1:8812`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=8.0s

## Summary

- success **0/6** (0%) — DONE **and** independently verified
- independently verified **0/6** (0%)
- found-but-never-stopped: **0**
- VLM rescues: **30** (~5.0/task)
- mean steps 12.3, mean duration 44.5s, decision p50/p95 159.5/278.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 6 | 0% | 0% | 12.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-729f773c577280ca` | blocked | ❌ | ❌ | 9 | 27 | missing evidence: [['fork', 'forks']] |
| `gen-8705a17250f135c5` | blocked | ❌ | ❌ | 7 | 17 | missing evidence: [['fork', 'forks']] |
| `gen-c9e3599696b70cde` | blocked | ❌ | ❌ | 7 | 33 | missing evidence: [['fork', 'forks']] |
| `gen-ba4d3230422a9a3b` | blocked | ❌ | ❌ | 7 | 41 | missing evidence: [['fork', 'forks']] |
| `gen-4cbf475d5b666be1` | blocked | ❌ | ❌ | 14 | 60 | missing evidence: [['fork', 'forks']] |
| `gen-656c3dbaf2a88ed7` | repeat-loop | ❌ | ❌ | 30 | 88 | missing evidence: [['scala']] |

## Step outcomes

- `executed`: 64 (86%)
- `no-text-model`: 5 (7%)
- `refused-empty-enter`: 3 (4%)
- `done-rejected`: 1 (1%)
- `stale`: 1 (1%)

low-confidence decisions (< τ): 3
