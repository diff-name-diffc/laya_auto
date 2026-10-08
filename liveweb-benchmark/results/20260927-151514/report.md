# liveweb-benchmark report

- generated: `2026-09-27T15:21:58+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **6/12** (50%) — DONE **and** independently verified
- independently verified **6/12** (50%)
- found-but-never-stopped: **0**
- mean steps 10.4, mean duration 22.7s, decision p50/p95 572.4/638.4 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 2 | 0% | 0% | 19.0 |
| google | 10 | 60% | 60% | 8.7 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-3ad51873f9592959` | bot-challenge | ❌ | ❌ | 6 | 28 | bot_challenge |
| `gen-6ad4190999ef773b` | done | ✅ | ✅ | 7 | 9 |  |
| `gen-7817918cb27eff6d` | done | ❌ | ❌ | 11 | 17 | url lacks 'q=generation' |
| `gen-6b25c21c5f22801d` | done | ❌ | ❌ | 27 | 49 | url lacks 'github.com/search' |
| `gen-5c29e34a779a1536` | done | ✅ | ✅ | 18 | 22 |  |
| `gen-94d7f1a0cc9183fc` | done | ✅ | ✅ | 12 | 15 |  |
| `gen-791146603b5ee52b` | unstable-page | ❌ | ❌ | 8 | 6 | missing evidence: [['kubernetes']] |
| `gen-0f1eb30367c58a0b` | done | ✅ | ✅ | 6 | 8 |  |
| `gen-d6ee8afe9eafa77f` | done | ❌ | ❌ | 8 | 24 | url lacks 'q=generation' |
| `gen-ab47777cd95cfe4d` | done | ✅ | ✅ | 8 | 16 |  |
| `gen-f3fc051023ea05ad` | done | ✅ | ✅ | 3 | 5 |  |
| `gen-9bfc342fbcfb9dcf` | done | ❌ | ❌ | 11 | 73 | url lacks 'github.com/search' |

## Step outcomes

- `executed`: 81 (65%)
- `stale`: 18 (14%)
- `done-rejected`: 11 (9%)
- `done`: 10 (8%)
- `page changed since the decision (url or marker mismatch)`: 3 (2%)
- `refused-empty-enter`: 2 (2%)

low-confidence decisions (< τ): 14
