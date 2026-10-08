# liveweb-benchmark report

- generated: `2026-09-27T21:03:29+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 3.5, mean duration 16.7s, decision p50/p95 497.8/607.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 11.0 |
| google | 7 | 0% | 0% | 2.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-95603a51670a9dfb` | done | ❌ | ❌ | 11 | 19 | missing evidence: [['pytorch']] |
| `gen-9f94f409f1da9c4b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f169906c3c833aa8` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-737778dd443a7240` | bot-challenge | ❌ | ❌ | 5 | 26 | bot_challenge |
| `gen-9ded7f96e6721616` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-6e22f5cd9ebcbcf9` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-67bbc7523c31c512` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-9a078659f5d92679` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 20 (71%)
- `done-rejected`: 4 (14%)
- `stale`: 1 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (4%)
- `done`: 1 (4%)
- `refused-empty-enter`: 1 (4%)

low-confidence decisions (< τ): 1
