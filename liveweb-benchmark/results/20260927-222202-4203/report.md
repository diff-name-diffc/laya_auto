# liveweb-benchmark report

- generated: `2026-09-27T22:26:34+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 7.1, mean duration 15.9s, decision p50/p95 568.6/636.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 12% | 7.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-e56db6573baa63a0` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-3214cdec1641afc9` | bot-challenge | ❌ | ❌ | 6 | 18 | bot_challenge |
| `gen-16dda499cf987198` | done | ❌ | ❌ | 7 | 21 | url lacks 'q=review' |
| `gen-1ebddeb04d294971` | done | ❌ | ❌ | 9 | 15 | missing evidence: [['tensorflow']] |
| `gen-9f5f1351e362491d` | done | ❌ | ❌ | 9 | 12 | url lacks 'q=patterns' |
| `gen-517522a7fe3e2f29` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-0b6f5eceb27e5b61` | done | ❌ | ❌ | 11 | 19 | missing evidence: [['generation', 'retrieval']] |
| `gen-766bb0606aa9e235` | done | ❌ | ❌ | 10 | 23 | url lacks 'q=docker' |

## Step outcomes

- `executed`: 29 (51%)
- `done-rejected`: 8 (14%)
- `page changed since the decision (url or marker mismatch)`: 7 (12%)
- `done`: 6 (11%)
- `stale`: 4 (7%)
- `refused-empty-enter`: 3 (5%)

low-confidence decisions (< τ): 15
