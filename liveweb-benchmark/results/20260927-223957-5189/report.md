# liveweb-benchmark report

- generated: `2026-09-27T22:44:03+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **5/8** (62%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **1**
- mean steps 10.0, mean duration 23.9s, decision p50/p95 588.6/891.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 62% | 75% | 10.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-14d78beef8209fd2` | done | ✅ | ✅ | 10 | 16 |  |
| `gen-a03713f95dc49860` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-0e000ac3a6eb4428` | done | ❌ | ❌ | 3 | 4 | url lacks 'q=review' |
| `gen-b5da94d0d2d239fd` | done | ✅ | ✅ | 12 | 42 |  |
| `gen-d128b7e64ae6b250` | done | ❌ | ❌ | 14 | 28 | url lacks 'q=testing' |
| `gen-7a0f6cee80c7167e` | done | ✅ | ✅ | 13 | 16 |  |
| `gen-796722a4ba8d2ba1` | repeat-loop | ✅ | ❌ | 15 | 62 | TYPE_TEXT on the same target repeats without progress; stopp |
| `gen-756be9b601546bef` | done | ✅ | ✅ | 10 | 18 |  |

## Step outcomes

- `executed`: 54 (68%)
- `stale`: 11 (14%)
- `done`: 7 (9%)
- `page changed since the decision (url or marker mismatch)`: 3 (4%)
- `done-rejected`: 3 (4%)
- `refused-empty-enter`: 2 (2%)

low-confidence decisions (< τ): 13
