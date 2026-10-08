# liveweb-benchmark report

- generated: `2026-09-27T19:24:29+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 4.9, mean duration 15.6s, decision p50/p95 529.0/910.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 4.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-852f65d8831c2989` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-48f11f743062fd73` | done | ✅ | ✅ | 7 | 13 |  |
| `gen-03f9c43c5d730cf3` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-65e1d3afcdf232e8` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-f9c06fabfbe72095` | bot-challenge | ❌ | ❌ | 10 | 28 | bot_challenge |
| `gen-da855f832684f616` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-2adf838c6a60ec75` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-3955e080b75d3ab2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 22 (56%)
- `done-rejected`: 7 (18%)
- `stale`: 3 (8%)
- `refused-empty-enter`: 3 (8%)
- `done`: 3 (8%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 5
