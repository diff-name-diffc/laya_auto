# liveweb-benchmark report

- generated: `2026-09-27T19:48:56+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 3.8, mean duration 17.0s, decision p50/p95 518.2/692.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 3.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-9ff2d9af244ae8de` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-39e976b48b85b51c` | done | ❌ | ❌ | 8 | 16 | missing evidence: [['scala']] |
| `gen-6475de4f090edae6` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-5b6e25a17ee4768a` | bot-challenge | ❌ | ❌ | 6 | 24 | bot_challenge |
| `gen-2b665e6c92bd4316` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-3aba1f2f72a1789c` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-36cd5c6b9c88db55` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-9f0a75788e29659a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 18 (60%)
- `done-rejected`: 6 (20%)
- `refused-empty-enter`: 3 (10%)
- `stale`: 2 (7%)
- `done`: 1 (3%)

low-confidence decisions (< τ): 2
