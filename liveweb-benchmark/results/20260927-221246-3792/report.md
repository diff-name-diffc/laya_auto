# liveweb-benchmark report

- generated: `2026-09-27T22:19:56+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 7.2, mean duration 24.3s, decision p50/p95 578.2/675.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 7.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-bac04606ffe5875a` | bot-challenge | ❌ | ❌ | 6 | 47 | bot_challenge |
| `gen-7d4a477b73df0dd1` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-6ce30528850a760c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a5122384d19de494` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |
| `gen-a73244507ac1a399` | done | ✅ | ✅ | 13 | 19 |  |
| `gen-7d42c37e3ef78c22` | done | ✅ | ✅ | 11 | 19 |  |
| `gen-656aff8e27481c3c` | done | ✅ | ✅ | 8 | 12 |  |
| `gen-651f8ce4dac490bc` | done | ❌ | ❌ | 13 | 50 | missing evidence: [['debugging', 'memory']] |

## Step outcomes

- `executed`: 37 (64%)
- `stale`: 7 (12%)
- `done-rejected`: 7 (12%)
- `done`: 4 (7%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)
- `refused-empty-enter`: 1 (2%)

low-confidence decisions (< τ): 5
