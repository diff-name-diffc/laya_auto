# liveweb-benchmark report

- generated: `2026-09-27T20:17:36+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **0**
- mean steps 6.4, mean duration 31.4s, decision p50/p95 585.2/722.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 62% | 62% | 6.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-41d3dfc4f1e22bd0` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-d357ec4543fc8a1c` | bot-challenge | ❌ | ❌ | 6 | 23 | bot_challenge |
| `gen-f2462aae6c4deba2` | bot-challenge | ❌ | ❌ | 3 | 41 | bot_challenge |
| `gen-def077559968238a` | done | ✅ | ✅ | 6 | 26 |  |
| `gen-d4c4174668bed9d9` | done | ✅ | ✅ | 4 | 51 |  |
| `gen-0a258a72292c685e` | done | ✅ | ✅ | 5 | 12 |  |
| `gen-80688c1dd10cd4d2` | done | ✅ | ✅ | 8 | 11 |  |
| `gen-d2365fc90a7a5c95` | done | ✅ | ✅ | 13 | 66 |  |

## Step outcomes

- `executed`: 27 (53%)
- `done-rejected`: 9 (18%)
- `stale`: 7 (14%)
- `done`: 5 (10%)
- `refused-empty-enter`: 2 (4%)
- `page changed since the decision (url or marker mismatch)`: 1 (2%)

low-confidence decisions (< τ): 1
