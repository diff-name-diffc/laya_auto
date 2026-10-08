# liveweb-benchmark report

- generated: `2026-09-27T22:11:52+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 2.6, mean duration 11.3s, decision p50/p95 517.3/607.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 2.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-eb88b870bb1eaace` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-6f02373584f501c1` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f306ddb5eb481dad` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-8494b7a598c93ec2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-34caef74d7c9f8a3` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d742227f9b3a33a5` | done | ✅ | ✅ | 5 | 8 |  |
| `gen-be22026c79fdb9a6` | done | ❌ | ❌ | 3 | 4 | url lacks 'q=pytorch' |
| `gen-0120fc9d9c3e335a` | done | ✅ | ✅ | 3 | 5 |  |

## Step outcomes

- `executed`: 16 (76%)
- `done`: 3 (14%)
- `refused-empty-enter`: 1 (5%)
- `done-rejected`: 1 (5%)

low-confidence decisions (< τ): 2
