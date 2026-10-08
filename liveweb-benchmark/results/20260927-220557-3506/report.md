# liveweb-benchmark report

- generated: `2026-09-27T22:10:13+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 9.0, mean duration 19.5s, decision p50/p95 582.2/694.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 50% | 50% | 9.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-194046cd09c88747` | bot-challenge | ❌ | ❌ | 3 | 16 | bot_challenge |
| `gen-cebeafe88b2a8a3b` | done | ❌ | ❌ | 5 | 35 | url lacks 'q=ruby' |
| `gen-fc3efaf31d715695` | done | ✅ | ✅ | 7 | 13 |  |
| `gen-9977c05ad29ee8f3` | done | ✅ | ✅ | 10 | 26 |  |
| `gen-7a938b3970639824` | done | ❌ | ❌ | 12 | 14 | url lacks 'q=programming' |
| `gen-7985c2e3df6c691e` | done | ❌ | ❌ | 11 | 18 | url lacks 'q=review' |
| `gen-04d3967b1a65d7ee` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-827c80930c42562e` | done | ✅ | ✅ | 21 | 30 |  |

## Step outcomes

- `executed`: 50 (69%)
- `stale`: 8 (11%)
- `done`: 7 (10%)
- `done-rejected`: 4 (6%)
- `refused-empty-enter`: 1 (1%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)
- `failed`: 1 (1%)

low-confidence decisions (< τ): 13
