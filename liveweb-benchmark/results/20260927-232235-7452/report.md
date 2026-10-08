# liveweb-benchmark report

- generated: `2026-09-27T23:30:13+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **1**
- mean steps 7.2, mean duration 22.3s, decision p50/p95 560.3/632.6 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 25% | 7.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-b962790f577c139a` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-7d1c9279890cbc14` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-a434b51370058c31` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-8e92b0e904eec887` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-2200101f6fea06e9` | repeat-loop | ✅ | ❌ | 27 | 42 | TYPE_TEXT on the same target repeats without progress; stopp |
| `gen-b72f6db15cc7ebf0` | done | ✅ | ✅ | 4 | 9 |  |
| `gen-bdcb4e93ed552904` | bot-challenge | ❌ | ❌ | 10 | 49 | url lacks 'q=rabbitmq' |
| `gen-7deb4558692a52ec` | unstable-page | ❌ | ❌ | 9 | 19 | missing evidence: [['express']] |

## Step outcomes

- `executed`: 42 (72%)
- `stale`: 10 (17%)
- `done-rejected`: 3 (5%)
- `page changed since the decision (url or marker mismatch)`: 2 (3%)
- `done`: 1 (2%)

low-confidence decisions (< τ): 5
