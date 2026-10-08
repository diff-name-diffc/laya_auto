# liveweb-benchmark report

- generated: `2026-09-27T20:09:40+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 4.4, mean duration 23.0s, decision p50/p95 478.5/600.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 4.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-6f66fb596e6b6eca` | repeat-loop | ❌ | ❌ | 16 | 70 | missing evidence: [['refactoring']] |
| `gen-5cbcbd6c10026b44` | bot-challenge | ❌ | ❌ | 5 | 18 | bot_challenge |
| `gen-80af10ecbb341d03` | bot-challenge | ❌ | ❌ | 3 | 18 | bot_challenge |
| `gen-0f5394ffadba57ed` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-edf47b0c9de30e57` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-ec2fdd7e484317b3` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-4f4c6d7109f187f3` | bot-challenge | ❌ | ❌ | 3 | 18 | bot_challenge |
| `gen-8116461d112c66b1` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 26 (74%)
- `stale`: 5 (14%)
- `refused-empty-enter`: 2 (6%)
- `done-rejected`: 2 (6%)

low-confidence decisions (< τ): 0
