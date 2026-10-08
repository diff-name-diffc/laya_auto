# liveweb-benchmark report

- generated: `2026-09-27T18:15:32+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **2/8** (25%) — DONE **and** independently verified
- independently verified **2/8** (25%)
- found-but-never-stopped: **0**
- mean steps 4.8, mean duration 17.2s, decision p50/p95 549.4/849.2 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 1 | 0% | 0% | 9.0 |
| google | 7 | 29% | 29% | 4.1 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-c5581f6319abe52e` | done | ❌ | ❌ | 7 | 10 | bot_challenge |
| `gen-f2d9ddee6f922db9` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-dc37754b237a4405` | done | ✅ | ✅ | 11 | 24 |  |
| `gen-555bb7bc1c5460c6` | done | ✅ | ✅ | 3 | 4 |  |
| `gen-acbd0595fee1b665` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-93d92fb27785f7e1` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-c8a37cfde3819c9b` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-dfb33ee2bdb53058` | done | ❌ | ❌ | 9 | 41 | missing evidence: [['elasticsearch']] |

## Step outcomes

- `executed`: 25 (66%)
- `done-rejected`: 5 (13%)
- `done`: 4 (11%)
- `refused-empty-enter`: 2 (5%)
- `stale`: 1 (3%)
- `page changed since the decision (url or marker mismatch)`: 1 (3%)

low-confidence decisions (< τ): 2
