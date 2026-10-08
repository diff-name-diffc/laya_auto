# liveweb-benchmark report

- generated: `2026-09-27T23:26:38+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **4/8** (50%) — DONE **and** independently verified
- independently verified **4/8** (50%)
- found-but-never-stopped: **0**
- mean steps 8.4, mean duration 21.7s, decision p50/p95 591.9/665.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 50% | 50% | 8.4 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-2c23aef7bc443a6d` | repeat-loop | ❌ | ❌ | 11 | 68 | missing evidence: [['react']] |
| `gen-308be1a0f3e993f1` | done | ❌ | ❌ | 4 | 12 | url lacks 'q=kafka' |
| `gen-6405b67a97a217ee` | done | ✅ | ✅ | 15 | 27 |  |
| `gen-acce1ee641937548` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-dca0a3ec2a470754` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-a45ee4a046088640` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-61e44f221e6592c7` | repeat-loop | ❌ | ❌ | 26 | 40 | missing evidence: [['refactoring']] |
| `gen-d4adc558a3868d8f` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |

## Step outcomes

- `executed`: 53 (79%)
- `stale`: 6 (9%)
- `done`: 5 (7%)
- `done-rejected`: 2 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (1%)

low-confidence decisions (< τ): 6
