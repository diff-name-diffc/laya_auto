# liveweb-benchmark report

- generated: `2026-09-27T19:01:23+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 6.1, mean duration 19.0s, decision p50/p95 540.0/666.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 12.0 |
| google | 7 | 57% | 57% | 5.3 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-3166a55615c9333d` | done | ❌ | ❌ | 12 | 62 | url lacks 'github.com/search' |
| `gen-949eacb8ae3e5518` | bot-challenge | ❌ | ❌ | 5 | 21 | bot_challenge |
| `gen-8e72bbf5663dc7f4` | done | ✅ | ✅ | 7 | 28 |  |
| `gen-f19b302e26c6e946` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-dea80662fdd89894` | done | ❌ | ❌ | 3 | 4 | url lacks 'q=svelte' |
| `gen-d9e96e957546c7e7` | done | ❌ | ❌ | 8 | 18 | missing evidence: [['docker']] |
| `gen-617025dd0b7ba27b` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-9b27edd73a9193e5` | done | ✅ | ✅ | 4 | 5 |  |

## Step outcomes

- `executed`: 27 (55%)
- `done-rejected`: 8 (16%)
- `done`: 7 (14%)
- `refused-empty-enter`: 3 (6%)
- `stale`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 2 (4%)

low-confidence decisions (< τ): 3
