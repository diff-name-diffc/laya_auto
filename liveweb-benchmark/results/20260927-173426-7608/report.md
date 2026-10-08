# liveweb-benchmark report

- generated: `2026-09-27T17:40:14+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **5/8** (62%)
- found-but-never-stopped: **1**
- mean steps 16.2, mean duration 36.6s, decision p50/p95 591.1/749.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 100% | 100% | 8.0 |
| google | 7 | 43% | 57% | 17.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-f12d3431f33cf014` | repeat-loop | ❌ | ❌ | 28 | 72 | missing evidence: [['pytorch']] |
| `gen-caadecf707b968d6` | done | ✅ | ✅ | 8 | 17 |  |
| `gen-04269cc5b5f3a34e` | done | ✅ | ✅ | 7 | 11 |  |
| `gen-62742204f09796ea` | done | ❌ | ❌ | 15 | 42 | url lacks 'pytorch.org' |
| `gen-116806d17d45895f` | done | ✅ | ✅ | 23 | 44 |  |
| `gen-a646d7023722f1c2` | done | ✅ | ✅ | 7 | 12 |  |
| `gen-b7401253312c7789` | max-steps | ❌ | ❌ | 28 | 35 | url lacks 'q=nginx' |
| `gen-05a0d6c68b402ef4` | repeat-loop | ✅ | ❌ | 14 | 59 | TYPE_TEXT on the same target repeats without progress; stopp |

## Step outcomes

- `executed`: 81 (62%)
- `stale`: 25 (19%)
- `done-rejected`: 11 (8%)
- `done`: 5 (4%)
- `page changed since the decision (url or marker mismatch)`: 5 (4%)
- `refused-empty-enter`: 3 (2%)

low-confidence decisions (< τ): 18
