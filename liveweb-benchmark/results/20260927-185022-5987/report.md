# liveweb-benchmark report

- generated: `2026-09-27T18:56:55+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 4.6, mean duration 19.7s, decision p50/p95 568.3/653.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 4.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-eb4e9c4bfcd99020` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-31eda903496de357` | done | ✅ | ✅ | 8 | 13 |  |
| `gen-3f35c14e80a8b5a9` | done | ✅ | ✅ | 9 | 12 |  |
| `gen-b17a77740b368285` | done | ❌ | ❌ | 10 | 58 | missing evidence: [['review', 'code']] |
| `gen-a741451e2fb5b7e1` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-5f38fb6d1d6e9b94` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-12a31c5819a7f347` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-1e18d62f8ae3eb77` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 25 (68%)
- `done-rejected`: 4 (11%)
- `stale`: 3 (8%)
- `done`: 3 (8%)
- `refused-empty-enter`: 1 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 1
