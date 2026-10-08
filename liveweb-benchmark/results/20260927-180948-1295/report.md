# liveweb-benchmark report

- generated: `2026-09-27T18:16:20+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 10.4, mean duration 25.1s, decision p50/p95 488.9/663.1 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| github | 3 | 33% | 33% | 16.3 |
| google | 5 | 0% | 0% | 6.8 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-92e650d40ee67e41` | bot-challenge | ❌ | ❌ | 6 | 22 | bot_challenge |
| `gen-c60bbe2e7826f562` | done | ❌ | ❌ | 14 | 37 | missing evidence: [['vllm']] |
| `gen-694e1a61e3cef1fc` | done | ❌ | ❌ | 16 | 44 | url lacks 'github.com/search' |
| `gen-30dcc53e457ef35d` | done | ❌ | ❌ | 8 | 14 | missing evidence: [['golang']] |
| `gen-f24dc1050db8b696` | done | ✅ | ✅ | 11 | 15 |  |
| `gen-e3e1c2618ecfd619` | bot-challenge | ❌ | ❌ | 3 | 19 | bot_challenge |
| `gen-ca40b2b4126c914c` | bot-challenge | ❌ | ❌ | 3 | 21 | bot_challenge |
| `gen-c13761f2855f63f2` | done | ❌ | ❌ | 22 | 31 | missing evidence: [['react']] |

## Step outcomes

- `executed`: 52 (63%)
- `done-rejected`: 13 (16%)
- `refused-empty-enter`: 5 (6%)
- `page changed since the decision (url or marker mismatch)`: 5 (6%)
- `done`: 5 (6%)
- `stale`: 3 (4%)

low-confidence decisions (< τ): 7
