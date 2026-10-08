# liveweb-benchmark report

- generated: `2026-09-27T19:22:44+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 5.4, mean duration 15.5s, decision p50/p95 565.0/845.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 50% | 50% | 5.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-60aa77891145a37f` | bot-challenge | ❌ | ❌ | 6 | 25 | bot_challenge |
| `gen-366f060f29b2c8dc` | done | ✅ | ✅ | 5 | 8 |  |
| `gen-888014e803070f42` | done | ✅ | ✅ | 11 | 15 |  |
| `gen-662bd8394df6ea93` | done | ✅ | ✅ | 4 | 8 |  |
| `gen-306b5d3c76cfc14c` | done | ❌ | ❌ | 10 | 25 | url lacks 'q=quantization' |
| `gen-8d3e441fc2b05a6e` | done | ✅ | ✅ | 3 | 13 |  |
| `gen-26be311429654639` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-eda7f3912eddbbdb` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 27 (63%)
- `done-rejected`: 5 (12%)
- `done`: 5 (12%)
- `stale`: 3 (7%)
- `page changed since the decision (url or marker mismatch)`: 2 (5%)
- `refused-empty-enter`: 1 (2%)

low-confidence decisions (< τ): 2
