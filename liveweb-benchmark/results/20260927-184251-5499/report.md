# liveweb-benchmark report

- generated: `2026-09-27T18:47:53+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 4.5, mean duration 14.0s, decision p50/p95 581.4/871.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 50% | 50% | 4.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-0b889c2647a9f13b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f2d3aa666023e26c` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-d36e8982869743cc` | done | ✅ | ✅ | 6 | 13 |  |
| `gen-e8434249e08eb00b` | done | ✅ | ✅ | 4 | 7 |  |
| `gen-b9a4ad203f954156` | done | ✅ | ✅ | 10 | 14 |  |
| `gen-1025241e1fe6bdcc` | bot-challenge | ❌ | ❌ | 2 | 16 | bot_challenge |
| `gen-805b9a04d4d70a3b` | bot-challenge | ❌ | ❌ | 3 | 21 | bot_challenge |
| `gen-c5a00b1e747edadb` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 23 (64%)
- `done-rejected`: 5 (14%)
- `done`: 4 (11%)
- `stale`: 3 (8%)
- `refused-empty-enter`: 1 (3%)

low-confidence decisions (< τ): 2
