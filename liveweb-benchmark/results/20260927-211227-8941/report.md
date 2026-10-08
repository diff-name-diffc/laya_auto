# liveweb-benchmark report

- generated: `2026-09-27T21:19:47+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 5.6, mean duration 20.0s, decision p50/p95 569.5/708.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 12% | 5.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-4ff9f134c45acc9f` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-3dcec38164160cea` | repeat-loop | ❌ | ❌ | 20 | 36 | missing evidence: [['redis']] |
| `gen-d124b226469124f6` | bot-challenge | ❌ | ❌ | 4 | 31 | bot_challenge |
| `gen-85377f67e34c6f94` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-dc95623f43895f1a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-88b599e0f9c049a7` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-81e3ff76750d4e9e` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-d8749e6191b27fc3` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 30 (67%)
- `done-rejected`: 7 (16%)
- `refused-empty-enter`: 4 (9%)
- `stale`: 2 (4%)
- `done`: 1 (2%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 10
