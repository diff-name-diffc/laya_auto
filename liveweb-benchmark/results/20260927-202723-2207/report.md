# liveweb-benchmark report

- generated: `2026-09-27T20:34:45+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **0/8** (0%) — DONE **and** independently verified
- independently verified **0/8** (0%)
- found-but-never-stopped: **0**
- mean steps 3.6, mean duration 14.7s, decision p50/p95 530.0/617.0 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 0% | 0% | 3.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-074964ec200f07c9` | bot-challenge | ❌ | ❌ | 8 | 21 | bot_challenge |
| `gen-affc160c74f74936` | bot-challenge | ❌ | ❌ | 5 | 19 | bot_challenge |
| `gen-e4ea4f72402048dd` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-6156092d67e653c8` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-408bd0b24dfd42a5` | unstable-page | ❌ | ❌ | 6 | 4 | missing evidence: [['flask']] |
| `gen-e859256c615d01f0` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-9925b805b878c644` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-7296c6e0c399477e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 20 (69%)
- `stale`: 6 (21%)
- `refused-empty-enter`: 3 (10%)

low-confidence decisions (< τ): 5
