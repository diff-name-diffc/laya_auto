# liveweb-benchmark report

- generated: `2026-09-27T18:31:59+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **1**
- mean steps 8.9, mean duration 25.0s, decision p50/p95 582.6/690.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 50% | 8.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-dfa2fa10300a0ddc` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-7712aa9b2ddde46f` | done | ✅ | ✅ | 7 | 13 |  |
| `gen-37d060a6d153c85b` | done | ✅ | ✅ | 10 | 18 |  |
| `gen-bd046bd739351fc0` | done | ❌ | ❌ | 17 | 71 | url lacks 'q=express' |
| `gen-4cabaf8f2df27ed3` | repeat-loop | ✅ | ❌ | 28 | 49 | TYPE_TEXT on the same target repeats without progress; stopp |
| `gen-352b3b974423eb85` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-b954fa3007b8a5e2` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-e091b00daaba088a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 48 (68%)
- `stale`: 7 (10%)
- `done-rejected`: 7 (10%)
- `done`: 4 (6%)
- `page changed since the decision (url or marker mismatch)`: 4 (6%)
- `refused-empty-enter`: 1 (1%)

low-confidence decisions (< τ): 1
