# liveweb-benchmark report

- generated: `2026-09-27T18:22:09+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 6.0, mean duration 25.3s, decision p50/p95 481.6/624.8 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 10.0 |
| google | 7 | 57% | 57% | 5.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-9ac56f173232b08e` | repeat-loop | ❌ | ❌ | 11 | 57 | missing evidence: [['quantization', 'model']] |
| `gen-bd0d7e67b14cc539` | done | ❌ | ❌ | 10 | 52 | missing evidence: [['python']] |
| `gen-da78ec6d50b938ed` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-71020c29008a61b8` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-9bb7a0ab3b20bb71` | done | ✅ | ✅ | 10 | 45 |  |
| `gen-278d56df93e623ef` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-12c5017c6eee394a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-fcc8552be97857a5` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 32 (67%)
- `done-rejected`: 5 (10%)
- `done`: 5 (10%)
- `stale`: 3 (6%)
- `refused-empty-enter`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 5
