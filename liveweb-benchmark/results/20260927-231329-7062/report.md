# liveweb-benchmark report

- generated: `2026-09-27T23:20:43+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 7.0, mean duration 24.9s, decision p50/p95 573.4/687.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 12% | 7.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-47edc1376cef2ae4` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d8a2892cdde1c1ac` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-2e3ee880abd97996` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-2444599a24c1abe2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-5bd83bf9d16bfccc` | unstable-page | ❌ | ❌ | 8 | 6 | missing evidence: [['scala']] |
| `gen-898d1ef22b0cdfc5` | repeat-loop | ❌ | ❌ | 26 | 45 | missing evidence: [['kotlin']] |
| `gen-b886afc193b970d8` | done | ❌ | ❌ | 10 | 76 | url lacks 'q=kubernetes' |
| `gen-10ddfe5d4f66d3de` | done | ✅ | ✅ | 4 | 12 |  |

## Step outcomes

- `executed`: 41 (73%)
- `stale`: 9 (16%)
- `done-rejected`: 3 (5%)
- `done`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 4
