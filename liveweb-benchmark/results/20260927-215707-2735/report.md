# liveweb-benchmark report

- generated: `2026-09-27T22:02:38+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 7.1, mean duration 17.6s, decision p50/p95 574.4/815.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 50% | 50% | 7.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-9fbcf8f8de31420d` | done | ✅ | ✅ | 8 | 25 |  |
| `gen-7cad69e62d7917a6` | done | ✅ | ✅ | 10 | 22 |  |
| `gen-7dbf508a573102e9` | bot-challenge | ❌ | ❌ | 6 | 19 | missing evidence: [['elasticsearch']] |
| `gen-d13fd540de1300c7` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-2a6827dda171cd7b` | bot-challenge | ❌ | ❌ | 10 | 27 | missing evidence: [['review', 'code']] |
| `gen-acc77151de83e32a` | bot-challenge | ❌ | ❌ | 6 | 19 | missing evidence: [['terraform']] |
| `gen-152de739a4cb97b8` | done | ❌ | ❌ | 3 | 5 | url lacks 'q=concurrency' |
| `gen-aaa4b4488f6eba98` | done | ✅ | ✅ | 11 | 20 |  |

## Step outcomes

- `executed`: 38 (67%)
- `stale`: 8 (14%)
- `done`: 5 (9%)
- `done-rejected`: 3 (5%)
- `page changed since the decision (url or marker mismatch)`: 3 (5%)

low-confidence decisions (< τ): 4
