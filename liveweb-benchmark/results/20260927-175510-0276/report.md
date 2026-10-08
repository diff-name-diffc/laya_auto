# liveweb-benchmark report

- generated: `2026-09-27T18:00:14+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **3/8** (38%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **1**
- mean steps 11.5, mean duration 25.6s, decision p50/p95 576.0/774.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 38% | 50% | 11.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-b457ce3c079ca065` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-2bffcc2a1aaa9d5d` | repeat-loop | ✅ | ❌ | 21 | 66 | CLICK on the same target repeats without progress; stopping |
| `gen-c248394a623626bf` | done | ❌ | ❌ | 16 | 24 | missing evidence: [['terraform']] |
| `gen-5e29e1bd129e6f01` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-64cf68687ff36a92` | done | ❌ | ❌ | 12 | 21 | url lacks 'google.com/search' |
| `gen-8356d67c5c445880` | done | ✅ | ✅ | 19 | 47 |  |
| `gen-5e030c7e517c8b89` | done | ❌ | ❌ | 8 | 14 | missing evidence: [['prometheus']] |
| `gen-b3f66aacdbb68531` | done | ✅ | ✅ | 11 | 15 |  |

## Step outcomes

- `executed`: 58 (63%)
- `stale`: 14 (15%)
- `done-rejected`: 7 (8%)
- `page changed since the decision (url or marker mismatch)`: 6 (7%)
- `done`: 6 (7%)
- `refused-empty-enter`: 1 (1%)

low-confidence decisions (< τ): 9
