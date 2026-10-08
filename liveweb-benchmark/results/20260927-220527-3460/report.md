# liveweb-benchmark report

- generated: `2026-09-27T22:12:16+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **0**
- mean steps 9.8, mean duration 27.4s, decision p50/p95 581.7/709.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 38% | 9.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-aa6aaee535253d88` | done | ✅ | ✅ | 8 | 28 |  |
| `gen-a376de27758d520c` | done | ✅ | ✅ | 15 | 33 |  |
| `gen-c0470234fd372bc8` | done | ❌ | ❌ | 9 | 16 | url lacks 'q=generation' |
| `gen-da2d7260967926b8` | done | ✅ | ✅ | 5 | 16 |  |
| `gen-65461d28f8b3a662` | bot-challenge | ❌ | ❌ | 27 | 72 | bot_challenge |
| `gen-98ebd20e5ebffec7` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-3a6acc7904d71719` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a42e41feb322b7b2` | done | ❌ | ❌ | 10 | 26 | url lacks 'q=quantization' |

## Step outcomes

- `executed`: 54 (69%)
- `stale`: 9 (12%)
- `done`: 5 (6%)
- `done-rejected`: 5 (6%)
- `page changed since the decision (url or marker mismatch)`: 5 (6%)

low-confidence decisions (< τ): 9
