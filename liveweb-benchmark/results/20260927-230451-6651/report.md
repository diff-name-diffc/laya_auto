# liveweb-benchmark report

- generated: `2026-09-27T23:12:04+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 11.6, mean duration 35.9s, decision p50/p95 590.1/670.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 11.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-c3f64c1430ef19a1` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-8be40dc8d39d7b59` | done | ✅ | ✅ | 14 | 18 |  |
| `gen-45a2e21709266ca9` | done | ❌ | ❌ | 26 | 37 | missing evidence: [['transformers', 'huggingface']] |
| `gen-77923bc49d20d0c9` | done | ✅ | ✅ | 17 | 26 |  |
| `gen-0de679a9dffccb78` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-9bffec224dbac2db` | done | ❌ | ❌ | 8 | 57 | missing evidence: [['golang']] |
| `gen-fd6a9f84238aa6a7` | repeat-loop | ❌ | ❌ | 12 | 95 | missing evidence: [['express']] |
| `gen-c4529aadda45c2f6` | done | ✅ | ✅ | 8 | 18 |  |

## Step outcomes

- `executed`: 54 (58%)
- `stale`: 19 (20%)
- `done-rejected`: 9 (10%)
- `page changed since the decision (url or marker mismatch)`: 6 (6%)
- `done`: 5 (5%)

low-confidence decisions (< τ): 28
