# liveweb-benchmark report

- generated: `2026-09-27T21:45:58+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 6.1, mean duration 18.6s, decision p50/p95 503.3/614.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 6.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-12052e646b5de6e7` | max-steps | ❌ | ❌ | 27 | 38 | missing evidence: [['review', 'code']] |
| `gen-26ced3683a72331e` | done | ❌ | ❌ | 10 | 22 | url lacks 'q=transformers' |
| `gen-88eadedcdb3999a2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-4a46f5dfacd6fc6f` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-5264406a6a7de17e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d6e3171be2cc690c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-559d63a2cf065c19` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d9d1898e749c0495` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 37 (76%)
- `stale`: 9 (18%)
- `refused-empty-enter`: 1 (2%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)
- `done`: 1 (2%)

low-confidence decisions (< τ): 0
