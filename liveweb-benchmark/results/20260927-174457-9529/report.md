# liveweb-benchmark report

- generated: `2026-09-27T17:49:32+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/8** (75%) — DONE **and** independently verified
- independently verified **6/8** (75%)
- found-but-never-stopped: **0**
- mean steps 9.8, mean duration 27.4s, decision p50/p95 572.3/655.7 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 8.0 |
| google | 7 | 86% | 86% | 10.0 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-ed89d08990d322e2` | done | ✅ | ✅ | 25 | 99 |  |
| `gen-c4720f06f8e239f2` | done | ✅ | ✅ | 18 | 44 |  |
| `gen-a0201968a064a874` | done | ✅ | ✅ | 5 | 9 |  |
| `gen-e3dd9245c5ef8c6e` | done | ✅ | ✅ | 4 | 5 |  |
| `gen-fae5d0ba69a30529` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-fb50a9f3cb817cca` | done | ❌ | ❌ | 8 | 33 | missing evidence: [['docker']] |
| `gen-3163e12459beeeb2` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-035a884b54c66fb1` | done | ❌ | ❌ | 12 | 20 | url lacks 'q=review' |

## Step outcomes

- `executed`: 47 (60%)
- `stale`: 8 (10%)
- `done`: 8 (10%)
- `done-rejected`: 7 (9%)
- `page changed since the decision (url or marker mismatch)`: 5 (6%)
- `refused-empty-enter`: 3 (4%)

low-confidence decisions (< τ): 10
