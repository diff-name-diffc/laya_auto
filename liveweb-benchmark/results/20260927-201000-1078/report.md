# liveweb-benchmark report

- generated: `2026-09-27T20:17:52+0800`
- backend: `http://10.144.144.2:8000`
- browser: CloakBrowser `145.0.7632.109.2` (humanize=True, headless=False)
- max_steps=25, delay=6.0s

## Summary

- success **1/8** (12%) — DONE **and** independently verified
- independently verified **1/8** (12%)
- found-but-never-stopped: **0**
- mean steps 3.2, mean duration 18.5s, decision p50/p95 514.5/786.5 ms

## By source

| source | n | success | verified | mean steps |
|---|---|---|---|---|
| google | 8 | 12% | 12% | 3.2 |

## Tasks

| task | status | verified | success | steps | s | fail reason |
|---|---|---|---|---|---|---|
| `gen-668f8c43a5daed30` | bot-challenge | ❌ | ❌ | 7 | 20 | bot_challenge |
| `gen-de1cb35a7218bcb9` | done | ❌ | ❌ | 6 | 51 | missing evidence: [['logging']] |
| `gen-7a49e0a54672f4ce` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-79325271236a2bae` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-c04c17743b673a29` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-9a5d9a22a4af74c2` | bot-challenge | ❌ | ❌ | 2 | 14 | bot_challenge |
| `gen-fd33393388d7ed7f` | bot-challenge | ❌ | ❌ | 2 | 15 | bot_challenge |
| `gen-f85e30776f24b88f` | done | ✅ | ✅ | 3 | 4 |  |

## Step outcomes

- `executed`: 18 (69%)
- `stale`: 2 (8%)
- `refused-empty-enter`: 2 (8%)
- `done-rejected`: 2 (8%)
- `done`: 2 (8%)

low-confidence decisions (< τ): 1
