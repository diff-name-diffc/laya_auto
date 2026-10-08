# liveweb-benchmark report

- generated: `2026-09-27T19:18:00+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 4.5, mean duration 15.5s, decision p50/p95 566.5/810.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 4.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-3050997548dc6036` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-55a1a495b131f894` | done | ✅ | ✅ | 8 | 13 |  |
| `gen-d2ddaf9377c2339a` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-e15eb2f7de4f896f` | bot-challenge | ❌ | ❌ | 11 | 24 | bot_challenge |
| `gen-9b00613a9229e5bf` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-d205916b94069652` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-1b55d6d2b691e47e` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a39ffa65663726df` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 20 (56%)
- `stale`: 7 (19%)
- `done-rejected`: 4 (11%)
- `refused-empty-enter`: 2 (6%)
- `done`: 2 (6%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 2
