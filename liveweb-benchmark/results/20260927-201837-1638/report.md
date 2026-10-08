# liveweb-benchmark report

- generated: `2026-09-27T20:27:08+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 6.8, mean duration 23.2s, decision p50/p95 444.9/691.9 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 6.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-3082677319cac4dd` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-9e80abb4d94e0308` | bot-challenge | ❌ | ❌ | 5 | 20 | bot_challenge |
| `gen-31e48d5d432d4862` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-0b17ff9743335177` | bot-challenge | ❌ | ❌ | 3 | 27 | bot_challenge |
| `gen-24a68a4f4ce489a3` | max-steps | ❌ | ❌ | 28 | 46 | missing evidence: [['c++']] |
| `gen-8fdfaf238838b01a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-edc67cb72faeb026` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-847791457126b29d` | bot-challenge | ❌ | ❌ | 6 | 26 | bot_challenge |

## Step outcomes

- `executed`: 35 (65%)
- `done-rejected`: 7 (13%)
- `stale`: 5 (9%)
- `refused-empty-enter`: 5 (9%)
- `page changed since the decision (url or marker mismatch)`: 2 (4%)

low-confidence decisions (< τ): 5
