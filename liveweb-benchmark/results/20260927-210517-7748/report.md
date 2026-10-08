# liveweb-benchmark report

- generated: `2026-09-27T21:11:56+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 15.5, mean duration 42.5s, decision p50/p95 593.0/859.3 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 25% | 15.5 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-cc35918ecd92771f` | done | ✅ | ✅ | 14 | 22 |  |
| `gen-1c2b145001b3c665` | repeat-loop | ❌ | ❌ | 15 | 62 | url lacks 'q=patterns' |
| `gen-a8e5e3dd71b49234` | done | ❌ | ❌ | 18 | 29 | missing evidence: [['fine-tuning']] |
| `gen-b8070b2c95eccb96` | repeat-loop | ❌ | ❌ | 29 | 46 | missing evidence: [['redis']] |
| `gen-5fe21d4427f5a930` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-1fc94506999eedf2` | done | ❌ | ❌ | 11 | 64 | missing evidence: [['quantization', 'model']] |
| `gen-61617afc570d1245` | done | ❌ | ❌ | 19 | 37 | url lacks 'google.com/search' |
| `gen-04777c4d9d290545` | done | ❌ | ❌ | 15 | 77 | url lacks 'q=review' |

## Step outcomes

- `executed`: 89 (72%)
- `stale`: 14 (11%)
- `done-rejected`: 7 (6%)
- `done`: 6 (5%)
- `refused-empty-enter`: 5 (4%)
- `page changed since the decision (url or marker mismatch)`: 3 (2%)

low-confidence decisions (< τ): 11
