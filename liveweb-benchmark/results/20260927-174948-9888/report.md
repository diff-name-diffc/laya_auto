# liveweb-benchmark report

- generated: `2026-09-27T17:54:06+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **3/8** (38%)
- found-but-never-stopped: **1**
- mean steps 10.9, mean duration 19.9s, decision p50/p95 580.2/885.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 25% | 38% | 10.9 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-5a10c093f01fb140` | bot-challenge | ❌ | ❌ | 4 | 16 | bot_challenge |
| `gen-37ba2416b8fa23dc` | repeat-loop | ✅ | ❌ | 28 | 52 | TYPE_TEXT on the same target repeats without progress; stopp |
| `gen-c9e27abcf19850a0` | done | ❌ | ❌ | 9 | 12 | url lacks 'q=generation' |
| `gen-a6482f3750ef2ba4` | done | ✅ | ✅ | 8 | 13 |  |
| `gen-9284a4b71afd3483` | done | ❌ | ❌ | 19 | 31 | url lacks 'q=testing' |
| `gen-bae5c354481093cd` | done | ✅ | ✅ | 5 | 6 |  |
| `gen-9a50e7527fd1349d` | done | ❌ | ❌ | 8 | 16 | missing evidence: [['react']] |
| `gen-01e52a20fc347f5e` | done | ❌ | ❌ | 6 | 12 | missing evidence: [['react']] |

## Step outcomes

- `executed`: 58 (67%)
- `stale`: 12 (14%)
- `done`: 6 (7%)
- `done-rejected`: 6 (7%)
- `page changed since the decision (url or marker mismatch)`: 4 (5%)
- `refused-empty-enter`: 1 (1%)

low-confidence decisions (< τ): 6
