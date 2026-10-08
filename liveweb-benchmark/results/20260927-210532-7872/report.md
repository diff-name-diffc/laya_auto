# liveweb-benchmark report

- generated: `2026-09-27T21:08:55+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **7/8** (88%) — DONE **and** independently verified
- independently verified **7/8** (88%)
- found-but-never-stopped: **0**
- mean steps 10.6, mean duration 17.9s, decision p50/p95 593.4/943.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 88% | 88% | 10.6 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-f9be650fca8b2c96` | done | ✅ | ✅ | 12 | 20 |  |
| `gen-0d259d3988a45061` | done | ✅ | ✅ | 7 | 9 |  |
| `gen-0655e75b2dab5077` | done | ✅ | ✅ | 23 | 42 |  |
| `gen-17b80a9059eee159` | done | ✅ | ✅ | 10 | 15 |  |
| `gen-10791cabf93d8c6e` | done | ✅ | ✅ | 13 | 19 |  |
| `gen-272bf0f150aa730d` | done | ✅ | ✅ | 7 | 13 |  |
| `gen-3ec98674c8497ab9` | done | ❌ | ❌ | 10 | 21 | url lacks 'q=fine-tuning' |
| `gen-267c429567229861` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 53 (62%)
- `stale`: 15 (18%)
- `done`: 8 (9%)
- `done-rejected`: 6 (7%)
- `refused-empty-enter`: 2 (2%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 11
