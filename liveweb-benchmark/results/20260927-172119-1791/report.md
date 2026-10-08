# liveweb-benchmark report

- generated: `2026-09-27T17:24:28+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 7.1, mean duration 16.6s, decision p50/p95 561.9/836.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 12.0 |
| google | 7 | 86% | 86% | 6.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-d35c0faab76bfa3f` | done | ❌ | ❌ | 12 | 51 | url lacks 'github.com/search' |
| `gen-5d1c185b2ef8a3ac` | done | ✅ | ✅ | 16 | 32 |  |
| `gen-f31eef3355d3f177` | done | ✅ | ✅ | 7 | 13 |  |
| `gen-251978efb3820e87` | done | ❌ | ❌ | 8 | 15 | url lacks 'q=generation' |
| `gen-335c6c0c6ba59834` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-7b85235385af06f3` | done | ✅ | ✅ | 4 | 6 |  |
| `gen-d317d8fb0f75856a` | done | ✅ | ✅ | 4 | 8 |  |
| `gen-8986b55a8f6f7d45` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 39 (68%)
- `done`: 8 (14%)
- `done-rejected`: 5 (9%)
- `stale`: 3 (5%)
- `refused-empty-enter`: 2 (4%)

low-confidence decisions (< τ): 3
