# liveweb-benchmark report

- generated: `2026-09-27T18:56:37+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 5.9, mean duration 19.2s, decision p50/p95 502.4/655.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 50% | 50% | 9.0 |
| google | 6 | 33% | 33% | 4.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-0ed0477f8221c733` | done | ❌ | ❌ | 10 | 15 | missing evidence: [['logging']] |
| `gen-1f190ede0b6dcc85` | bot-challenge | ❌ | ❌ | 6 | 48 | bot_challenge |
| `gen-bb5a1a0c01b0822b` | done | ✅ | ✅ | 8 | 13 |  |
| `gen-48748e25a81e5864` | done | ✅ | ✅ | 7 | 10 |  |
| `gen-0d7a5ce46dee9d24` | done | ✅ | ✅ | 9 | 20 |  |
| `gen-938701444e018d1d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-0768438bc026bc54` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d5470d30aa2b6040` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |

## Step outcomes

- `executed`: 27 (57%)
- `done-rejected`: 10 (21%)
- `done`: 4 (9%)
- `refused-empty-enter`: 3 (6%)
- `stale`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 1
