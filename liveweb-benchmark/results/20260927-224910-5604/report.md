# liveweb-benchmark report

- generated: `2026-09-27T22:54:49+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 12.1, mean duration 29.7s, decision p50/p95 591.3/724.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 12.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-b20ae4a5f524fed0` | done | ❌ | ❌ | 3 | 6 | url lacks 'q=patterns' |
| `gen-9f4e0e58b88e4ff6` | repeat-loop | ❌ | ❌ | 26 | 69 | missing evidence: [['pipelines', 'ci/cd']] |
| `gen-28e0ed168ed43b3d` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-674d73906afeb5ff` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-3351451937da3ed0` | done | ❌ | ❌ | 8 | 58 | missing evidence: [['vue']] |
| `gen-12a3df1dd1524c48` | max-steps | ❌ | ❌ | 29 | 51 | missing evidence: [['kotlin']] |
| `gen-9a6c8475b1c54f0d` | done | ✅ | ✅ | 15 | 20 |  |
| `gen-581c17303fb1c735` | done | ✅ | ✅ | 11 | 16 |  |

## Step outcomes

- `executed`: 72 (74%)
- `stale`: 12 (12%)
- `done`: 5 (5%)
- `done-rejected`: 4 (4%)
- `page changed since the decision (url or marker mismatch)`: 4 (4%)

low-confidence decisions (< τ): 7
